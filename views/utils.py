# from typing import Dict, Callable, Sequence
# import os
# import importlib
# from views import *
# BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# module = importlib.import_module(BASE_DIR)
# # views = os.listdir(BASE_DIR)
#
#
# # class Router:
# #     @staticmethod
# #     def register_light_command(*commands: Sequence[str]) -> Dict[str, str]:
# #         light_commands = {}
# #         print(type(commands))
# #         for command in commands:
# #             for view in views:
# #                 if command == view.split('_')[0]:
# #                     light_commands.update(
# #                         {command: view.split('.')[0]}
# #                     )
# #         return light_commands
# #
# #     @staticmethod
# #     def register_sudo_command(commands: str = None) -> Dict[str, Callable]:
# #         if commands is not None:
# #             return {command: view for (command, view) in commands}
# #
# #
# # router = Router()
# # print(router.register_light_command('web', 'share'))
# print('@'*120)
# print(module)

