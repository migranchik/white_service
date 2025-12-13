from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infra.db.models.referral_reward import ReferralRewardBase, ReferralRewardStatus


class ReferralRewardsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_payment_id(self, payment_id: int):
        stmt = select(ReferralRewardBase).where(
            ReferralRewardBase.payment_id == payment_id
        )
        return await self.session.scalar(stmt)

    async def create(
        self,
        referrer_id: int,
        referred_user_id: int,
        payment_id: int,
        amount: int,
    ):
        reward = ReferralRewardBase(
            referrer_id=referrer_id,
            referred_user_id=referred_user_id,
            payment_id=payment_id,
            amount=amount,
            status=ReferralRewardStatus.CONFIRMED,
        )
        self.session.add(reward)
        return reward

    async def get_stats_for_user(self, user_id: int):
        stmt = select(ReferralRewardBase).where(
            ReferralRewardBase.referrer_id == user_id,
            ReferralRewardBase.status == ReferralRewardStatus.CONFIRMED,
        )
        res = await self.session.scalars(stmt)
        rewards = res.all()

        total_amount = sum(reward.amount for reward in rewards)
        total_count = len(rewards)

        return {
            "total_amount": total_amount,
            "total_count": total_count,
        }
