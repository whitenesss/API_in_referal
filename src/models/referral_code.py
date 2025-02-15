from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from src.database import Base
from sqlalchemy.orm import relationship

from src.models.user import User


class ReferralCode(Base):
    __tablename__ = 'referral_codes'

    id = Column(Integer, primary_key=True, index=True)  # Уникальный ID кода
    code = Column(String, unique=True, index=True)  # Уникальный реферальный код
    user_id = Column(Integer, ForeignKey("users.id"))  # Связь с пользователем
    expiration_date = Column(DateTime(timezone=True))  # Срок годности кода
    is_active = Column(Boolean, default=True)  # Активен ли код

    # Связь с пользователем (владельцем кода)
    user = relationship("User", back_populates="referral_codes")