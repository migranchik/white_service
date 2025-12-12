from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from infra.db.models import PaymentBase, PaymentStatus
from datetime import datetime


class PaymentsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, *, user_id: int, plan_id: int, amount: int) -> PaymentBase:
        payment = PaymentBase(
            user_id=user_id,
            plan_id=plan_id,
            amount=amount,
        )
        self.session.add(payment)
        await self.session.flush()
        # после flush у payment уже есть id
        return payment

    async def get_pending_payment(self, *, user_id: int, plan_id: int) -> PaymentBase | None:
        """
        Вернуть самый свежий платеж со статусом pending
        для конкретного пользователя и тарифа.
        """
        q = (
            select(PaymentBase)
            .where(
                PaymentBase.user_id == user_id,
                PaymentBase.plan_id == plan_id,
                PaymentBase.status == PaymentStatus.PENDING,
            )
            .order_by(PaymentBase.created_at.desc())
            .limit(1)
        )
        res = await self.session.execute(q)
        return res.scalar_one_or_none()

    async def set_confirmation_url(self, payment: PaymentBase, confirmation_url: str):
        payment.confirmation_url = confirmation_url
        await self.session.flush()

    async def set_provider_payment_id(self, payment: PaymentBase, provider_payment_id: str):
        payment.provider_payment_id = provider_payment_id
        await self.session.flush()

    async def mark_success(self, provider_payment_id: str):
        q = select(PaymentBase).where(PaymentBase.provider_payment_id == provider_payment_id)
        res = await self.session.execute(q)
        payment = res.scalar_one_or_none()
        if not payment:
            return None
        payment.status = PaymentStatus.SUCCESS
        payment.paid_at = datetime.utcnow()
        await self.session.flush()
        return payment

    async def mark_failed(self, provider_payment_id: str):
        q = select(PaymentBase).where(PaymentBase.provider_payment_id == provider_payment_id)
        res = await self.session.execute(q)
        payment = res.scalar_one_or_none()
        if not payment:
            return None
        payment.status = PaymentStatus.FAILED
        await self.session.flush()
        return payment
