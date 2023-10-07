from fastapi import HTTPException, status

from functools import reduce

from models.user_models import User
from models.message_models import Message
from models.flashcards_models import Card

from utils.data_compilers import card_compiler, stack_compiler
from data.card_groups import groups


""" 
POST
"""


async def add_cards_to_user(stack_name, current_user):
    cards_in_groups = await card_compiler(groups[stack_name], stack_name, current_user)
    # card_groups_in_stacks = await stack_compiler(
    #     cards_in_groups, stack_name, current_user
    # )

    return cards_in_groups
    # return card_groups_in_stacks


""" 
GET
"""


async def get_user(id: str):
    """function takes the MongoDB document _id as a string, to search database."""
    found = await User.get(id)
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return found


def get_list_of_stacks(current_user):
    stacks = current_user.stacks
    set_of_stacks = set()
    for stack in stacks:
        set_of_stacks.add(stack.stack)

    return set_of_stacks


async def get_stack_cards(stack_name, current_user):
    this_user = await User.get(current_user.id)
    stacks = this_user.stacks
    cards = []

    for stack in stacks:
        if stack.stack == stack_name:
            cards.append(stack.cards)

    consolidated_cards = reduce(lambda x, y: x + y, cards, [])
    expanded_cards = []

    for card in consolidated_cards:
        expanded_card = await Card.get(card.id, fetch_links=True)
        expanded_cards.append(expanded_card)

    return expanded_cards


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
