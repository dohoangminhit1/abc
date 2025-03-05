from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., ge=0, le=150)
    que: str = Field(..., min_length=1)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Truong Tuan Tu",
                "age": 29,
                "que": "Hai Phong"
            }
        }