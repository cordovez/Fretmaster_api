"""
User registration router
"""

from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from auth.current_user import get_current_user
from models.user_models import User, UserIn, UserUpdate, UserOut, UserOutMinimal
from models.flashcards_models import StackName, Stack
from models.message_models import Message
from controllers.user_controllers import (
    delete_user,
    update_user_data,
    add_stack_reference_to_user,
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

user_route = APIRouter()


# Create


@user_route.post("/add-stack")
async def add_stack(
    stack: str, current_user: Annotated[User, Depends(get_current_user)]
):
    # async def add_stack(
    #     stack: str, current_user: Annotated[User, Depends(get_current_user)]
    # ) -> list[Stack]:
    """Route adds a specified "stack" of flashcards

    Args:
        stack (StackName): name of the stack
        current_user (Annotated[User, Depends): currently signed-on user

    Returns:
        Stack: the new stack
    """
    result = await add_stack_reference_to_user(stack, current_user)
    return result


# Read


@user_route.get("/profile")
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_user)]
) -> UserOut:
    """Route takes an id and current_user as parameters.  Route requires
    ('Depends' on) the authorization 'get_current_user'.

    It searches for the id in the database and returns db document (model: User)
    """
    found_user = await User.get(current_user.id, fetch_links=True)
    return found_user


@user_route.get("/stacks")
async def get_my_things(
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[Stack]:
    user = await User.get(current_user.id, fetch_links=True)
    return user.stacks


# Update
@user_route.patch("/update")
async def update_user(
    update_data: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserOut:
    result = await update_user_data(update_data, current_user)
    return result


# Delete
@user_route.delete("/remove")
async def delete_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> Message:
    user_has_been_deleted = await delete_user(current_user)

    return user_has_been_deleted
