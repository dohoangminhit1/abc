from fastapi import APIRouter, HTTPException
from app.auth.utils import decode_token, is_token_revoked, create_access_token, create_refresh_token
from app.redis import get_redis
from jose import jwt

router = APIRouter()

@router.post("/refresh")
async def refresh(refresh_token: str):
    try:
        payload = decode_token(refresh_token)

        # Kiểm tra loại token
        if payload["type"] != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type. Refresh token required.")

        # Kiểm tra JTI
        jti = payload.get("jti")
        if not jti:
            raise HTTPException(status_code=401, detail="Token missing JTI claim")

        # Kiểm tra refresh token trong Redis
        redis = get_redis()
        stored_token = await redis.get(f"refresh:{jti}")
        if not stored_token or stored_token != refresh_token:
            raise HTTPException(status_code=401, detail="Token mismatch or revoked refresh token.")

        # Thu hồi refresh token cũ
        await redis.delete(f"refresh:{jti}")

        # Tạo access token và refresh token mới
        new_access_token = create_access_token(data={"sub": payload["sub"]})
        new_refresh_token = await create_refresh_token(data={"sub": payload["sub"]})

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "message": "Access token refreshed successfully"
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired.")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")