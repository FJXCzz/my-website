from fastapi import APIRouter
from pydantic import BaseModel,EmailStr
from typing import Union


class userin(BaseModel):
    username:str
    password:str
    email:EmailStr
    full_name:Union[str,None]=None


class userout(BaseModel):
    username:str
    email:EmailStr
    full_name:Union[str,None]=None




app05=APIRouter()

@app05.post("/user",response_model=userout)
async def create_user(user:userin):
    return user


