from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.utils import decode_token, revoke_jti, is_token_revoked
from app.redis import get_redis

router = APIRouter()
bearer_scheme = HTTPBearer()

@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    try:
        # Lấy token từ HTTPAuthorizationCredentials
        token = credentials.credentials

        # Giải mã token
        access_token_data = decode_token(token)

        # Kiểm tra loại token
        if access_token_data.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type. Access token required.")

        # Thu hồi access token
        access_jti = access_token_data.get("jti")
        access_expiry = access_token_data.get("exp")
        if not access_jti:
            raise HTTPException(status_code=401, detail="Token missing JTI claim")
        if await is_token_revoked(access_jti):
            raise HTTPException(status_code=400, detail="Access token already revoked")
        await revoke_jti(access_jti, access_expiry)

        # Thu hồi refresh token
        username = access_token_data.get("sub")
        redis = get_redis()
        user_key = f"user_refresh:{username}"
        refresh_jti = await redis.get(user_key)
        if refresh_jti:
            await redis.delete(f"refresh:{refresh_jti}")
            await redis.delete(user_key)

        return {"message": "Successfully logged out"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")