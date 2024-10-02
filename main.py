from fastapi import FastAPI
from prisma import Prisma
from typing import List
from pydantic import BaseModel

app = FastAPI()
prisma = Prisma()

@app.on_event("startup")
async def startup():
    await prisma.connect()

@app.on_event("shutdown")
async def shutdown():
    await prisma.disconnect()

class UserResponse(BaseModel):
    id: int
    email: str
    
class UserCreate(BaseModel):
    email: str
    password: str


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/", response_model=List[UserResponse])
async def get_all_users():
    users = await prisma.user.find_many()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int):
    user = await prisma.user.find_unique(where={"id": user_id})
    return user

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    created_user = await prisma.user.create(data=user.model_dump())
    return created_user
