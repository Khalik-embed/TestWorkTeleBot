from enum import Enum
from typing import Any
from dataclasses import dataclass
from lexicon import NAVIGATION

BANNERS = Enum('BANNERS', ['subscrion_required', 'start_menu', 'categories', 'subcategories', 'basket', 'items', 'faq'])
COMMANDS = Enum('COMMANDS', ['add_to_basket', 'payment', 'delete', 'decrement', 'increment', 'back', 'next', 'prev'])
class MenuLevel(Enum):
    start_menu = 0
    categories = 1
    subcategories = 2
    items = 3
    basket = 4
    faq = 5


# class BotCommand:
#     def __init__(self, level : int, slug_name : str, button_name : str):
#         self.level = level
#         self.slug_name = slug_name
#         self.button_name = button_name

# class BotMenu():
#     def __init__(self, level : int, slug_name : str, button_name : str):
#     command : BotCommand
#     sub_command : list[BotCommand] | none



# @dataclass
# class BotCommand:
#     slug_name : str
#     button_name : str
#     next_level : int

# @dataclass
# class MenuPoint():
#     level : int
#     command : list[BotCommand]

# @dataclass
# class BotMenu():
#     menu : list[MenuPoint]

# # def create_menu(arg = None):
# #     ret

# MENU = BotMenu(menu = [
#     MenuPoint(level = 0, command = [BotCommand(slug_name = 'start_menu', button_name = '', next_level = 1)]),

#     MenuPoint(level = 1,
#         command = [BotCommand(slug_name = 'categories', button_name = NAVIGATION['catalog'], next_level = 10)]),
#     MenuPoint(level = 10,
#         command = [BotCommand(slug_name = 'subcategories', button_name = '', next_level = 100)]),
#     MenuPoint(level = 100,
#         command = [BotCommand(slug_name = 'items', button_name = '', next_level = 1000)]),
#     MenuPoint(level = 1000,
#         command = [BotCommand(slug_name = 'basket', button_name = NAVIGATION['basket'], next_level = 20)]),
#     MenuPoint(level = 1000,
#         command = [BotCommand(slug_name = 'add_to_basket', button_name = NAVIGATION['add_to_basket'], next_level = 1000)]),
#     MenuPoint(level = 1000,
#         command = [BotCommand(slug_name = 'prev', button_name = NAVIGATION['prev'], next_level = 1000)]),
#     MenuPoint(level = 1000,
#         command = [BotCommand(slug_name = 'next', button_name = NAVIGATION['next'], next_level = 1000)]),
#     MenuPoint(level = 1000,
#         command = [BotCommand(slug_name = 'subcategories', button_name = NAVIGATION['back'], next_level = )]),
#     MenuPoint(level = 1000,
#         command = [BotCommand(slug_name = 'subcategories', button_name = NAVIGATION['back'], next_level = )]),

#                                 MenuPoint(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu'])
#     MenuPoint(level = 10, command = [BotCommand(slug_name = 'categories', button_name = NAVIGATION['back'], next_level = 1),]),

#     MenuPoint(level = 1, command = [
#         BotCommand(slug_name = 'basket', button_name = NAVIGATION['basket'], next_level = 20),
#         ]),
#     MenuPoint(level = 1, command = [
#         BotCommand(slug_name = 'faq', button_name = NAVIGATION['FAQ'], next_level = 30),
#         ]),


#     ])

# BACKET_MENU = BotMenuPoint(command = BotCommand(level = 1,  slug_name = 'basket', button_name = ),
#                            sub_menu = [
#                                 BotCommand(level = 3, slug_name = 'add_to_basket', button_name = NAVIGATION['add_to_basket']),
#                                 BotCommand(level = 3, slug_name = 'prev', button_name = NAVIGATION['prev']),
#                                 BotCommand(level = 3, slug_name = 'next', button_name = NAVIGATION['next']),
#                                 BotCommand(level = 2,  slug_name = 'subcategories', button_name = NAVIGATION['back']),
#                                 BotCommand(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu'])
#                            ])
# CATEGORY_MENU =

