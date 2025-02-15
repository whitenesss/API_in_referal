import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from src.database import get_db
from src.models.referral_code import ReferralCode
from src.models.user import User
from src.schemas.user import UserResponse, UserCreate
from src.utils import get_password_hash, create_access_token, verify_password, get_current_user, verify_email
from datetime import datetime, timezone

router = APIRouter(tags=["auth"])

@router.post(
    "/register",
    response_model=UserResponse,
    summary="Регистрация нового пользователя"
)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    is_valid = await verify_email(user_data.email)
    if not is_valid:
        raise HTTPException(status_code=400, detail="НЕ коректный Email")
    existing_user = await db.execute(select(User).filter(User.email == user_data.email))
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Email уже зарегистрирован")

    hashed_password = get_password_hash(user_data.password)
    user = User(email=user_data.email, password_hash=hashed_password)

    if user_data.referral_code:
        referral_code = await db.execute(
            select(ReferralCode).filter(
                ReferralCode.code == user_data.referral_code,
                ReferralCode.is_active == True,
                ReferralCode.expiration_date > datetime.now(timezone.utc)
            )
        )
        referral_code = referral_code.scalar_one_or_none()
        if referral_code:
            user.referrer_id = referral_code.user_id
    db.add(user)
    await db.commit()
    return user


@router.post(
    "/token",
    response_model=dict,
    summary="Авторизация пользователя",
    description="Возвращает токен для доступа к защищенным ресурсам"
)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).filter(User.email == form_data.username))
    user = user.scalar()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {
        "access_token": create_access_token({"sub":user.email}),
        "token_type": "bearer"
    }

