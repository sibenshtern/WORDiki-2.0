from datetime import datetime

import sqlalchemy
from sqlalchemy import Integer, String, DateTime

from . import SqlAlchemyBase


class Card(SqlAlchemyBase):
    __tablename__ = 'cards'

    id = sqlalchemy.Column(Integer, primary_key=True, autoincrement=True)

    word = sqlalchemy.Column(String, unique=True)
    translate = sqlalchemy.Column(String)

    card_type = sqlalchemy.Column(Integer)
    learning_type = sqlalchemy.Column(Integer)
    last_time = sqlalchemy.Column(DateTime, default=datetime(1970, 1, 1))
