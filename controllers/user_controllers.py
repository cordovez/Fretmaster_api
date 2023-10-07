from fastapi import HTTPException, status

from models.user_models import User
from models.message_models import Message
from models.flashcards_models import Stack, UserCardStats

from utils.data_compilers import card_compiler, stack_compiler
from data.card_groups import groups


""" 
POST
"""


async def add_cards_to_user(stack_name, current_user):
    cards_in_groups = await card_compiler(groups[stack_name], stack_name, current_user)
    card_groups_in_stacks = await stack_compiler(
        cards_in_groups, stack_name, current_user
    )

    return card_groups_in_stacks


""" 
GET
"""


async def get_user(id: str):
    """function takes the MongoDB document _id as a string, to search database."""
    found = await User.get(id)
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return found


"""
Patch
"""


async def update_user_data(update_data, user):
    update_data = update_data.dict(exclude_unset=True)

    await User.find_one(User.id == user.id).update({"$set": update_data})
    updated_user = await User.get(user.id)
    return updated_user


async def delete_user(user):
    """function takes the MongoDB document _id as a string, to search database
    for document and delete it.
    """
    success_message = Message(message="user deleted")
    user_found = await User.get(user.id)

    if user_found is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    await user_found.delete()
    return success_message


async def add_avatar_image(user):
    # Upload to Cloudinary
    # file_info = uploadImage(path_to_image)
    user = await User.get(user.id)

    await user.save()

    return True


async def add_generic_avatar(user):
    """Function to automatically add a generic avatar on new user create"""

    user = await User.get(user._id)
    user.avatar = "https://api.multiavatar.com/" + user.username + ".png"

    await user.save()

    return True
