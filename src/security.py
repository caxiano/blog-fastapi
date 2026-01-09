import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

# Defines the secret key used to sign and verify JWT tokens. Must be kept secret.
SECRET = "my-secret"
# Defines the encryption algorithm to be used in the JWT signature.
ALGORITHM = "HS256"


# Defines a Pydantic model for the structure of the access token's payload.
class AccessToken(BaseModel):
    iss: str  # "iss" (issuer): who issued the token.
    sub: int  # "sub" (subject): the identifier of the user to whom the token belongs.
    aud: str  # "aud" (audience): for whom the token is intended.
    exp: float  # "exp" (expiration time): when the token expires (timestamp).
    iat: float  # "iat" (issued at): when the token was issued (timestamp).
    nbf: float  # "nbf" (not before): the time before which the token is not valid (timestamp).
    jti: str  # "jti" (JWT ID): a unique identifier for the token.


# Defines a Pydantic model for the response object containing the access token.
class JWTToken(BaseModel):
    access_token: AccessToken


# Function to create and sign a new JWT token for a user.
def sign_jwt(user_id: int):
    now = time.time()
    payload = {
        "iss": "fastapi.com.br",
        "sub": str(user_id),
        "aud": "fastapi",
        "exp": now + (60 * 30),  # Sets the expiration to 30 minutes from now.
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = str(jwt.encode(payload, SECRET, algorithm=ALGORITHM))
    return {"access_token": token}

# Asynchronous function to decode and validate a JWT token.
async def decode_jwt(token: str) -> JWTToken | None:
    try:
        decoded_token = jwt.decode(token, SECRET, audience="fastapi", algorithms=[ALGORITHM])
        _token = JWTToken.model_validate({"access_token": decoded_token})
        # Checks if the token has not expired by comparing the expiration time with the current time.
        return _token if _token.access_token.exp >= time.time() else None
    except Exception:
        return None


# Class that inherits from HTTPBearer to customize JWT token verification.
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> JWTToken:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not scheme == "Bearer":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme.")

            payload = await decode_jwt(credentials)
            if not payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token.")
            return payload
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code.")


# Function to get the current user from the token. Used as a FastAPI dependency.
async def get_current_user(token: Annotated[JWTToken, Depends(JWTBearer())]) -> dict[str, int]:
    return {"user_id": token.access_token.sub}


# Dependency function to protect routes that require login.
def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return current_user
