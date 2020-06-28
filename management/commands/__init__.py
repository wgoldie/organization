from typing import Dict, Callable, List
from .util import assert_arguments
from ..query import Query
from ..session import Session


CommandFunc = Callable[[Session, List[str]], None]


def add_board(session: Session, arguments: List[str]):
    name, = assert_arguments(arguments, 1)
    Query(
        session, 'insert into boards (name) values (%s);', (name,)
    ).run()


def add_card(session: Session, arguments: List[str]):
    board_name, card_name = assert_arguments(arguments, 2)
    Query(session,
    '''
        with source as (select id, %s as name from boards where name = %s)
        insert into cards (board_id, name) (select id, name from source);
    ''', (card_name, board_name)
    ).run()


dispatch_map: Dict[str, CommandFunc] = {
    'add_board': add_board,
    'add_card': add_card
}
