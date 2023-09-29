"""
User Models
"""
import pytz
from datetime import datetime
from typing import Optional

from beanie import Document, Link
from pydantic import BaseModel, EmailStr, ConfigDict



central_europe = pytz.timezone('Europe/Paris')

class Card(BaseModel):
    """ keys are: image, question, answer, score, previous_viewed, next_view
    """
    image: Optional[str] 
    question: str
    answer: str
    score: Optional[str]
    previous_view: Optional[datetime] 
    next_view: Optional[datetime]

class Stack(Document):
    """ name: str, cards: list"""
    name: str
    cards: list[Card]
    
    class Settings:
        name = "Stacks"


        