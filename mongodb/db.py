import beanie
import motor
import motor.motor_asyncio

from dotenv import dotenv_values
from models.user_models import User
from models.flashcards_models import UserCardStats, Card

"""Beanie uses a single model to create database models and give responses, so
models have to be imported into the client initialization.
    """

env = dotenv_values(".env")


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient(env["MONGO_URI"])
    await beanie.init_beanie(
        database=client[env["MONGO_DB"]],
        document_models=[User, Card, UserCardStats],
    )
