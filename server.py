from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from mongodb.db import init_db
from routes.user_routes import user_router
from routes.admin_routes import admin_router
from routes.token_route import token_route
from routes.public_routes import public_router
from routes.stacks_routes import stack_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(public_router, tags=["public access"])
app.include_router(token_route, tags=["login"])
app.include_router(user_router, prefix="/me", tags=["current user"])
app.include_router(stack_router, prefix="/stacks", tags=["stacks"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])


@app.on_event("startup")
async def connect():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(reload=True, app="server:app")
