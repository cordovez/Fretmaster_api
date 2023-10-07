from data.triads import c_major, f_major
from data.inversions import inversions
from utils.stack_builder import stack

# groups = {"name_of_group":{"name_of_stack": (list of card dict/obj with answer:question)}}

groups = {
    "triads": {"C triads": c_major, "F triads": f_major},
    "inversions": {
        "Inversions": inversions,
    },
}


async def add_stack_group(group_name, user):
    stack_group = await stack(groups[group_name], group_name, user)
    return stack_group
