from fastapi import HTTPException, status
from models.flashcards_models import Card, UserCardStats, Stack
from models.user_models import User


async def card_compiler(group_data, group_name, current_user):
    user_stats = UserCardStats(user=current_user.username)
    await user_stats.create()
    card_groups = {}
    for group, data in group_data.items():
        card_list = []
        for k, v in data.items():
            card = Card(
                image=None, question=str(v), answer=str(k), card_stats=[user_stats]
            )
            await card.create()
            card_list.append(card)
        card_groups[group] = card_list

    return card_groups


async def stack_compiler(card_groups, group_name, current_user):
    new_list_of_stacks = [stack for stack in current_user.stacks]
    if group_name in current_user.stacks:
        raise HTTPException(status.HTTP_409_CONFLICT)

    for group, data in card_groups.items():
        new_stack = Stack(stack=group_name, group=group, cards=data)
        new_list_of_stacks.append(new_stack)

    current_user.stacks = new_list_of_stacks
    await current_user.save()
    return current_user


def stack_already_exist(list_of_stacks, group_name):
    for group in list_of_stacks:
        for key, data in group.items():
            if key["stack"] == group_name:
                return False
