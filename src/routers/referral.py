from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from src.database import get_db
from src.models.referral_code import ReferralCode
from src.models.user import User
from src.schemas.referral import ReferralCodeResponse, ReferralCodeCreate, ReferralCodeOnly
from src.schemas.user import UserResponse
from src.utils import get_current_user, generate_unique_code, cache_referral_code, get_cached_referral_code
from sqlalchemy.future import select
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/referral", tags=["referral"])


@router.post(
    "/create_codes",
    response_model=ReferralCodeResponse,
    summary="Создать реферальный код",
    description="Создает новый реферальный код. "
                "У пользователя может быть только один активный код."
                "Пример: expires_in: 10080  # 7 дней в минутах -> Время задается в минутах",
)
async def create_referral_code(
        code_data: ReferralCodeCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    existing_code = await db.execute(
        select(ReferralCode)
        .where(
            ReferralCode.user_id == current_user.id,
            ReferralCode.is_active == True,
        )
    )
    if existing_code.scalar():
        raise HTTPException(400, "У вас уже есть активный код")

    expiration_date = datetime.now(timezone.utc) + timedelta(minutes=code_data.expires_in)
    code = generate_unique_code()

    new_code = ReferralCode(
        code=code,
        user_id=current_user.id,
        expiration_date=expiration_date,
        is_active=True,
    )
    db.add(new_code)
    await db.commit()
    await cache_referral_code(current_user.id, code, code_data.expires_in * 60)
    return new_code


@router.get(
    "/referrals",
    response_model=List[UserResponse],
    summary="список пользователей зарегистрировавшихся по вашему реферальному коду"
)
async def get_referrals(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(User).where(User.referrer_id == current_user.id)
    )
    referrals = result.scalars().all()
    return referrals


@router.get(
    "/codes",
    response_model=ReferralCodeOnly,
    summary="Просмотр активного реферального кода"
)
async def get_active_referral_code(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cached_code = await get_cached_referral_code(current_user.id)
    if cached_code:
        return {"code": cached_code}

    result = await db.execute(
        select(ReferralCode).where(
            ReferralCode.user_id == current_user.id,
            ReferralCode.is_active == True,
            ReferralCode.expiration_date > datetime.now(timezone.utc)
        )
    )
    active_code = result.scalar_one_or_none()
    if active_code is None:
        raise HTTPException(status_code=404, detail="Нет активных кодов")
    return {"code": active_code.code}


@router.delete("/codes/delete", summary="Деактивация кода")
async def delete_referral_code(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(ReferralCode).where(
            ReferralCode.user_id == current_user.id,
            ReferralCode.is_active == True,
            ReferralCode.expiration_date > datetime.now(timezone.utc)
        )
    )
    code = result.scalar_one_or_none()
    if code is None:
        raise HTTPException(status_code=404, detail="Активный реферальный код не найден")

    code.is_active = False
    await db.commit()
    return {"message": "Код деактивирован"}


@router.get(
    "/referral-code/{email}",
    response_model=ReferralCodeOnly,
    summary="Получить реферальный код по email пользователя"

)
async def get_referral_code_by_email(
        email: str,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).filter(User.email == email))
    referrer = result.scalar_one_or_none()
    if referrer is None:
        raise HTTPException(status_code=404, detail="Пользователь с таким email не найден")
    cached_code = await get_cached_referral_code(referrer.id)
    if cached_code:
        return {"code": cached_code}
    result = await db.execute(
        select(ReferralCode).where(
            ReferralCode.user_id == referrer.id,
            ReferralCode.is_active == True,
            ReferralCode.expiration_date > datetime.now(timezone.utc)
        )
    )
    referral_code = result.scalar_one_or_none()
    if referral_code is None:
        raise HTTPException(status_code=404, detail="Активный реферальный код не найден")

    expires_in = int((referral_code.expiration_date - datetime.now(timezone.utc)).total_seconds())
    await cache_referral_code(referrer.id, referral_code.code, expires_in)

    return {"code": referral_code.code}


@router.get(
    "/referrals/{referrer_id}",
    response_model=List[UserResponse],
    summary="Получить список пользователей "
            "зарегистрировавшихся по реферальному "
            "коду от конкретного пользователя по id"
)
async def get_referrals_by_referrer_id(
        referrer_id: int,
        db: AsyncSession = Depends(get_db)
):
    referrer_result = await db.execute(
        select(User).where(User.id == referrer_id)
    )
    referrer = referrer_result.scalar_one_or_none()
    if referrer is None:
        raise HTTPException(status_code=404, detail="Нт тпкого пользователя")
    result = await db.execute(
        select(User).where(User.referrer_id == referrer_id)
    )
    referrals = result.scalars().all()
    if not referrals:
        raise HTTPException(status_code=404, detail="Рефералы отсутствуют")
    return referrals
