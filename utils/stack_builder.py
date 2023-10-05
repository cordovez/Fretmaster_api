from models.flashcards_models import Card, Stack, UserCardStats
from data.triads import c_major, f_major

# group_data = {"C major": c_major, "F major": f_major}


async def card_constructor(groups):
    card_groups = {}
    for group, data in groups.items():
        card_list = []
        for k, v in data.items():
            card = Card(image=None, question=str(v), answer=str(k), card_stats=[])
            card_list.append(card)
        card_groups[group] = card_list

    return card_groups


async def stack_builder(card_groups, group_name):
    groups = []
    for group, data in card_groups.items():
        groups.append({group: data})

    stacks = []
    for group in groups:
        for key, cards in group.items():
            new_stack = Stack(stack=key, cards=cards, group=group_name)
            stacks.append(new_stack)

    for stack in stacks:
        await Stack.create(stack)

    return stacks


async def stack(group_data, name):
    cards = await card_constructor(group_data)
    stack = await stack_builder(cards, name)

    # return cards
    return stack
