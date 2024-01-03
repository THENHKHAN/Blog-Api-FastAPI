
# response_model

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    full_name: str | None = None


class UserOut(BaseModel):
    username: str
    full_name: str | None = None


@app.post("/user/", response_model=UserOut) # this will get priortity : Go read FastAPi Google Sheet my Docs
async def create_user(user: UserIn) :
    return user
