import sqlalchemy as sa
from fastapi import APIRouter, Request

from infra.db.connection import async_session_maker
from infra.db.models import WebhookEvent

router = APIRouter(
    prefix="/webhook",
    tags=["webhooks"],
)


@router.post("/yookassa")
async def yookassa_webhook(request: Request):
    payload = await request.json()

    async with async_session_maker() as session:
        await session.execute(
            sa.insert(WebhookEvent).values(
                source="yookassa",
                payload=payload,
            )
        )
        await session.commit()

    return {"status": "queued"}
