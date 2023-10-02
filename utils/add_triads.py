
from models.flashcards_models import Card, Stack, Group
from data.triads import c_major, f_major

keys = {"C major":c_major, "F major":f_major}

async def triads(username):
    """Function creates triads stack"""
    stacks = []
    
    for name, key in keys.items():
        card_list = []
        for k, v in key.items():
            card = Card(image=None, question=str(v), answer=k, score=None,
                        previous_view=None, next_view=None, owner=username)
            card_list.append(card)
        
        saved_stack = Stack(name=name, cards=card_list)
        stacks.append(saved_stack)
        
    for stack in stacks:
        await Stack.create(stack)
    # new_group = Group(group_name="Triads", group_stacks=stacks)
    return stacks

def inversions():
     pass

# available_stacks = {
#     "triads": triads,
#     "inversions": inversions,
# }
# async def add_stack_to_user(user, stack):
#     found_user =  await User.get(user.id)
#     print("User: ", found_user.stacks.append(stack))
#     await found_user.stacks.append(stack)