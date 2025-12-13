import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.notifications_service import NotificationsService
from core.services.subscriptions_service import SubscriptionsService
from infra.repositories.payments_repo import PaymentsRepository
from infra.repositories.plans_repo import PlansRepository
from infra.repositories.users_repo import UsersRepository
from infra.payment_providers.yookassa_api import YooKassaClient


class PaymentsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.payments_repo = PaymentsRepository(session)
        self.plans_repo = PlansRepository(session)
        self.users_repo = UsersRepository(session)
        self.subscriptions_service = SubscriptionsService(session)
        self.notifications_service = NotificationsService()

    async def create_yookassa_payment_for_plan(self, user_tg_id: int, plan_id: int, email: str):
        # 1. найдём пользователя и план
        user = await self.users_repo.get_by_tg_id(user_tg_id)
        if not user:
            raise ValueError("User not found")

        plan = await self.plans_repo.get_by_id(plan_id)
        if not plan or not plan.is_active:
            raise ValueError("Plan not found or inactive")

        # 2. проверяем, есть ли уже pending-платёж по этому тарифу
        existing_payment = await self.payments_repo.get_pending_payment(
            user_id=user.id,
            plan_id=plan.id,
        )

        if existing_payment and existing_payment.confirmation_url:
            # уже есть неоплаченный платёж — просто возвращаем ссылку
            return existing_payment.confirmation_url

        # 3. создаём локальный платеж в БД
        payment = await self.payments_repo.create_payment(
            user_id=user.id,
            plan_id=plan.id,
            amount=plan.price,
        )

        # 4. создаём платёж в Юкассе
        idem_key = str(uuid.uuid4())
        description = f"Оплата WhiteVPN: {plan.name}, пользователь {user.tg_id}"

        yk_payment = YooKassaClient.create_payment(
            amount_rub=plan.price,
            description=description,
            customer_email=email,
            metadata={
                "payment_id": payment.id,
                "user_id": user.id,
                "plan_id": plan.id,
            },
        )

        # 5. сохраняем provider_payment_id и confirmation_url
        await self.payments_repo.set_provider_payment_id(
            payment,
            provider_payment_id=yk_payment.id,
        )

        confirmation_url = yk_payment.confirmation.confirmation_url
        await self.payments_repo.set_confirmation_url(payment, confirmation_url)

        await self.session.commit()

        # 6. возвращаем ссылку на оплату
        return confirmation_url


    async def handle_yookassa_webhook(self, payload: dict):
        """
        Обработка вебхука Юкассы.
        """
        obj = payload.get("object") or {}
        status = obj.get("status")
        provider_payment_id = obj.get("id")

        if not provider_payment_id:
            return

        if status == "succeeded":
            payment = await self.payments_repo.mark_success(provider_payment_id)
            if not payment:
                await self.session.commit()
                return

            # продляем/создаём подписку
            await self.subscriptions_service.apply_success_payment(payment)

            # достаем данные для уведомления
            user = await self.users_repo.get_by_id(payment.user_id)
            if user:
                await self.notifications_service.send_payment_success(
                    tg_id=user.tg_id
                )
            await self.session.commit()

        elif status in ("canceled", "expired"):
            payment = await self.payments_repo.mark_failed(provider_payment_id)
            plan = await self.plans_repo.get_by_id(payment.plan_id)

            # достаем данные для уведомления
            user = await self.users_repo.get_by_id(payment.user_id)
            if user:
                await self.notifications_service.send_payment_failed(
                    tg_id=user.tg_id,
                    plan=plan
                )

            await self.session.commit()


