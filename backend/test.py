import jwt
from fastapi import HTTPException
token = input()
decoded_data = jwt.decode(token, options={"verify_signature": False})
print("Decoded Data:", decoded_data)
