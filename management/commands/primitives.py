from typing import List, Tuple
from ..query import Query
from ..session import Session


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
