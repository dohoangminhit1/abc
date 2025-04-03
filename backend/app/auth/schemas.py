from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    # refresh_token: str | None = None
    token_type: str = "bearer"

class TokenData(BaseModel):
    token: str | None = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class Revoked_Token(BaseModel):
    token: str
    exp: int

