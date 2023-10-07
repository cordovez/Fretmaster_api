from models.flashcards_models import Card, Stack


async def card_constructor(groups):
    card_groups = {}
    for group, data in groups.items():
        card_list = []
        for k, v in data.items():
            card = Card(image=None, question=str(v), answer=str(k), card_stats=[])
            card_list.append(card)
        card_groups[group] = card_list

    return card_groups


async def stack_builder(card_groups, group_name, owner):
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


async def stack(group_data, group_name, owner):
    cards = await card_constructor(group_data)
    stack = await stack_builder(cards, group_name, owner)

    # return cards
    return stack
