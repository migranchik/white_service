from typing import List
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from infra.repositories import PlansRepository
from infra.db.models import PlanBase


class PlansService:
    def __init__(self, session: AsyncSession):
        self.repo = PlansRepository(session)

    async def get_all_active_plans(self) -> list[PlanBase] | None:
        """
        Возвращает все активные тарифные планы
        """
        plans = await self.repo.get_all_plans()
        return plans

    async def get_plan_by_id(self, plan_id: int) -> PlanBase | None:
        """
        Возвращает тарифный план по id
        """
        return await self.repo.get_by_id(plan_id)



