"""
User Models
"""
import pytz
from datetime import datetime
from typing import Optional, List
from bson import ObjectId

from beanie import Document, Link
from pydantic import BaseModel, EmailStr, ConfigDict, Field

from models.flashcards_models import Stack
from utils.object_id import PyObjectId


central_europe = pytz.timezone("Europe/Paris")


class ImageBase(BaseModel):
    public_id: str
    uri: str


class User(Document):
    """User database representation"""

    model_config = ConfigDict(extra="allow")

    first_name: Optional[str] | None = None
    last_name: Optional[str] | None = None
    created_at: Optional[datetime] = datetime.now(central_europe)
    disabled: bool = False
    admin: bool = False
    email: Optional[EmailStr] | None = None
    username: Optional[str] | None = None
    password_hash: Optional[str] | None = None
    stacks: List[Link[Stack]] = []

    class Settings:
        name = "Users"


class UserIn(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserOutMinimal(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    admin: bool
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr

    class Config:
        json_encoders = {ObjectId: str}


class UserOut(BaseModel):
    model_config = ConfigDict(extra="allow")

    first_name: Optional[str]
    last_name: Optional[str]
    avatar: dict
    email: EmailStr
    username: str
    created_at: datetime
    stacks: List[Link[Stack]]


class UserUpdate(BaseModel):
    """User database representation"""

    model_config = ConfigDict(extra="allow")

    first_name: Optional[str] | None = None
    last_name: Optional[str] | None = None
    email: Optional[EmailStr] | None = None
    username: Optional[str] | None = None
