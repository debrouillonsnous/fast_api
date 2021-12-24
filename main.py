from typing import List
from uuid import UUID, uuid4
from fastapi import FastAPI, HTTPException

from models import Gender, Role, User, UserUpdateRequest

app = FastAPI()

db: List[User] = [
    User(
        id=UUID("3f0d999b-6e0a-4b95-bf3a-f1ba6b5f5e35"),
        first_name="Ousmane",
        last_name="SOW",
        gender=Gender.female,
        roles=[Role.student],
    ),
    User(
        id=UUID("e41816f9-6966-4785-b8ca-5894bdb24880"),
        first_name="Moussa",
        last_name="SOW",
        gender=Gender.male,
        roles=[Role.admin, Role.user],
    ),
]


@app.get("/")
async def root():
    return {"Hello": "hi"}


# get all the users
@app.get("/api/v1/users")
async def get_users():
    return db


@app.post("/api/v1/users")
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404, detail=f"user avec l'ID: {user_id} n'existe pas"
    )


@app.put("/api/v1/users/{user_id}")
async def update_user(user_update: UserUpdateRequest, user_id: UUID):
    for user in db:
        if user.id == user_id:
            if user_update.first_name is not None:
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.last_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404, detail=f"user avec l'ID: {user_id} n'existe pas"
    )
