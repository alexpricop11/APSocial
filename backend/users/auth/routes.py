from database.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from users.auth.schemas import LoginUser, RegisterUser
from users.auth.services import AuthServices

auth = APIRouter(tags=['auth'], prefix='/auth')


@auth.post("/login")
async def login(user: LoginUser, db: AsyncSession = Depends(get_db)):
    auth_services = AuthServices(db)
    return await auth_services.login(user)


@auth.post('/register')
async def register_user(user: RegisterUser, db: AsyncSession = Depends(get_db)):
    auth_services = AuthServices(db)
    return await auth_services.register(user)
