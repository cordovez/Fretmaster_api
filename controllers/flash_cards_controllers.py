
from models.flashcards_models import Card, Stack
from models.user_models import User
from data.triads import c_major, f_major

keys = {"C":c_major, "F":f_major}

async def triads():
    """Function creates triads stack"""
    stacks = []
    
    for name, key in keys.items():
        card_list = []
        for k, v in key.items():
            card = Card(image=None, question=str(v), answer=k, score=None,
                        previous_view=None, next_view=None)
            card_list.append(card)
        
        saved_stack = Stack(name=f"{name} triads", cards=card_list)
        stacks.append(saved_stack)
        
    for stack in stacks:
        await Stack.create(stack)
    return stacks

def inversions():
     pass

available_stacks = {
    "triads": triads(),
    "inversions": inversions(),
}
async def add_stack_to_user(user, stack):
    found_user =  await User.get(user.id)
    await found_user.stacks.append(stack)