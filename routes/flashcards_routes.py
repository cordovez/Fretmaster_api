"""
User registration router
"""

from fastapi import APIRouter, Depends 
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer

from models.message_models import Message
from models.user_models import User
from controllers.flash_cards_controllers import available_stacks, add_stack_to_user

from auth.current_user import get_current_user
from controllers.user_controllers import (create_user, get_users, get_user,
                                          delete_user_by_id, update_user_data)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

flashcard_route = APIRouter()

# Create
@flashcard_route.post("/add_stack")
async def add_stack( stack: str, current_user: Annotated[User, Depends(get_current_user)]):
    """Route takes stack name to create stack and add to current user document. 
    To do: convert stack type to Enum?"""
    
    new_stack= await available_stacks[stack]
    return new_stack
    # await add_stack_to_user(current_user, new_stack)
    # return current_user
    
    