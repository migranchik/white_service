from ..connection import Base
from datetime import datetime

from sqlalchemy import ForeignKey, String, Boolean, Text, DateTime
from sqlalchemy.orm import (Mapped,
                            mapped_column,
                            relationship)


class VpnAccountBase(Base):
    __tablename__ = "vpn_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        index=True,
    )

    # ID пользователя в XRAY/панели (uuid, email, что угодно)
    external_id: Mapped[str] = mapped_column(String(128), unique=True)

    # можешь хранить готовый конфиг или ссылку на него
    subscription_link: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow,
    )

    user: Mapped["UserBase"] = relationship(back_populates="vpn_account")