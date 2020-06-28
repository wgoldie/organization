import sys
from os import path
from typing import \
    Any, List, Optional, Tuple, Iterable, Dict, \
    NamedTuple, Callable
import psycopg2
import json


def load_config(filename: str) -> dict:
    with open(filename, 'r') as f:
        config = json.load(f)
    return config


class UserError(Exception):
    message: str
    pass


Session = NamedTuple('Session', (
    ('config', dict),
    ('connection', psycopg2.extensions.connection),
))

CommandFunc = Callable[[Session, List[str]], None]


class Query(object):
    def __init__(
        self,
        session: Session,
        command: str,
        format_variables: Optional[Tuple[Any]],
    ):
        self.session = session
        self.cursor = session.connection.cursor()
        self.command = command
        self.format_variables = format_variables

    def _enter(self) -> Iterable[Optional[Tuple[Any, ...]]]:
        self.cursor.execute(self.command, self.format_variables)
        return (tuple(row) for row in self.cursor)

    def __enter__(self) -> Iterable[Optional[Tuple[Any, ...]]]:
        return self._enter()

    def _exit(self) -> None:
        self.session.connection.commit()
        self.cursor.close()

    def __exit__(self, type, value, traceback):
        self._exit()

    def run(self):
        self._enter()
        self._exit()


def assert_arguments(args, min_len: int, max_len: int = None):
    if max_len is None:
        max_len = min_len
    if len(args) < min_len:
        raise UserError("Too few arguments")
    if len(args) > max_len:
        raise UserError("Too many arguments")


def add_board(session, arguments):
    assert_arguments(arguments, 1)
    name, = arguments
    Query(
        session, 'insert into boards (name) values (%s);', (name,)
    ).run()


dispatch_map: Dict[str, CommandFunc] = {
    'add_board': add_board
}


def make_session() -> Session:
    base_path = path.dirname(path.abspath(__file__))
    config_file = path.join(base_path, 'config.json')
    config = load_config(config_file)
    connection=psycopg2.connect(
        dbname=config['DB_NAME'],
        user=config['DB_USER'],
    )
    session = Session(config=config, connection=connection)
    return session


def run_command(command: str, arguments: Iterable[str]):
    session = make_session()
    if command not in dispatch_map:
        print(f'Command {command} not known.')
        sys.exit(1)
    try:
        dispatch_map[command](session, list(arguments))
        session.connection.close()
    except UserError as e:
        print(f'Error: {e.message}')
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    run_command(sys.argv[1], sys.argv[2:])
