from models.user_models import UserIn, User
from fastapi import HTTPException, status

from auth.password_hasher import get_password_hash


async def create_new_user(user: UserIn):
    """This function verifies that neither the username nor email passed in as
    'user' parameters, exist in the database.

    if user doesn't already exist, it takes this information information and
    passes it to the to the add_params() function.
    """

    user_email = await User.find_one({"email": user.email})
    user_username = await User.find_one({"username": user.username})

    if user_email is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="user with that email already exists"
        )
    if user_username is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="user with that username already exists"
        )

    with_added_information = add_params(user)

    saved_user = await User.create(with_added_information)
    return saved_user


def add_params(user_in: UserIn):
    """This function, takes the information passed in from 'create_user' and
    additionally generates:
    • hashed_password
    • uri to a generic avatar image

    It creates a user_dict excluding the password passed through 'UserIn' and
    register the new user.

    """
    hashed_password = get_password_hash(user_in.password)
    user_dict = user_in.dict(exclude={"password"})

    user_name = user_dict["username"]
    uri = f"https://api.multiavatar.com/{user_name}.png"
    avatar_dict = {"public_id": None, "uri": uri}
    user = User(
        email=user_dict["email"],
        username=user_dict["username"],
        password_hash=hashed_password,
        avatar=avatar_dict,
    )
    return user
