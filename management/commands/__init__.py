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


def list_boards(session: Session, arguments: List[str]):
    assert_arguments(arguments, 0)
    with Query(session, 'select name from boards;') as cursor:
        print('Boards:')
        for name, in cursor:
            print(f"- {name}")


def add_card(session: Session, arguments: List[str]):
    board_name, card_name = assert_arguments(arguments, 2)
    Query(session,
    '''
        with source as (select id, %s as name from boards where name = %s)
        insert into cards (board_id, name) (select id, name from source);
    ''', (card_name, board_name)
    ).run()


def list_cards(session: Session, arguments: List[str]):
    board_name, = assert_arguments(arguments, 1)
    
    query = Query(session,
                  '''select columns.name
                  from columns, boards
                  where columns.board_id = boards.id
                  and boards.name = %s order by columns.index;''',
                  (board_name,))
    columns = {None: []}
    with query as cursor:
        for column_name, in cursor:
            columns[column_name] = []

    query = Query(session,
                  '''select cards.name, columns.name
                  from cards
                  left join columns on columns.id = cards.column_id
                  inner join boards on boards.id = cards.board_id
                  and boards.name = %s;''',
                  (board_name,))
    with query as cursor:
        print(f'{board_name} - Cards:')
        for card_name, column_name in cursor:
            columns[column_name].append(card_name)
    for column_name, card_names in columns.items():
        print(f'- {column_name}')
        for card_name in card_names:
            print(f'\t- {card_name}')


dispatch_map: Dict[str, CommandFunc] = {
    'add_board': add_board,
    'list_boards': list_boards,
    'add_card': add_card,
    'list_cards': list_cards
}
