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


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/users/", response_model=List[UserResponse])
async def get_all_users():
    users = await prisma.user.find_many()
    return users