"""
Card models
"""
import pytz
import pymongo
from enum import Enum
from datetime import datetime
from typing import Optional

from beanie import Document, Link, Indexed, View
from pydantic import BaseModel, Field


central_europe = pytz.timezone("Europe/Paris")


class StackName(str, Enum):
    triads = "triads"
    inversions = "inversions"


class UserCardStats(Document):
    """Adds user-specific information to each card"""

    question: Optional[str] | None = None
    user: Optional[str] | None = None
    score: Optional[int] | None = 0
    created_at: Optional[datetime] = datetime.now(central_europe)
    previous_view: Optional[datetime] | None = None
    next_view: Optional[datetime] | None = None

    class Settings:
        name = "Card Stats"


class Card(Document):
    """keys are: image, question, answer, score, previous_viewed, next_view"""

    image: Optional[str] | None = None
    question: str
    answer: str
    card_stats: Optional[list[Link[UserCardStats]]] | None = []

    class Settings:
        name = "Cards"


class Stack(BaseModel):
    """name: str, cards: list"""

    stack: str
    group: Indexed(str, index_type=pymongo.TEXT)
    cards: list[Card]

    class Settings:
        name = "Stacks"
