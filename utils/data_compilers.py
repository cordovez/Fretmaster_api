from fastapi import HTTPException, status
from models.flashcards_models import Card, UserCardStats, Stack


async def card_compiler(group_data, stack_name, current_user):
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


async def stack_compiler(card_groups, stack_name, current_user):
    new_list_of_stacks = [stack for stack in current_user.stacks]

    if stack_already_exist(new_list_of_stacks, stack_name):
        raise HTTPException(status.HTTP_409_CONFLICT)

    for group, data in card_groups.items():
        new_stack = Stack(stack=stack_name, group=group, cards=data)
        new_list_of_stacks.append(new_stack)

    current_user.stacks = new_list_of_stacks
    await current_user.save()
    return new_list_of_stacks


def stack_already_exist(list_of_stacks, stack_name):
    for group in list_of_stacks:
        if group.stack == stack_name:
            raise HTTPException(status.HTTP_409_CONFLICT)
