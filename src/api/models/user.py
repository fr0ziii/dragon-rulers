from pydantic import BaseModel
from uuid import UUID

ID = "id"
USERNAME = "username"
EMAIL = "email"
CREATED_AT = "created_at"
UPDATED_AT = "updated_at"
PASSWORD = "password"

class User(BaseModel):
    id: UUID
    username: str
    email: str
    created_at: str
    updated_at: str

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        if ID in data:
            data[ID] = str(data[ID])
        return data

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        return data
