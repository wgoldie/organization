from typing import List, Tuple

from psycopg2 import sql

from ..util import get_name_and_id
from ...query import Query
from ...session import Session


def get_flashcard_deck_id(session: Session, deck_name: str) -> Tuple[int, str]:
    if deck_name == '--':
        return Query(
            session,
            'select id, name from flashcard_decks where is_favorite = true;',
        ).one()
    return get_name_and_id(session, sql.Identifier('flashcard_decks'),
                           deck_name, id_delimiter='@')
