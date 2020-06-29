from typing import List, Tuple

from psycopg2 import sql

from ..util import assert_arguments, get_name_and_id
from ...query import Query
from ...session import Session


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


def get_flashcard_deck_id(session: Session, deck_name: str) -> Tuple[int, str]:
    if deck_name == '--':
        return Query(
            session,
            'select id, name from flashcard_decks where is_favorite = true;',
        ).one()
    return get_name_and_id(session, sql.Identifier('flashcard_decks'),
                           deck_name, id_delimiter='@')


def set_favorite_deck(session: Session, arguments: List[str]) -> None:
    deck_name, = assert_arguments(arguments, 1)
    deck_id, _ = get_flashcard_deck_id(session, deck_name)
    Query(session,
          'update flashcard_decks set is_favorite = (id = %s);',
          (deck_id,)
    ).run()


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


FLASHCARD_COMMANDS = {
    'add_deck': add_flashcard_deck,
    'list_decks': list_flashcard_decks,
    'set_favorite_deck': set_favorite_deck,
    'add_flashcard': add_flashcard,
    'list_flashcards': list_flashcards,
}
