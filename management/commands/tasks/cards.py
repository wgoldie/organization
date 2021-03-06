from typing import List

from ...query import Query
from ...session import Session
from ..util import assert_arguments
from .primitives import \
    get_board_id, get_column_id, \
    get_column_names, get_card_id


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
    columns = {column_index: (column_name, [])
               for column_index, column_name in column_names}
    query = Query(session,
                  '''select cards.id,
                  cards.name,
                  columns.index
                  from cards, columns
                  where cards.column_id = columns.id
                  and cards.board_id = %s;''',
                  (board_id,))
    with query as cursor:
        print(f'(@{board_id}) {board_name}:')
        for card_id, card_name, column_index in cursor:
            columns[column_index][1].append((card_id, card_name))
    for column_index, (column_name, card_names) in columns.items():
        print(f'\t(*{column_index}) {column_name}')
        for card_id, card_name in card_names:
            print(f'\t\t(_{card_id}) {card_name}')


def edit_card(session: Session, arguments: List[str]):
    board_name, card_name, edit = assert_arguments(arguments, 3)
    board_id, _ = get_board_id(session, board_name)
    card_id, _ = get_card_id(session, board_id, card_name)
    Query(session,
          '''update cards set name = %s
          where cards.id = %s
          and board_id = %s;''',
          (edit, card_id, board_id)).run()


def move_card(session: Session, arguments: List[str]):
    board_name, card_name, column_name = assert_arguments(arguments, 3)
    board_id, _ = get_board_id(session, board_name)
    column_id, _ = get_column_id(session, board_id, column_name)
    card_id, _ = get_card_id(session, board_id, card_name)
    Query(session,
          '''update cards set column_id = %s
          where cards.id = %s
          and board_id = %s;''',
          (column_id, card_id, board_id)).run()


def build_shift_card(shift: int):
    def shift_card(session: Session, arguments: List[str]):
        board_name, card_name = assert_arguments(arguments, 2)
        board_id, _ = get_board_id(session, board_name)
        card_id, _ = get_card_id(session, board_id, card_name)
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
                  and cards.id = %s
                  and cards.board_id = %s
              ) as sq_table
              where sq_table.card_id = cards.id;''',
              (shift, card_id, board_id),
              ).run()

    return shift_card
