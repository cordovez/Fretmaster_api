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
    question: str
    answer: str

class Stack(BaseModel):
    name: str
    cards: list[Card]  


        