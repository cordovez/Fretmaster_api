from models.flashcards_models import GroupName
from models.user_models import User
from data.triads import c_major, f_major
from utils.stack_builder import stack

groups = {"triads": {"C triads": c_major, "F triads": f_major}}


async def add_stack_group(group_name):
    stack_group = await stack(groups[group_name], group_name)
    return stack_group
