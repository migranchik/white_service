from datetime import datetime, timedelta

from remnawave.models import (CreateUserRequestDto,
                              UserResponseDto, )

from .client import get_remnawave_client


class RemnawaveGateway:
    def __init__(self) -> None:
        self._client = get_remnawave_client()

    # ---- Пользователь на панели ----
    async def create_panel_user(
        self,
        username
    ) -> UserResponseDto:
        """
        Создаёт юзера в Remnawave, возвращает UUID юзера на панели.
        """
        # примеры имён DTO — подставь реальные
        response = await self._client.users.create_user(
            CreateUserRequestDto(
                username=username,
                status="ACTIVE",
                expire_at=datetime.now() + timedelta(days=7),
                active_internal_squads=["7fda2bf2-b140-468d-92f9-9a143f7c11d0"]
            )
        )
        print(response)
        return response

