from typing import List, Tuple

from psycopg2 import sql

from ..util import assert_arguments, get_name_and_id
from ...query import Query
from ...session import Session
from .primitives import get_flashcard_deck_id


def add_flashcard_deck(session: Session, arguments: List[str]):
    name, = assert_arguments(arguments, 1)
    Query(
        session, 'insert into flashcard_decks (name) values (%s);', (name,)
    ).run()


def list_flashcard_decks(session: Session, arguments: List[str]):
    assert_arguments(arguments, 0)
    with Query(session, 'select id, name from flashcard_decks;') as cursor:
        print('Decks:')
        for deck_id, name, in cursor:
            print(f"(@{deck_id}) {name}")


def set_favorite_deck(session: Session, arguments: List[str]) -> None:
    deck_name, = assert_arguments(arguments, 1)
    deck_id, _ = get_flashcard_deck_id(session, deck_name)
    Query(session,
          'update flashcard_decks set is_favorite = (id = %s);',
          (deck_id,)
    ).run()
