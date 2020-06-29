from typing import Dict, Callable, List, Tuple

from ...query import Query
from ...exceptions import UserError
from ...session import Session
from ..util import assert_arguments
from .primitives import get_column_names, get_board_id


def add_column(session: Session, arguments: List[str]):
    board_name, column_name = assert_arguments(arguments, 2)
    board_id, _ = get_board_id(session, board_name)
    column_names = get_column_names(session, board_id)
    Query(session,
          'insert into columns (board_id, name, index) values (%s, %s, %s);',
          (board_id, column_name, len(column_names))).run()
