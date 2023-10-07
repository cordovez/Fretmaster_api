from data.triads import c_major, f_major
from data.inversions import inversions


groups = {
    "triads": {"C triads": c_major, "F triads": f_major},
    "inversions": {
        "Inversions": inversions,
    },
}


async def add_stack_group(group_name, user):
    pass
