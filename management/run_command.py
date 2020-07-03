import sys
from typing import Iterable
from .commands import command_maps, help_command
from .session import make_session
from .exceptions import UserError


def run_command(arguments: Iterable[str]):
    session = make_session()
    command_module = arguments[0].strip().lower()
    if command_module in ('?', 'help', '--help'):
        help_command()
        sys.exit(0)

    if command_module not in command_maps:
        print(f'Module {command_module} not known.')
        sys.exit(1)

    command = arguments[1].strip().lower()
    module_map = command_maps[command_module]
    if command not in module_map:
        print(f'Command {command} not known for module {command_module}.')
        sys.exit(1)

    try:
        module_map[command](session, list(arguments[2:]))
        session.connection.close()
    except UserError as e:
        print(f'Error: {e.message}')
        sys.exit(1)
    sys.exit(0)
