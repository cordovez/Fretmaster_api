from data.card_groups import groups

from models.flashcards_models import Stack, Card


async def add_stack_group(stack_name, user):
    stacks = []
    for group, data in groups[stack_name].items():
        new_stack = Stack(stack=stack_name, group=group, cards=[])

        for q, a in data.items():
            new_card = Card(question=q, answer=a)
            await new_card.create()
            new_stack.cards.append(new_card)
        await new_stack.create()

        stacks.append(new_stack)
    return stacks
