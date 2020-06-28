from typing import Dict, Callable, List
from .util import assert_arguments
from ..query import Query
from ..session import Session


CommandFunc = Callable[[Session, List[str]], None]


def add_board(session, arguments):
    assert_arguments(arguments, 1)
    name, = arguments
    Query(
        session, 'insert into boards (name) values (%s);', (name,)
    ).run()


dispatch_map: Dict[str, CommandFunc] = {
    'add_board': add_board
}
