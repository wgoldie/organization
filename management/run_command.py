import sys
from typing import Iterable
from .commands import dispatch_map
from .session import make_session
from .exceptions import UserError


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
