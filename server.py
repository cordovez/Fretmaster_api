from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from mongodb.db import init_db
from routes.user_routes import user_route
from routes.admin_routes import admin_router
from routes.token_route import token_route
from routes.public_routes import public_route


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


app.include_router(public_route, tags=["public access"])
app.include_router(user_route, prefix="/me", tags=["current user"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(token_route, tags=["login"])


@app.on_event("startup")
async def connect():
    await init_db()


if __name__ == "__main__":
    uvicorn.run(reload=True, app="server:app")
