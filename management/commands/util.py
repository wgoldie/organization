from typing import Tuple, Iterable, Optional

from psycopg2 import sql

from ..exceptions import UserError
from ..session import Session
from ..query import Query


def assert_arguments(
    args: Iterable[str], min_len: int, max_len: int = None
) -> Tuple[str, ...]:
    if max_len is None:
        max_len = min_len
    if len(args) < min_len:
        raise UserError("Too few arguments")
    if len(args) > max_len:
        raise UserError("Too many arguments")
    return tuple(args)


class IdError(Exception):
    pass


def parse_name(name: str, id_delimiter: str) -> Optional[int]:
    if not name.startswith(id_delimiter):
        return None
    try:
        return int(name[len(id_delimiter):])
    except (ValueError, TypeError):
        raise IdError()


def get_name_and_id(
        session: Session, table_name: sql.Identifier, row_name: str, *,
        id_delimiter: Optional[str] = None,
) -> Tuple[int, str]:
    id_val = None
    if id_delimiter is not None:
        try:
            id_val = parse_name(row_name, id_delimiter)
        except IdError:
            raise UserError(
                f'References to {table_name} beginning with ' +
                f'{id_delimiter} are treated as raw ids')
    if id_val is not None:
        return Query(
            session,
            sql.SQL('select id, name from {} where id = %s').format(table_name),
            (id_val,),
        ).one()
    else:
        return Query(
            session,
            sql.SQL('select id, name from {} where name = %s;').format(table_name),
            (row_name,),
        ).one()
