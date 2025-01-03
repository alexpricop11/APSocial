from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from password_service.schemas import ChangePassword, ResetPassword
from password_service.service import PasswordService
from users.auth.jwt import get_current_user
from users.models import User

password = APIRouter(tags=['password'], prefix='/auth')


@password.put('/change-password')
async def change_password(pass_data: ChangePassword,
                          current_user: User = Depends(get_current_user),
                          db: AsyncSession = Depends(get_db)):
    try:
        service = PasswordService(db)
        return await service.change_password(current_user.id, pass_data)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f'{str(ex)}')


@password.post('/reset-password')
async def reset_password(request: ResetPassword, db: AsyncSession = Depends(get_db)):
    service = PasswordService(db)
    return await service.reset_password(request)


@password.post('/confirm-reset-password')
async def confirm_reset_password(request: ResetPassword, db: AsyncSession = Depends(get_db)):
    service = PasswordService(db)
    return await service.confirm_reset_password(request)
