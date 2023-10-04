from models.flashcards_models import Stack
from models.user_models import User


async def get_stacks():
    stacks = await Stack.find().to_list()
    return f"Currently there are {len(stacks)} stacks. They need to be organised"


async def get_users():
    users = await User.find().to_list()
    return users
