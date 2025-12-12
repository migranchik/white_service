from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from infra.repositories import VpnAccountsRepository
from infra.db.models import VpnAccountBase, UserBase


class VpnAccountService:
    def __init__(self, session: AsyncSession):
        self.repo = VpnAccountsRepository(session)

    async def register_vpn_account(
        self,
        user: UserBase,
        external_id: str | None = None,
        subscription_link: str | None = None,
    ) -> Optional[VpnAccountBase]:
        """
        Возвращает vpn account
        """
        vpn_account = await self.repo.get_by_user_id(user.id)
        if vpn_account:
            return vpn_account


        vpn_account = await self.repo.create_vpn_account(
            user=user,
            external_id=external_id,
            subscription_link=subscription_link,
        )
        return vpn_account




