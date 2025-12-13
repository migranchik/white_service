from ..connection import Base

from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import (
    Integer,
    Numeric,
    ForeignKey,
    DateTime,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ReferralRewardStatus(str, PyEnum):
    PENDING = "pending"      # можно использовать, если ждёшь подтверждение
    CONFIRMED = "confirmed"  # начислено
    CANCELED = "canceled"    # отменено (возврат, chargeback и т.д.)


class ReferralRewardBase(Base):
    __tablename__ = "referral_rewards"

    id: Mapped[int] = mapped_column(primary_key=True)

    # id пригласившего
    referrer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    # тот, кто купил подписку и принёс вознаграждение
    referred_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )
    # id платежа
    payment_id: Mapped[int] = mapped_column(
        ForeignKey("payments.id", ondelete="CASCADE"),
        index=True,
    )

    # сумма вознаграждения
    amount: Mapped[float] = mapped_column(Numeric(20, 2),
                                          default=0)
    status: Mapped[ReferralRewardStatus] = mapped_column(
        Enum(ReferralRewardStatus, name="referral_reward_status"),
        default=ReferralRewardStatus.CONFIRMED,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    referrer: Mapped["UserBase"] = relationship(
        foreign_keys=[referrer_id],
        back_populates="referral_rewards",
    )
    # просто чтобы можно было достать информацию
    referred_user: Mapped["UserBase"] = relationship(
        foreign_keys=[referred_user_id],
        back_populates="rewards_as_referred",
    )
    payment: Mapped["PaymentBase"] = relationship()
