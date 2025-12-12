from typing import Optional

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from infra.db.models import UserBase


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

    async def get_referrals_count(self, user_id: int) -> int:
        statement = select(func.count(UserBase.id)).where(
            UserBase.referred_by_id == user_id
        )
        result = await self.session.execute(statement)

        return result.scalar_one() or 0