from data.card_groups import groups

from models.flashcards_models import Stack, Card


async def add_stack_group(stack_name, user):
    cards = []
    # for stack, obj in groups.items():
    #     for answer, question in obj.items():
    #         new_card = Card(answer=str(answer), question=str(question))
    #         # await new_card.create()
    #         cards.append(new_card)
    # cluster = [group for _, group in groups[stack_name].items()]
    # for card in cluster:
    #     for a, q in card.items():
    #         new_card = Card(answer=str(a), question=str(q))
    #         cards.append(new_card)
    for group, data in groups[stack_name].items():
        # group_name = group
        for answer, question in data.items():
            new_card = Card(answer=answer, question=question)
            cards.append(new_card)

        new_stack = Stack(stack=stack_name, group=group, cards=cards)

    # new_stack = Stack(group=stack_name, cards=cards, stack=stack_name)
    return new_stack
