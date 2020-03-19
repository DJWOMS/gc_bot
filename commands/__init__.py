"""Light commands available to all users. But sudo only admin or sudoers"""
from typing import Sequence, Dict, Callable

from views import *
import views


def init_light_command(*commands: Sequence[str]) -> Dict[str, Callable]:
    light_command = {}
    for command in commands:
        for view in views.__all__:
            if command == view.split('_')[0]:
                try:
                    light_command[f'!{command}'] = getattr(globals()[view], view)
                except AttributeError as err:
                    print(
                        f'{err}. '
                        f'May be you forget add or rename function. Module and function name must be the same name!'
                    )
    return light_command


def init_sudo_command(*commands: Sequence[str]) -> Dict[str, Callable]:
    sudo_command = {}
    for command in commands:
        for view in views.__all__:
            if command == view.split('_')[0]:
                try:
                    sudo_command[f'!{command}'] = getattr(globals()[view], view)
                except AttributeError as err:
                    print(
                        f'{err}. '
                        f'May be you forget add or rename function. Module and function name must be the same name!'
                    )
    return sudo_command
