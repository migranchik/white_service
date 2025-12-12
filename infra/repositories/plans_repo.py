from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from infra.db.models import PlanBase


class PlansRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_plans(self) -> list[PlanBase]:
        statement = select(PlanBase).where(PlanBase.is_active.is_(True))
        result = await self.session.execute(statement)

        return list(result.scalars().all())

    async def get_by_id(self, plan_id: int) -> PlanBase | None:
        statement = select(PlanBase).where(PlanBase.id == plan_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

