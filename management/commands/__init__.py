from typing import Dict, Callable, List, Tuple
from ..session import Session
from .flashcards import FLASHCARD_COMMANDS
from .tasks import TASK_COMMANDS 

CommandFunc = Callable[[Session, List[str]], None]
CommandMaps = Dict[str, Dict[str, CommandFunc]]

command_maps: CommandMaps = {
    'flashcards': FLASHCARD_COMMANDS,
    'tasks': TASK_COMMANDS,
}

def build_help_command(maps: CommandMaps):
    def help_command():
        print("Commands:")
        for module_name, cmap in maps.items():
            print(f"\t{module_name}:")
            for k in cmap:
                print(f"\t\t{k}")
    return help_command

help_command = build_help_command(command_maps)
