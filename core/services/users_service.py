from typing import Tuple, Any, Coroutine
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from infra.repositories import UsersRepository
from infra.db.models import UserBase


@dataclass
class ReferralStats:
    user: UserBase
    total_referrals: int
    balance: int
    total_earned: int

class UsersService:
    def __init__(self, session: AsyncSession):
        self.repo = UsersRepository(session)

    async def register_user(
        self,
        tg_id: int,
        username: str | None,
        ref_code: str | None,
        raw_ref_payload: str | None,
    ) -> Tuple[UserBase, bool]:
        """
        Возвращает (user, is_new)
        """
        user = await self.repo.get_by_tg_id(tg_id)
        if user:
            return user, False

        referrer_user: UserBase | None = None
        if raw_ref_payload:
            referrer_code = raw_ref_payload.strip()
            referrer_user = await self.repo.get_by_ref_code(referrer_code)

            if referrer_user and referrer_user.tg_id == tg_id:
                referrer_user = None

        user = await self.repo.create_from_telegram(
            tg_id=tg_id,
            username=username,
            ref_code=ref_code,
            referrer=referrer_user
        )
        return user, True

    async def get_user_by_tg_id(self, tg_id: int) -> UserBase | None:
        """
        Возвращает пользователя по Telegram ID
        """
        user = await self.repo.get_by_tg_id(tg_id)
        return user

    async def get_ref_code(self, tg_id : int) -> InstrumentedAttribute[str] | None:
        """
        Возвращает ref_code пользователя
        """
        user = await self.repo.get_by_tg_id(tg_id)

        if user:
            return user.ref_code
        return None

    async def get_referral_stats(self, tg_id: int) -> ReferralStats:
        user = await self.repo.get_by_tg_id(tg_id)
        if not user:
            raise ValueError("User not found")  # или создай, как у тебя задумано
        total_referrals = await self.repo.get_referrals_count(user.id)

        return ReferralStats(
            user=user,
            total_referrals=total_referrals,
            balance=user.ref_balance,
            total_earned=user.ref_total_earned,
        )

    async def get_email(self, tg_id: int) -> InstrumentedAttribute[str] | None:
        user = await self.repo.get_by_tg_id(tg_id)
        return user.email

    async def set_email(self, tg_id: int, new_email: str) -> None:
        return await self.repo.update_email(tg_id, new_email)


    async def check_existing_user_by_email(self, email: str) -> UserBase | None:
        user = await self.repo.get_by_email(email)
        if user:
            return user
        return None