# # MENU = [
#         # MenuPoint(level = 1, , [
#     #     # MenuPoint(level = 2, slug_name = 'subcategories', button_name = '', [
#     #     #     # MenuPoint(level = 3, slug_name = 'items', button_name = '', [
#     #     #     #     MenuPoint(level = 4,  slug_name = 'basket', button_name = NAVIGATION['basket']),
#     #     #     #     MenuPoint(level = 3, slug_name = 'add_to_basket', button_name = NAVIGATION['add_to_basket']),
#     #     #     #     MenuPoint(level = 3, slug_name = 'prev', button_name = NAVIGATION['prev']),
#     #     #     #     MenuPoint(level = 3, slug_name = 'next', button_name = NAVIGATION['next']),
#     #     #     #     MenuPoint(level = 2,  slug_name = 'subcategories', button_name = NAVIGATION['back']),
#     #     #     #     MenuPoint(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu']),
#     #     #     #     ]),
#     #     #     MenuPoint(level = 1, slug_name = 'categories', button_name = NAVIGATION['back']),
#     #     #     MenuPoint(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu'])
#     #     #     ]),
#     #     ]),

#     # MenuPoint(level = 4,  slug_name = 'basket', button_name = NAVIGATION['basket'], [
#     #     MenuPoint(level = 5, slug_name = 'payment', button_name = NAVIGATION['payment']),
#     #     MenuPoint(level = 4, slug_name = 'prev', button_name = NAVIGATION['prev']),
#     #     MenuPoint(level = 4, slug_name = 'next', button_name = NAVIGATION['next']),
#     #     MenuPoint(level = 4, slug_name = 'increment', button_name = NAVIGATION['increment']),
#     #     MenuPoint(level = 4, slug_name = 'decrement', button_name = NAVIGATION['decrement']),
#     #     MenuPoint(level = 4, slug_name = 'delete', button_name = NAVIGATION['delete']),
#     #     MenuPoint(level = 0, slug_name = 'start_menu', button_name = NAVIGATION['start_menu']),
#     # ]),

# # MENU.append_subpoint(MenuPoint(level = 1, slug_name = 'faqs', button_name = NAVIGATION['FAQ']))


# # class CommandPoint:
# #     def __init__(self, level : int, slug_name : str, button_name : str):
# #         self.level = level
# #         self.slug_name = slug_name
# #         self.button_name = button_name

# # MENU =  MenuPoint(level = 0, slug_name = 'start_menu', button_name = '', sub_points = (
# #     MenuPoint(level = 1, slug_name = 'categories', button_name = MENU_LEVEL0_BUTTONS['catalog'], sub_points = (
# #             MenuPoint(level = 2, slug_name = 'subcategories', button_name = '', sub_points = (
# #                     MenuPoint(level = 3, slug_name = 'items', button_name = '')))),
# #     MenuPoint(level = 1, slug_name = 'basket', button_name = MENU_LEVEL0_BUTTONS['basket']),
# #     MenuPoint(level = 1, slug_name = 'FAQ', button_name = MENU_LEVEL0_BUTTONS['FAQ']))))

# #MENU_PAYMENT =
# MENU_BACKET = MenuPoint(level = 4,  slug_name = 'basket', button_name = NAVIGATION['basket'], sub_menu = [
#                 BotCommand(level = 5, slug_name = 'payment', button_name = NAVIGATION['payment']),
#                 BotCommand(level = 4, slug_name = 'prev', button_name = NAVIGATION['prev']),
#                 BotCommand(level = 4, slug_name = 'next', button_name = NAVIGATION['next']),
#                 BotCommand(level = 4, slug_name = 'increment', button_name = NAVIGATION['increment']),
#                 BotCommand(level = 4, slug_name = 'decrement', button_name = NAVIGATION['decrement']),
#                 BotCommand(level = 4, slug_name = 'delete', button_name = NAVIGATION['delete']),
#                 BotCommand(level = 0, slug_name = 'start_menu', button_name = NAVIGATION['start_menu'])])

