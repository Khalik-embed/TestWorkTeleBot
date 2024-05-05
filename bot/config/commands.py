from enum import Enum
from typing import Any
from dataclasses import dataclass
from lexicon import NAVIGATION

BANNERS = Enum('BANNERS', ['subscrion_required', 'start_menu', 'categories', 'subcategories', 'basket', 'items', 'faq'])
COMMANDS = Enum('COMMANDS', ['add_to_basket', 'payment', 'delete', 'decrement', 'increment', 'back', 'next', 'prev', 'faq'])

class MenuLevel(Enum):
    start_menu = 0
    categories = 1
    subcategories = 2
    items = 3
    basket = 4
    faq = 5
