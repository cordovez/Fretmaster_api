"""
User Models
"""
import pytz
from enum import Enum
from datetime import datetime
from typing import Optional

from beanie import Document, Link
from pydantic import BaseModel, EmailStr, ConfigDict


central_europe = pytz.timezone("Europe/Paris")


class StackName(str, Enum):
    triads = ("triads",)
    inversions = "inversions"


class Card(BaseModel):
    """keys are: image, question, answer, score, previous_viewed, next_view"""

    image: Optional[str]
    question: str
    answer: str
    score: Optional[str]
    previous_view: Optional[datetime]
    next_view: Optional[datetime]
    owner_stats: str


class Stack(Document):
    """name: str, cards: list"""

    name: str
    cards: list[Card]

    class Settings:
        name = "Stacks"


class Group(Document):
    group_name: str
    group_stacks: list[Stack]
