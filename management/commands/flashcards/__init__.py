from .decks import add_flashcard_deck, list_flashcard_decks, set_favorite_deck
from .flashcards import add_flashcard, list_flashcards
from .review import print_response_codes, review_flashcard

FLASHCARD_COMMANDS = {
    'add_deck': add_flashcard_deck,
    'list_decks': list_flashcard_decks,
    'set_favorite_deck': set_favorite_deck,
    'add_flashcard': add_flashcard,
    'review_flashcard': review_flashcard,
    'print_flashcard_codes': print_response_codes,
    'list_flashcards': list_flashcards,
}
