from typing import Dict, Callable, List, Tuple
from ..session import Session
from .boards import add_board, set_favorite_board, list_boards
from .cards import add_card, list_cards, move_card, build_shift_card
from .columns import add_column
from .flashcards import FLASHCARD_COMMANDS


CommandFunc = Callable[[Session, List[str]], None]

TASK_COMMANDS = {
    'add_board': add_board,
    'set_favorite_board': set_favorite_board,
    'list_boards': list_boards,
    'add_card': add_card,
    'list_cards': list_cards,
    'add_column': add_column,
    'move_card': move_card,
    'inc_card': build_shift_card(1),
    'dec_card': build_shift_card(-1),
}


def merge_command_maps(
    *maps: List[Dict[str, CommandFunc]],
) -> Dict[str, CommandFunc]:
    merged = {}
    for cmap in maps:
        for k, v in cmap.items():
            assert k not in merged
            merged[k] = v
    return merged


dispatch_map = merge_command_maps(
    FLASHCARD_COMMANDS,
    TASK_COMMANDS,
)
