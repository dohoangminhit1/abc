import jwt
from fastapi import HTTPException
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzZW5haGloaSIsImV4cCI6MTc0MjkxNTIwNCwidHlwZSI6ImFjY2VzcyJ9.byOkFTwUtKAe4x6Ek3AXbk4yJYmVeZdYNhJ3pGcBvQw"

decoded_data = jwt.decode(token, options={"verify_signature": False})
print("Decoded Data:", decoded_data)
