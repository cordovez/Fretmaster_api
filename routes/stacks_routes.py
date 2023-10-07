"""
User registration router
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

from auth.current_user import get_current_user
from models.flashcards_models import StackName, Stack
from models.user_models import User
from controllers.flash_cards_controllers import add_stack_group

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

stack_router = APIRouter()


@stack_router.get("/all")
async def get_all_stacks():
    stack_list = await Stack.find_all().to_list()
    return stack_list


@stack_router.post("/add", summary="Add cards in stack")
async def add_stack_to_db(
    stack_name: StackName, current_user: Annotated[User, Depends(get_current_user)]
):
    added_stack = await add_stack_group(stack_name, current_user)
    return added_stack