# MENU_CATEGORIES =   MenuPoint(level = 1, slug_name = 'categories', button_name = NAVIGATION['catalog'], sub_menu = [
#                         BotCommand(level = 2, slug_name = 'subcategories', button_name = ''),
#                         BotCommand(level = 0, slug_name = 'start_menu', button_name = NAVIGATION['back'])])
# MENU_SUBCATEGORIES =

#                             MenuPoint(level = 3, slug_name = 'items', button_name = '', sub_points = [
#                                 MENU_BACKET,
#                                 MenuPoint(level = 3, slug_name = 'add_to_basket', button_name = NAVIGATION['add_to_basket']),
#                                 MenuPoint(level = 3, slug_name = 'prev', button_name = NAVIGATION['prev']),
#                                 MenuPoint(level = 3, slug_name = 'next', button_name = NAVIGATION['next']),
#                                 MenuPoint(level = 2,  slug_name = 'subcategories', button_name = NAVIGATION['back']),
#                                 MenuPoint(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu'])
#                             ])
#                         MenuPoint(level = 1, slug_name = 'categories', button_name = NAVIGATION['back'])
#                         MenuPoint(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu'])
#                         ])
#                 ])
# MENU_FAQ = MenuPoint(level = 1, slug_name = 'faqs', button_name = NAVIGATION['FAQ'])

# # MENU =  BotMenu(level = 0, slug_name = 'start_menu', button_name = '', sub_command =
# #             [BotMenu(level = 1, slug_name = 'categories', button_name = NAVIGATION['catalog'], sub_command =
# #                 BotMenu(level = 2, slug_name = 'subcategories', button_name = '', sub_command = [
# #                     BotMenu(level = 3, slug_name = 'items', button_name = '', sub_command = [
# #                         BotMenu(level = 1,  slug_name = 'basket', button_name = NAVIGATION['basket']),
# #                         BotMenu(level = 3, slug_name = 'add_to_basket', button_name = NAVIGATION['add_to_basket']),
# #                         BotMenu(level = 3, slug_name = 'prev', button_name = NAVIGATION['prev']),
# #                         BotMenu(level = 3, slug_name = 'next', button_name = NAVIGATION['next']),
# #                         BotMenu(level = 2,  slug_name = 'subcategories', button_name = NAVIGATION['back']),
# #                         BotMenu(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu'])
# #                     ]),
# #                     BotMenu(level = 1,  slug_name = 'categories', button_name = NAVIGATION['back'])
# #                 ])
# #             ),
# #             BotMenu(level = 1, slug_name = 'basket', button_name = NAVIGATION['basket']),
# #             BotMenu(level = 1, slug_name = 'faqs', button_name = NAVIGATION['FAQ']), ])
# # MENU = {
# #     'start_menu' :
# # }

