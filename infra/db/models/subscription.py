from ..connection import Base
from enum import Enum as PyEnum
from datetime import datetime

from sqlalchemy import ForeignKey, Enum, DateTime
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)


# ENUM для статуса подписки
class SubscriptionStatus(str, PyEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class SubscriptionBase(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(primary_key=True)

    # id пользователя нашего сервиса
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    # id учетной записи впна пользоветеля
    vpn_account_id: Mapped[int | None] = mapped_column(
        ForeignKey("vpn_accounts.id", ondelete="SET NULL"),
        nullable=True,
    )

    # статус подписки из enum
    status: Mapped[SubscriptionStatus] = mapped_column(
        Enum(SubscriptionStatus, name="subscription_status"),
        default=SubscriptionStatus.ACTIVE,
    )

    # дата истечения подписки
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )

    # дата создания подписки
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    # связи
    user: Mapped["UserBase"] = relationship(back_populates="subscription")

