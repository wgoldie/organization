from typing import List, Tuple

from psycopg2 import sql

from ..exceptions import UserError
from ..query import Query
from ..session import Session
from .util import get_name_and_id


def get_board_id(session: Session, board_name: str) -> Tuple[int, str]:
    if board_name == '--':
        return Query(
            session,
            'select id, name from boards where is_favorite = true;',
        ).one()
    return get_name_and_id(session, sql.Identifier('boards'), board_name,
                           id_delimiter='@')


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
    return get_name_and_id(session, sql.Identifier('columns'), column_name,
                           id_delimiter='*')


def get_card_id(session: Session, board_id: int, card_name: str):
    return get_name_and_id(session, sql.Identifier('cards'), card_name,
                           id_delimiter='_')


def get_column_names(session: Session, board_id: int) -> List[Tuple[int, str]]:
    query = Query(session, '''
                  select columns.index, columns.name
                  from columns
                  where board_id = %s
                  order by index;''',
                  (board_id,))
    with query as cursor:
        return [(column_index, column_name)
                for column_index, column_name in cursor]
