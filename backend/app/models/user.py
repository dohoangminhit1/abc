from pydantic import BaseModel, Field

class LoginCredentials(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)

    class Config:
        json_schema_extra = {
            "example": {
                "username": "poweruser",
                "password": "strongpassword123"
            }
        }

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=0, le=150)
    que: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Truong Tuan Tu",
                "age": 30,
                "que": "Hai Phong"
            }
        }
