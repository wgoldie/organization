from typing import List
from .util import assert_arguments
from ..query import Query
from ..session import Session


def add_board(session: Session, arguments: List[str]):
    name, = assert_arguments(arguments, 1)
    Query(
        session, 'insert into boards (name) values (%s);', (name,)
    ).run()


def list_boards(session: Session, arguments: List[str]):
    assert_arguments(arguments, 0)
    with Query(session, 'select name from boards;') as cursor:
        print('Boards:')
        for name, in cursor:
            print(f"- {name}")


def set_favorite_board(session: Session, arguments: List[str]) -> None:
    board_name, = assert_arguments(arguments, 1)
    Query(session,
          'update boards set is_favorite = (name = %s);',
          (board_name,)).run()
