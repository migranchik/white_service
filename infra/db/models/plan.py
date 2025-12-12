from ..connection import Base

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)


class PlanBase(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Имя и описание тарифа
    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # цена за период (например, месяц)
    price: Mapped[int] = mapped_column(Integer)

    # длительность подписки в днях
    duration_days: Mapped[int] = mapped_column(Integer, default=30)

    # лимиты, если нужны (можно оставить nullable)
    traffic_limit_gb: Mapped[int | None] = mapped_column(Integer, nullable=True)
    devices_limit: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # есть ли данный тариф в продаже
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # связи
    payments: Mapped[list["PaymentBase"]] = relationship(
        back_populates="plan",
    )
