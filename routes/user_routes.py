"""
User registration router
"""

from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from auth.current_user import get_current_user
from models.user_models import User, UserIn, UserUpdate, UserOut
from models.flashcards_models import StackName, Stack
from models.message_models import Message
from controllers.user_controllers import (
    delete_user,
    update_user_data,
    add_cards_to_user,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_router = APIRouter()


# Create


@user_router.post("/add-cards")
async def add_cards(
    stack_name: StackName, current_user: Annotated[User, Depends(get_current_user)]
):
    added_stack = await add_cards_to_user(stack_name, current_user)
    return added_stack


# Read


@user_router.get("/profile")
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserOut:
    """Route takes an id and current_user as parameters.  Route requires
    ('Depends' on) the authorization 'get_current_user'.

    It searches for the id in the database and returns db document (model: User)
    """
    found_user = await User.get(current_user.id, fetch_links=True)
    return found_user


@user_router.get("/stacks")
async def get_my_stacks(
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[Stack]:
    user = await User.get(current_user.id, fetch_links=True)
    return user.stacks


# Update
@user_router.patch("/update")
async def update_user(
    update_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserOut:
    result = await update_user_data(update_data, current_user)
    return result


# Delete
@user_router.delete("/remove")
async def delete_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> Message:
    user_has_been_deleted = await delete_user(current_user)

    return user_has_been_deleted
