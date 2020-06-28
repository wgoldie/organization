from typing import Tuple, Iterable
from ..exceptions import UserError

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
