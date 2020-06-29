from typing import List
from .util import assert_arguments
from ..query import Query
from ..session import Session
from .primitives import get_board_id


def add_board(session: Session, arguments: List[str]):
    name, = assert_arguments(arguments, 1)
    Query(
        session, 'insert into boards (name) values (%s);', (name,)
    ).run()


def list_boards(session: Session, arguments: List[str]):
    assert_arguments(arguments, 0)
    with Query(session, 'select id, name from boards;') as cursor:
        print('Boards:')
        for board_id, name, in cursor:
            print(f"(@{board_id}) {name}")


def set_favorite_board(session: Session, arguments: List[str]) -> None:
    board_name, = assert_arguments(arguments, 1)
    board_id, _ = get_board_id(session, board_name) 
    Query(session,
          'update boards set is_favorite = (id = %s);',
          (board_id,)).run()
