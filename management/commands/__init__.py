from typing import Dict, Callable, List, Tuple
from ..session import Session
from .flashcards import FLASHCARD_COMMANDS
from .tasks import TASK_COMMANDS 

CommandFunc = Callable[[Session, List[str]], None]

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
