from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from models.user_models import UserIn, User
from models.message_models import Message
from models.flashcards_models import Stack, GroupName, UserCardStats
from beanie import UpdateResponse

# from utils.add_triads import triads, inversions
from auth.password_hasher import get_password_hash

# STACK_BUILDERS = {
#     "triads": triads,
#     "inversions": inversions,
# }

""" 
POST
"""


# async def add_stats(user):
#     stats = UserCardStats(user=user.username)
#     found_user = await User.get(user.id)
#     user_stacks = found_user.stack.to_list()

#     for group in user_stacks:
#         for card in group["cards"]:
#             card.card_stats.append(stats)


async def add_card_group_reference_to_user(group, user):
    stats = UserCardStats(user=user.username)
    found_groups = await Stack.find(Stack.group == group).to_list()
    for group in found_groups:
        for card in group.cards:
            card.card_stats.append(stats)

    found_user = await User.find_one(User.id == user.id)

    user_with_stacks = await found_user.update({"$set": {"stacks": found_groups}})
    await user_with_stacks.save()

    return user_with_stacks


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
