"""
Public Access router
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from models.user_models import UserIn, UserOut
from models.message_models import Message
from controllers.public_controllers import create_new_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

public_router = APIRouter()


@public_router.get("/")
def root() -> Message:
    """Route is point of entry and publicly accessible"""
    welcome_message = Message(message="""Welcome to my Fretmaster.""")
    return welcome_message


@public_router.post("/register")
async def add_user_to_db(user: UserIn) -> UserOut:
    """To create a new user, you only need to pass in email, username, and
    password (model: UserIn).

    The password will be converted to a hash before saving and a generic avatar
    will be generated.

    Return is a database document (model: User)
    """
    new_user = await create_new_user(user)

    return new_user
