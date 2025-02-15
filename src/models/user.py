from src.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)  # Уникальный ID пользователя
    email = Column(String, unique=True, index=True)  # Уникальный email
    password_hash = Column(String)  # Хеш пароля
    is_active = Column(Boolean, default=True)  # Активен ли пользователь
    created_at = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))  # Дата регистрации

    # Связь с реферером (кто пригласил)
    referrer_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Связь с рефералами (кого пригласил)
    referrals = relationship(
        "User",  # Ссылка на ту же таблицу
        back_populates="referrer",  # Обратная связь
        remote_side=[id]  # Указываем, что это самоссылающаяся связь
    )

    # Связь с реферальными кодами
    referral_codes = relationship("ReferralCode", back_populates="user")

    # Обратная связь для реферера
    referrer = relationship(
        "User",  # Ссылка на ту же таблицу
        back_populates="referrals",  # Обратная связь
    )