from datetime import datetime, timedelta
from uuid import UUID
import random
from fastapi import HTTPException
from passlib.context import CryptContext
from sqlalchemy.future import select

from password_service.functions import send_email
from password_service.hash_password import hash_password
from password_service.schemas import ChangePassword, ResetPassword, ResetPasswordConfirm
from users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PasswordService:
    def __init__(self, db):
        self.db = db

    async def change_password(self, user_id: UUID, password: ChangePassword):
        query = select(User).where(user_id == User.id)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if user is None:
            raise HTTPException(status_code=400, detail="User not found")
        if not pwd_context.verify(password.current_password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect current password")
        if password.current_password == password.new_password:
            raise HTTPException(status_code=400, detail="New password cannot be the same as the current password")
        hashed_password = pwd_context.hash(password.new_password)
        user.password = hashed_password
        await self.db.commit()
        await self.db.refresh(user)

    async def reset_password(self, request: ResetPassword):
        query = select(User).where(request.email == User.email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        reset_code = str(random.randint(100000, 999999))
        user.reset_code = reset_code
        user.reset_code_expiry = datetime.utcnow() + timedelta(minutes=15)
        self.db.commit()
        await send_email(request.email, reset_code)
        return {'message': "The code was sent successfully"}

    async def confirm_reset_password(self, request: ResetPasswordConfirm):
        query = select(User).where(request.email == User.email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user.reset_code != request.reset_code:
            raise HTTPException(status_code=400, detail='The code is not correct')
        if datetime.utcnow() > user.reset_code_expiry:
            raise HTTPException(status_code=400, detail="Expire code")
        user.password = hash_password(request.new_password)
        user.reset_code = None
        user.reset_code_expiry = None
        self.db.commit()
        return {"message": "This password success reset"}
