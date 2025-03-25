# backend/app/user.py
from pydantic import BaseModel, Field

class LoginCredentials(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "poweruser",
                "password": "strongpassword123"
            }
        }

class UserOut(BaseModel):
    username: str
