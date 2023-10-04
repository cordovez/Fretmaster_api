from models.flashcards_models import Card, Stack, UserCardStats
from data.triads import c_major, f_major

keys = {"C major": c_major, "F major": f_major}


async def card_constructor(username):
    """Helper function to help generate a stack of flashcards pertinent to user

    Args:
        username (current_user): The logged-in user

    Returns:
        card_list
    """

    for name, key in keys.items():
        card_list = []
        for k, v in key.items():
            card = Card(
                image=None,
                question=str(v),
                answer=k,
            )
            user_stats = UserCardStats(user=username)
            card.users.append(user_stats)
            card_list.append(card)

        return card_list


async def stack_builder(cards, stack_name):
    """Helper function to help generate a stack of flashcards

    Args:
        cards (list): a collection of cards to add to the Stack
        stack_name (primary key): This key will help prevent duplicates

    Returns:
        Stack: a stack contains cards, which contain user-specific data
    """
    stacks = []
    new_stack = Stack(name=stack_name, cards=cards)
    stacks.append(new_stack)

    for stack in stacks:
        await Stack.create(stack)
    return stacks


async def triads():
    pass


def inversions():
    pass
