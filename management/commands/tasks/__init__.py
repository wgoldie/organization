from .boards import add_board, set_favorite_board, list_boards
from .cards import add_card, list_cards, move_card, build_shift_card
from .columns import add_column


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
