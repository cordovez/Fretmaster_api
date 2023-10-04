from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from models.user_models import UserIn, User
from models.message_models import Message
from models.flashcards_models import Stack
from beanie import UpdateResponse

from utils.add_triads import triads, inversions
from auth.password_hasher import get_password_hash

STACK_BUILDERS = {
    "triads": triads,
    "inversions": inversions,
}

""" 
POST
"""


async def add_stack_to_user(stack, user):
    # Get all the Stack document with fetch_links
    reveal_user_stacks = await User.get(user.id, fetch_links=True)
    user_stacks = reveal_user_stacks.stacks

    # Get the names of the stacks the user has already
    user_stack_names = []
    if user_stacks is not None:
        for existing in user_stacks:
            user_stack_names.append(existing.name)

    # see Dictionary Dispatch Patter (https://youtu.be/bL0Y-aEnlgY?si=m2pMm7sBGXCUyHkE)
    created_stacks = await STACK_BUILDERS[stack](user.username)

    # Verify that the new stack created does not exist already
    for each_stack in created_stacks:
        if each_stack.name in user_stack_names:
            raise HTTPException(
                status.HTTP_409_CONFLICT, detail="That stack already exists"
            )

    for each_stack in created_stacks:
        user.stacks.append(each_stack)
    await user.save()
    return created_stacks


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
