from fastapi import APIRouter, Depends
from app.auth.utils import decode_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/profile")

def get_profile(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):

    token = credentials.credentials

    payload = decode_token(token)
    username = payload.get("sub")
    return{"username": username}