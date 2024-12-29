from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.future import select

from database.database import AsyncSession, get_db
from settings.settings import SECRET_KEY, ALGORITHM
from users.models import Users


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, refresh_token: bool = False):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            if refresh_token:
                return create_access_token(data={"sub": payload["sub"]})
            else:
                raise HTTPException(status_code=401, detail="Token expired and refresh is not allowed")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or corrupted token")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_token(token, refresh_token=True)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token does not contain username")

        query = select(Users).where(username == Users.username)
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        new_token = None
        if datetime.utcnow() > datetime.utcfromtimestamp(payload["exp"]):
            new_token = create_access_token(data={"sub": username})

        return {"user": user, "new_token": new_token} if new_token else user

    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
