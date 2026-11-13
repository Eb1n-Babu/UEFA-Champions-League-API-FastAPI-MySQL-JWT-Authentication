"""security module"""
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer





SECRET_KEY = "my-secret-key-change-this"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_token(username: str):
    """create jwt token"""
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    data = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    """verify jwt token"""
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError as exc:
        raise HTTPException(status_code=401, detail={"Invalid or expired token": str(exc)}) from exc
