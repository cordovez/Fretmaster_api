from fastapi import HTTPException, status
from models.flashcards_models import Stack, Card
from models.user_models import User


async def get_stacks(user):
    if not user.admin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    stacks = await Card.find().to_list()
    return f"Currently there are {len(stacks)} stacks. They need to be organised"


async def get_users(user):
    if not user.admin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    users = await User.find().to_list()
    return users


ADMIN_USERS = ["cordovez", "jane"]


async def make_admin(admin_name, current_user):
    if current_user.username.lower() not in ADMIN_USERS:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED)

    found_user = await User.find_one(User.username == admin_name.lower())

    if not found_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    await found_user.update({"$set": {"admin": True}})

    return found_user