# # Menu = {
# #     BotCommand(level = 0, slug_name = 'start_menu', button_name = '') : {
# #         BotCommand(level = 1, slug_name = 'categories', button_name = NAVIGATION['catalog']) : {(
# #             BotCommand(level = 2, slug_name = 'subcategories', button_name = '') : {(
# #                BotCommand(level = 3, slug_name = 'items', button_name = '') : {(
# #                     BotCommand(level = 1,  slug_name = 'basket', button_name = NAVIGATION['basket']),
# #                     BotCommand(level = 3, slug_name = 'add_to_basket', button_name = NAVIGATION['add_to_basket']),
# #                     BotCommand(level = 3, slug_name = 'prev', button_name = NAVIGATION['prev']),
# #                     BotCommand(level = 3, slug_name = 'next', button_name = NAVIGATION['next']),
# #                     BotCommand(level = 2,  slug_name = 'subcategories', button_name = NAVIGATION['back']),
# #                     BotCommand(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu']),
# #                )},
# #             )}
#         #     # MenuPoint(level = 3, slug_name = 'items', button_name = '', [
#         #     #     MenuPoint(level = 4,  slug_name = 'basket', button_name = NAVIGATION['basket']),
#         #     #     MenuPoint(level = 3, slug_name = 'add_to_basket', button_name = NAVIGATION['add_to_basket']),
#         #     #     MenuPoint(level = 3, slug_name = 'prev', button_name = NAVIGATION['prev']),
#         #     #     MenuPoint(level = 3, slug_name = 'next', button_name = NAVIGATION['next']),
#         #     #     MenuPoint(level = 2,  slug_name = 'subcategories', button_name = NAVIGATION['back']),
#         #     #     MenuPoint(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu']),
#         #     #     ]),
#         #     MenuPoint(level = 1, slug_name = 'categories', button_name = NAVIGATION['back']),
#         #     MenuPoint(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu'])
#         #     ]),
# #         )}
# #         BotCommand(level = 1, slug_name = 'basket', button_name = NAVIGATION['basket']),
# #         BotCommand(level = 1, slug_name = 'faqs', button_name = NAVIGATION['FAQ']),
# #     }
# # }
#     # MenuPoint(level = 1, slug_name = 'categories', button_name = NAVIGATION['catalog'], [
#     #     # MenuPoint(level = 2, slug_name = 'subcategories', button_name = '', [
#     #     #     # MenuPoint(level = 3, slug_name = 'items', button_name = '', [
#     #     #     #     MenuPoint(level = 4,  slug_name = 'basket', button_name = NAVIGATION['basket']),
#     #     #     #     MenuPoint(level = 3, slug_name = 'add_to_basket', button_name = NAVIGATION['add_to_basket']),
#     #     #     #     MenuPoint(level = 3, slug_name = 'prev', button_name = NAVIGATION['prev']),
#     #     #     #     MenuPoint(level = 3, slug_name = 'next', button_name = NAVIGATION['next']),
#     #     #     #     MenuPoint(level = 2,  slug_name = 'subcategories', button_name = NAVIGATION['back']),
#     #     #     #     MenuPoint(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu']),
#     #     #     #     ]),
#     #     #     MenuPoint(level = 1, slug_name = 'categories', button_name = NAVIGATION['back']),
#     #     #     MenuPoint(level = 0,  slug_name = 'start_menu', button_name = NAVIGATION['start_menu'])
#     #     #     ]),
#     #     ]),

#     # MenuPoint(level = 4,  slug_name = 'basket', button_name = NAVIGATION['basket'], [
#     #     MenuPoint(level = 5, slug_name = 'payment', button_name = NAVIGATION['payment']),
#     #     MenuPoint(level = 4, slug_name = 'prev', button_name = NAVIGATION['prev']),
#     #     MenuPoint(level = 4, slug_name = 'next', button_name = NAVIGATION['next']),
#     #     MenuPoint(level = 4, slug_name = 'increment', button_name = NAVIGATION['increment']),
#     #     MenuPoint(level = 4, slug_name = 'decrement', button_name = NAVIGATION['decrement']),
#     #     MenuPoint(level = 4, slug_name = 'delete', button_name = NAVIGATION['delete']),
#     #     MenuPoint(level = 0, slug_name = 'start_menu', button_name = NAVIGATION['start_menu']),
#     # ]),

# # MENU.append_subpoint(MenuPoint(level = 1, slug_name = 'faqs', button_name = NAVIGATION['FAQ']))



# # COMMANDS = Enum('COMMANDS', ['add_to_basket', 'payment', 'delete', 'decrement', 'increment', 'back', 'next', 'prev', ])
