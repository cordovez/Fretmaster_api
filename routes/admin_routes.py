"""
Admin privileges
"""

from fastapi import APIRouter, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from models.message_models import Message
from models.user_models import User, UserOutMinimal

from controllers.admin_controllers import get_stacks, get_users
from auth.current_user import get_current_user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
admin_router = APIRouter()


# Read
@admin_router.get("/all_stacks")
async def read_all_stacks(current_user: Annotated[User, Depends(get_current_user)]):
    stacks = await get_stacks()
    return stacks


@admin_router.get("/all_users")
async def read_all_users(
    current_user: Annotated[User, Depends(get_current_user)]
) -> list[UserOutMinimal]:
    users_list = await get_users()

    return users_list
