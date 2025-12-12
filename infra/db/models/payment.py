from ..connection import Base
from enum import Enum as PyEnum
from datetime import datetime

from sqlalchemy import ForeignKey, String, Enum, Integer, DateTime
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)


# enums для статуса платежа
class PaymentStatus(str, PyEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"


# enums для провайдеров платежей
class PaymentProvider(str, PyEnum):
    YOOKASSA = "yookassa"
    CRYPTOPAY = "cryptopay"
    ANYPAY = "anypay"


class PaymentBase(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)

    # id пользователя сервиса
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    # id тарифного плана который оплачивается
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id"),
        index=True,
    )

    confirmation_url: Mapped[str | None] = mapped_column(
        String(128),
        index=True,
    )

    # провайдер платежа
    provider: Mapped[PaymentProvider] = mapped_column(
        Enum(PaymentProvider, name="payment_provider"),
        default=PaymentProvider.YOOKASSA,
    )
    # статус платежа
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status"),
        default=PaymentStatus.PENDING,
        index=True,
    )
    # Сумма и валюта платежа
    amount: Mapped[int] = mapped_column(Integer)
    currency: Mapped[str] = mapped_column(String(8), default="RUB")

    # ID платежа у провайдера
    provider_payment_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )

    # время создания платежа
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )
    # время оплаты
    paid_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    user: Mapped["UserBase"] = relationship(back_populates="payments")
    plan: Mapped["PlanBase"] = relationship(back_populates="payments")