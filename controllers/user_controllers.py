from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException, status
from models.user_models import UserIn, User
from models.message_models import Message
from models.flashcards_models import Stack

from utils.add_triads import triads, inversions
from auth.password_hasher import get_password_hash

STACK_BUILDERS = {
    "triads" : triads,
    "inversions" : inversions,
}

""" 
POST
"""
async def create_user( user: UserIn):
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
        avatar=avatar_dict
    )
    return user

async def add_stack_to_user(stack, user ):
    # Do we have the correct stack name?
    if stack not in STACK_BUILDERS:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="That is the incorrect name of a stack"
        )
    # Get all the Stack document with fetch_links
    reveal_user_stacks = await User.get(user.id, fetch_links=True)   
    user_stacks = reveal_user_stacks.stacks
    
    # Get the names of the stacks the user has already  
    user_stack_names = []    
    if user_stacks is not None:
        for existing in user_stacks:
            user_stack_names.append(existing.name)
    
    created_stacks =  await STACK_BUILDERS[stack](user.username)
    
    # Verify that the new stack created does not exist already
    for each_stack in created_stacks:
        if each_stack.name in user_stack_names:
            raise HTTPException(
            status.HTTP_409_CONFLICT, detail="That stack already exists"
        )
    
    for each_stack in created_stacks:
        user.stacks.append(each_stack)
    await user.save()
    return created_stacks
   

""" 
GET
"""
async def get_user(id: str):
    """ function takes the MongoDB document _id as a string, to search database.
    """
    found = await User.get(id)
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return found


async def get_users():
    """ function returns all users in the database as a list.
    """
    all_users = await User.find().to_list()
    return all_users

"""
Patch
"""
async def update_user_data( id, user_update_data):
    update_data = user_update_data.dict(exclude_unset=True)
    found_user = await User.get(id)
    
    # duplicate_user =  found_user.copy(update=update_data, exclude={"_id"})
    updated_user = await found_user.update({"$set": update_data})
    
    # # updated_item = user.copy(update=update_data, exclude={"id"})
    # updated_to_json = jsonable_encoder(updated_user)

    # await found_user.set({**updated_to_json})
    return found_user

    # return True


async def delete_user_by_id(id: str):
    """ function takes the MongoDB document _id as a string, to search database
    for document and delete it.
    """
    success_message = Message(message="user deleted")
    user_found = await User.get(id)
    
    if user_found is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    await user_found.delete()
    return success_message
    
    
async def add_avatar_image(user):
    # Upload to Cloudinary
    # file_info = uploadImage(path_to_image)
    user = await User.get(user.id)
    
    await user.save()

    return True

async def add_generic_avatar(user):
    """Function to automatically add a generic avatar on new user create"""

    user = await User.get(user._id)
    user.avatar = "https://api.multiavatar.com/"+user.username+".png"

    await user.save()

    return True

    
    