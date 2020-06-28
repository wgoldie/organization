from typing import Dict, Callable, List, Tuple
from .util import assert_arguments
from ..query import Query
from ..exceptions import UserError
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


def get_board_id(session: Session, board_name: str) -> Tuple[int, str]:
    if board_name == '--':
        return Query(
            session,
            'select id, name from boards where is_favorite = true;',
        ).one()
    return Query(
        session,
        'select id, name from boards where name = %s;',
        (board_name,),
    ).one()


def set_favorite_board(session: Session, arguments: List[str]) -> None:
    board_name, = assert_arguments(arguments, 1)
    Query(session,
          'update boards set is_favorite = (name = %s);',
          (board_name,),
    ).run()


def get_column_id(session: Session, board_id: int, column_name: str) -> Tuple[int, str]:
    if column_name == '--':
        return Query(
            session,
            '''
                select id, name from columns where board_id = %s
                order by index limit 1;
            ''',
            (board_id,),
        ).one()
    return Query(
        session,
        'select id, name from columns where name = %s and board_id = %s;',
        (column_name, board_id),
    ).one()


def add_card(session: Session, arguments: List[str]):
    board_name, column_name, card_name = assert_arguments(arguments, 3)
    board_id, _ = get_board_id(session, board_name)
    column_id, _ = get_column_id(session, board_id, column_name)

    Query(
        session,
        'insert into cards (board_id, column_id, name) values (%s, %s, %s);',
        (board_id, column_id, card_name),
    ).run()


def get_column_names(session: Session, board_id: int) -> List[str]:
    query = Query(session, '''
                  select columns.name
                  from columns
                  where board_id = %s
                  order by index;''',
                  (board_id,))
    columns = []
    with query as cursor:
        for column_name, in cursor:
            columns.append(column_name)
    return columns


def list_cards(session: Session, arguments: List[str]):
    board_name_arg, = assert_arguments(arguments, 1)
    board_id, board_name = get_board_id(session, board_name_arg)
    column_names = get_column_names(session, board_id)
    columns = {column_name: [] for column_name in column_names}
    query = Query(session,
              '''select cards.name, columns.name
              from cards, columns
              where cards.column_id = columns.id
              and cards.board_id = %s;''',
              (board_id,))
    with query as cursor:
        print(f'{board_name} - Cards:')
        for card_name, column_name in cursor:
            columns[column_name].append(card_name)
    for column_name, card_names in columns.items():
        print(f'- {column_name}')
        for card_name in card_names:
            print(f'\t- {card_name}')


def add_column(session: Session, arguments: List[str]):
    board_name, column_name = assert_arguments(arguments, 2)
    board_id, _ = get_board_id(session, board_name)
    column_names = get_column_names(session, board_id)
    Query(session,
          'insert into columns (board_id, name, index) values (%s, %s, %s);',
          (board_id, column_name, len(column_names))).run()


def move_card(session: Session, arguments: List[str]):
    board_name, card_name, column_name = assert_arguments(arguments, 3)
    board_id, _ = get_board_id(session, board_name) 
    column_id, _ = get_column_id(session, board_id, card_name)
    Query(session,
          '''update cards set column_id = %s
          where card_name = %s
          and board_id = %s;''',
          (column_id, card_name, board_id)).run()


def build_shift_card(shift: int):
    def shift_card(session: Session, board_name: str, card_name: int):
        board_id, _ = get_board_id(session, board_name) 
        Query(session, '''
              with (
                  select cards.id as card_id,
                  shifted_column.id as shifted_column_id
                  from cards, columns as base_column, columns as shifted_column
                  where base_column.id = cards.column_id
                  and shifted_column.index = (base_column.index + %s)
                  and cards.name = %s
                  and cards.board_id = %s
              ) as sq_table
              update cards set column = sq_table.shifted_column_id
              from sq_table
              where sq_table.card_id = cards.id;''',
              (shift, card_name, board_id),
              ).run()

    return shift_card


dispatch_map: Dict[str, CommandFunc] = {
    'add_board': add_board,
    'set_favorite_board': set_favorite_board,
    'list_boards': list_boards,
    'add_card': add_card,
    'list_cards': list_cards,
    'add_column': add_column,
    'move_card': move_card,
    'ind_card': build_shift_card(1),
    'dec_card': build_shift_card(-1),
}
