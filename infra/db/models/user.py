from ..connection import Base
from datetime import datetime

from sqlalchemy import BigInteger, String, DateTime, ForeignKey, Integer
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)

class UserBase(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Telegram id – делаем уникальным
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    # Telegram username
    username: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # email пользователя
    email: Mapped[str | None] = mapped_column(String(64), nullable=True)

    # реферальный код пользователя
    ref_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)

    # баланс реферальных начислений
    ref_balance: Mapped[int] = mapped_column(Integer, default=0)
    ref_total_earned: Mapped[int] = mapped_column(Integer, default=0)

    # id пригласившего
    referred_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Дата регистрации пользователя в нашем сервисе
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    # связи
    referrer: Mapped["UserBase | None"] = relationship(
        remote_side="UserBase.id",
        back_populates="referrals",
    )
    referrals: Mapped[list["UserBase"]] = relationship(
        back_populates="referrer",
    )
    # все реферальные начисления, где он — реферер
    referral_rewards: Mapped[list["ReferralRewardBase"]] = relationship(
        back_populates="referrer",
        foreign_keys="ReferralRewardBase.referrer_id",
    )
    # награды, которые были начислены за меня как за реферала
    rewards_as_referred: Mapped[list["ReferralRewardBase"]] = relationship(
        back_populates="referred_user",
        foreign_keys="ReferralRewardBase.referred_user_id",
    )


    vpn_account: Mapped["VpnAccountBase"] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    payments: Mapped[list["PaymentBase"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    subscription: Mapped["SubscriptionBase"] = relationship(back_populates="user")

