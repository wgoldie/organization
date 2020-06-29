from typing import List, Tuple
from ..exceptions import UserError
from ..query import Query
from ..session import Session


def get_board_id(session: Session, board_name: str) -> Tuple[int, str]:
    if board_name == '--':
        return Query(
            session,
            'select id, name from boards where is_favorite = true;',
        ).one()
    if board_name.startswith('@'):
        try:
            board_id = int(board_name[1:])
        except (TypeError, ValueError):
            raise UserError(
                'Board references beginning with @ are treated as raw ids')
        return Query(
            session,
            'select id, name from boards where id = %s',
            (board_id,),
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
    if column_name.startswith('*'):
        try:
            column_id = int(column_name[1:])
        except (TypeError, ValueError):
            raise UserError(
                'Column references beginning with * are treated as raw ids')
        return Query(
            session,
            'select id, name from columns where id = %s and board_id = %s',
            (column_id, board_id),
        ).one()
    return Query(
        session,
        'select id, name from columns where name = %s and board_id = %s;',
        (column_name, board_id),
    ).one()


def get_card_id(session: Session, board_id: int, card_name: str):
    if card_name.startswith('_'):
        try:
            card_id = int(card_name[1:])
        except (TypeError, ValueError):
            raise UserError(
                'Card references beginning with _ are treated as raw ids')
        return Query(
            session,
            'select id, name from cards where id = %s and board_id = %s',
            (card_id, board_id),
        ).one()
    return Query(
        session,
        'select id, name from cards where name = %s and board_id = %s',
        (card_name),
    ).one()


def get_column_names(session: Session, board_id: int) -> List[Tuple[int, str]]:
    query = Query(session, '''
                  select columns.id, columns.name
                  from columns
                  where board_id = %s
                  order by index;''',
                  (board_id,))
    with query as cursor:
        return [(column_id, column_name)
                for column_id, column_name in cursor]
