"""
User registration router
"""

from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from auth.current_user import get_current_user
from models.user_models import User, UserIn, UserUpdate, UserOut, UserOutMinimal
from models.flashcards_models import GroupName, Stack
from models.message_models import Message
from controllers.flash_cards_controllers import add_stack_group

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

stack_router = APIRouter()


@stack_router.get("/all")
async def get_all_stacks():
    stack_list = await Stack.find_all().to_list()
    return stack_list


@stack_router.post("/add")
async def add_stack_to_db(group_name: GroupName):
    added_stack = await add_stack_group(group_name)
    return added_stack
