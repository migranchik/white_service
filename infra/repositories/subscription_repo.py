from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.models import SubscriptionBase, SubscriptionStatus


class SubscriptionsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        user_id: int,
        vpn_account_id: int | None,
        duration_days: int,
    ) -> SubscriptionBase:
        now = datetime.now(timezone.utc)  # ⬅️ aware datetime
        expires_at = now + timedelta(days=duration_days)

        sub = SubscriptionBase(
            user_id=user_id,
            vpn_account_id=vpn_account_id,
            expires_at=expires_at,
            status=SubscriptionStatus.ACTIVE,
        )

        self.session.add(sub)
        await self.session.flush()
        return sub

    async def extend(self, subscription: SubscriptionBase, duration_days: int) -> SubscriptionBase:
        now = datetime.now(timezone.utc)

        if subscription.expires_at < now:
            subscription.expires_at = now + timedelta(days=duration_days)
        else:
            subscription.expires_at += timedelta(days=duration_days)

        subscription.status = SubscriptionStatus.ACTIVE
        await self.session.flush()
        return subscription

    async def get_by_user_id(self, user_id: int) -> SubscriptionBase | None:
        result = await self.session.execute(
            select(SubscriptionBase).where(SubscriptionBase.user_id == user_id)
        )
        return result.scalar_one_or_none()