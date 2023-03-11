from datetime import datetime
from enum import Enum


class CardType(Enum):
    UNLEARNED = 0
    STUDIED = 1
    LEARNED = 2


class Card:

    def __init__(self, word, translate, _type=CardType.UNLEARNED, last_time=datetime(1970, 1, 1)):
        self.word = word
        self.translate = translate
        self.type = _type
        self.last_time = last_time