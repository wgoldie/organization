from typing import List
from ..query import Query
from ..session import Session

from .util import assert_arguments
from .primitives import get_board_id, get_column_id, get_column_names


def add_card(session: Session, arguments: List[str]):
    board_name, column_name, card_name = assert_arguments(arguments, 3)
    board_id, _ = get_board_id(session, board_name)
    column_id, _ = get_column_id(session, board_id, column_name)

    Query(
        session,
        'insert into cards (board_id, column_id, name) values (%s, %s, %s);',
        (board_id, column_id, card_name),
    ).run()



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
    def shift_card(session: Session, arguments: List[str]):
        board_name, card_name = assert_arguments(arguments, 2)
        board_id, _ = get_board_id(session, board_name)
        Query(session, '''
              update cards set column_id = sq_table.shifted_column_id
              from (
                  select cards.id as card_id,
                  shifted_column.id as shifted_column_id
                  from cards,
                  columns as base_column,
                  columns as shifted_column
                  where base_column.id = cards.column_id
                  and shifted_column.index = (base_column.index + %s)
                  and cards.name = %s
                  and cards.board_id = %s
              ) as sq_table
              where sq_table.card_id = cards.id;''',
              (shift, card_name, board_id),
              ).run()

    return shift_card
