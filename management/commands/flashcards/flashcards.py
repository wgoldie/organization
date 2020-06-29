from typing import List

from psycopg2 import sql

from ..util import assert_arguments
from ...query import Query
from ...session import Session
from .primitives import get_flashcard_deck_id


def add_flashcard(session: Session, arguments: List[str]):
    deck_name, front, back = assert_arguments(arguments, 3)
    deck_id, _ = get_flashcard_deck_id(session, deck_name)
    
    Query(
        session,
        'insert into flashcards (deck_id, front, back) values (%s, %s, %s);',
        (deck_id, front, back),
    ).run()


def list_flashcards(session: Session, arguments: List[str]):
    deck_identifier, = assert_arguments(arguments, 1)
    deck_id, deck_name = get_flashcard_deck_id(session, deck_identifier)

    query = Query(session,
          'select id, front, back from flashcards where deck_id = %s;',
          (deck_id,)
    )
    print(f'(@{deck_id}) {deck_name} - flashcards')
    with query as cursor:
        for flashcard_id, front, back in cursor:
            print(f'\t(*{flashcard_id}) {front} /// {back}')
