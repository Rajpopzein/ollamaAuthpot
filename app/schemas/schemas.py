from typing import Any

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class APIKeyBase(BaseModel):
    key: str
    user_id: int

class APIKeyCreate(APIKeyBase):
    pass

class APIKey(APIKeyBase):
    id: int

    class Config:
        orm_mode = True

class ModelBase(BaseModel):
    name: str

class ModelCreate(ModelBase):
    pass

class Model(ModelBase):
    id: int

    class Config:
        orm_mode = True

class APIKeyRequest(BaseModel):
    username: str

class APIKeyResponse(BaseModel):
    api_key: str

class ChatRequest(BaseModel):
    prompt: str
    model: str

class ChatResponse(BaseModel):
    response: Any
