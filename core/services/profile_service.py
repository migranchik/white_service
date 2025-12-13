from core.services import UsersService
from infra.repositories.referral_rewards_repo import ReferralRewardsRepository

class ProfileService:
    def __init__(self, session):
        self.users_service = UsersService(session)
        self.referral_repo = ReferralRewardsRepository(session)

    async def get_profile(self, user_tg_id: int):
        user = await self.users_service.get_user_by_tg_id(user_tg_id)
        subscription = user.subscription
        vpn_account = user.vpn_account
        referral_count = await self.users_service.get_referral_stats(user_tg_id)
        referral_stats = await self.referral_repo.get_stats_for_user(user.id)

        return {
            "tg_id": user.tg_id,
            "subscription_link": vpn_account.subscription_link,
            "subscription_status": subscription.status,
            "subscription_expire": subscription.expires_at,
            "balance": user.ref_balance,
            "referrals_count": referral_count,
            "referrals_income": referral_stats["total_amount"],
            "subscription_until": user,
        }