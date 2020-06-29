from typing import Tuple, Optional, Iterable, Any

import psycopg2

from .session import Session

class Query(object):
    def __init__(
        self,
        session: Session,
        command: str,
        format_variables: Optional[Tuple[Any]] = None,
    ):
        self.session = session
        self.cursor = session.connection.cursor()
        self.command = command
        self.format_variables = format_variables

    def _enter(self) -> Iterable[Optional[Tuple[Any, ...]]]:
        self.cursor.execute(self.command, self.format_variables)
        return (tuple(row) for row in self.cursor)

    def __enter__(self) -> Iterable[Optional[Tuple[Any, ...]]]:
        return self._enter()

    def _exit(self) -> None:
        self.session.connection.commit()
        self.cursor.close()

    def __exit__(self, type, value, traceback):
        self._exit()

    def run(self):
        self._enter()
        self._exit()

    def one(self):
        results = list(self._enter())
        assert len(results) == 1
        return results[0]

    def one_or_none(self):
        results = list(self._enter())
        assert len(results) <= 1
        return results[0] if len(results) > 0 else None
