from typing import Optional

from datetime import datetime, timezone

from sqlalchemy import select, func, update, exists
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from infra.db.models import UserBase, SubscriptionBase


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[UserBase]:
        statement = (select(UserBase)
                     .options(joinedload(UserBase.vpn_account))
                     .where(UserBase.id == user_id))
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_tg_id(self, tg_id: int) -> Optional[UserBase]:
        statement = (
            select(UserBase)
            .options(joinedload(UserBase.vpn_account))
            .options(joinedload(UserBase.subscription))
            .where(UserBase.tg_id == tg_id)
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Optional[UserBase]:
        statement = select(UserBase).where(UserBase.email == email)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def update_email(self, tg_id: int, email: str) -> UserBase | None:
        # обновляем email
        stmt = (
            update(UserBase)
            .where(UserBase.tg_id == tg_id)
            .values(email=email)
            .returning(UserBase)
        )

        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if user is None:
            return None

        await self.session.commit()
        return user

    async def get_by_ref_code(self, ref_code: str) -> Optional[UserBase]:
        statement = select(UserBase).where(UserBase.ref_code == ref_code)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def add_balance(self, user_id: int, amount: int):
        stmt = (
            update(UserBase)
            .where(UserBase.id == user_id)
            .values(balance=UserBase.ref_balance + amount)
        )
        await self.session.execute(stmt)

    async def create_from_telegram(
        self,
        tg_id: int,
        username: str | None,
        ref_code: str | None,
        referrer: UserBase | None = None,
    ) -> UserBase:
        user = UserBase(
            tg_id=tg_id,
            username=username,
            ref_code=ref_code,
            referrer=referrer,
        )
        self.session.add(user)
        await self.session.commit()  # ✅ обязателен
        await self.session.refresh(user)
        await self.session.flush()  # чтобы у user появился id
        return user

    # for admin panel

    async def get_tg_ids_all(self) -> list[int]:
        res = await self.session.execute(select(UserBase.tg_id))
        return [row[0] for row in res.all() if row[0]]

    async def get_tg_ids_active(self) -> list[int]:
        now = datetime.now(timezone.utc)
        q = select(UserBase.tg_id).where(
            exists(
                select(1).where(
                    (SubscriptionBase.user_id == UserBase.id) &
                    (SubscriptionBase.expires_at > now)
                )
             )
        )
        res = await self.session.execute(q)
        return [row[0] for row in res.all() if row[0]]

    async def get_tg_ids_inactive(self) -> list[int]:
        now = datetime.now(timezone.utc)
        q = select(UserBase.tg_id).where(
            ~exists(
                select(1).where(
                    (SubscriptionBase.user_id == UserBase.id) &
                    (SubscriptionBase.expires_at > now)
                )
            )
        )
        res = await self.session.execute(q)
        return [row[0] for row in res.all() if row[0]]
