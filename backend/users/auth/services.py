from fastapi import HTTPException
from users.auth.schemas import RegisterUser, LoginUser
from users.models import Users
from sqlalchemy.future import select
from database.database import AsyncSession
from uuid import uuid4
from passlib.context import CryptContext

from users.auth.jwt import create_access_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthServices:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def existing_user(self, username: str):
        query = select(Users).where(username == Users.username)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def register(self, schemas: RegisterUser):
        existing_user = await self.existing_user(schemas.username)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists.")
        try:
            new_user = Users(
                id=uuid4(),
                username=schemas.username,
                password=pwd_context.hash(schemas.password),
                email=schemas.email if schemas.email else None,
                phone_number=schemas.phone_number if schemas.phone_number else None,
                birthday=schemas.birthday if schemas.birthday else None
            )
            self.db.add(new_user)
            await self.db.commit()
            await self.db.refresh(new_user)

            access_token = create_access_token(data={"sub": new_user.username})

            return {
                "message": "User registered successfully",
                "token": access_token,
                "user_id": new_user.id
            }
        except Exception as ex:
            raise HTTPException(status_code=500, detail=f"Failed to register user: {str(ex)}")

    async def login(self, user: LoginUser):
        query = select(Users).where(user.username == Users.username)
        result = await self.db.execute(query)
        db_user = result.scalar_one_or_none()

        if db_user is None or not pwd_context.verify(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid username or password")

        token = create_access_token({"sub": db_user.username})
        return {"access_token": token, "token_type": "bearer"}
