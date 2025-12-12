from watchfiles import awatch
from yookassa import Payment

from infra.repositories import SubscriptionsRepository, UsersRepository, PlansRepository
from infra.db.models import SubscriptionBase, PaymentBase


class SubscriptionsService:
    def __init__(self, session):
        self.session = session
        self.subscriptions_repo = SubscriptionsRepository(session)
        self.users_repo = UsersRepository(session)
        self.plans_repo = PlansRepository(session)

    async def activate_or_extend(
        self,
        user_id: int,
        vpn_account_id: int | None,
        duration_days: int,
    ) -> SubscriptionBase:

        subscription = await self.subscriptions_repo.get_by_user_id(user_id)
        if subscription is None:
            # создаём новую
            sub = await self.subscriptions_repo.create(
                user_id=user_id,
                vpn_account_id=vpn_account_id,
                duration_days=duration_days,
            )
            await self.session.commit()
            return sub

        # продлеваем
        sub = await self.subscriptions_repo.extend(subscription, duration_days)
        await self.session.commit()
        return sub

    async def apply_success_payment(self, payment: PaymentBase) -> SubscriptionBase | None:
        plan_id = payment.plan_id
        user_id = payment.user_id

        user = await self.users_repo.get_by_id(user_id)
        vpn_account = user.vpn_account
        plan = await self.plans_repo.get_by_id(plan_id)

        subscription = await self.activate_or_extend(
            user_id,
            vpn_account.id,
            plan.duration_days
        )

        return subscription
