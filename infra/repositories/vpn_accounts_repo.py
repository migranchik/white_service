from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.models import VpnAccountBase, UserBase


class VpnAccountsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_id(self, user_id: int) -> Optional[VpnAccountBase]:
        statement = select(VpnAccountBase).where(VpnAccountBase.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def create_vpn_account(
        self,
        user: UserBase,
        external_id : str | None = None,
        subscription_link : str | None = None,
    ) -> VpnAccountBase:
        vpn_account = VpnAccountBase(
            user=user,
            external_id=external_id,
            subscription_link=subscription_link,
        )
        self.session.add(vpn_account)
        await self.session.commit()  # ✅ обязателен
        await self.session.refresh(vpn_account)
        await self.session.flush()  # чтобы у user появился id
        return vpn_account
