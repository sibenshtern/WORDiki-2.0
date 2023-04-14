from enum import Enum
from random import shuffle
from datetime import datetime, timedelta

from sqlalchemy.sql import func

from database import create_session, models
from config import Time


class CardType(Enum):
    UNLEARNED = 0
    STUDIED = 1
    LEARNED = 2


class SessionManager:

    def __init__(self):
        self.session = create_session()
        self.current_cards = []

    def learn_session(self, cards_amount=30):
        cards: list[models.Card] = self.session.query(models.Card) \
            .filter(models.Card.card_type == CardType.UNLEARNED.value).all()
        cards = cards[-cards_amount:] if len(cards) > cards_amount else cards
        self.current_cards = cards
        shuffle(self.current_cards)

    def get_cards_for_repeat(self, learning_type, time) -> list[models.Card]:
        return self.session.query(models.Card) \
            .filter(((func.julianday("now") - func.julianday(models.Card.last_time)) * 3600 >= time.value) &
                    (models.Card.learning_type == learning_type)).all()

    def repeat_session(self):
        self.current_cards.extend(self.get_cards_for_repeat(0, Time.TEN_MINUTES)[:20])
        self.current_cards.extend(self.get_cards_for_repeat(1, Time.DAY)[:15])
        self.current_cards.extend(self.get_cards_for_repeat(2, Time.WEEK)[:10])
        self.current_cards.extend(self.get_cards_for_repeat(3, Time.MONTH)[:7])
        self.current_cards.extend(self.get_cards_for_repeat(4, Time.THREE_MONTHS)[:5])
        self.current_cards.extend(self.get_cards_for_repeat(5, Time.SIX_MONTHS)[:3])

    def finish_session(self):
        self.current_cards.clear()

    def __del__(self):
        self.session.close()
