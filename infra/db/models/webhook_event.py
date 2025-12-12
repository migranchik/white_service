from datetime import datetime

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..connection import Base


class WebhookEvent(Base):
    __tablename__ = "webhook_events"

    id: Mapped[int] = mapped_column(primary_key=True)

    # откуда пришёл вебхук (yookassa, ещё что-то потом)
    source: Mapped[str] = mapped_column(String(32), nullable=False)

    # сам payload
    payload: Mapped[dict] = mapped_column(JSONB, nullable=False)

    processed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        index=True,
    )
