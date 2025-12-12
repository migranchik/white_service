import asyncio

from sqlalchemy import select, update

from infra.db.connection import async_session_maker
from infra.db.models import WebhookEvent
from core.services.payments_service import PaymentsService


async def process_event(event: WebhookEvent):
    async with async_session_maker() as session:
        service = PaymentsService(session)
        await service.handle_yookassa_webhook(event.payload)
        await session.commit()


async def worker_loop():
    while True:
        async with async_session_maker() as session:
            q = (
                select(WebhookEvent)
                .where(WebhookEvent.processed == False)
                .order_by(WebhookEvent.created_at)
                .limit(1)
            )
            res = await session.execute(q)
            event = res.scalar_one_or_none()

            if not event:
                # ничего нет — немного спим
                await asyncio.sleep(1)
                continue

            # обрабатываем
            await process_event(event)

            # помечаем как обработанный
            await session.execute(
                update(WebhookEvent)
                .where(WebhookEvent.id == event.id)
                .values(processed=True)
            )
            await session.commit()

        # чтобы цикл не ел CPU
        await asyncio.sleep(0.5)


if __name__ == "__main__":
    asyncio.run(worker_loop())
