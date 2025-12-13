import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from configs.settings import settings
from bot.handlers.admin import get_admin_router
from bot.bot_instance import bot  # ⬅️ вот он

from bot.handlers import (start,
                          support,
                          profile,
                          profile_settings,
                          referral,
                          install_vpn,
                          plans,
                          pay_plan,
                          unsubscribe)

from bot.commands import user_commands


async def main():
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start.router)
    dp.include_router(support.router)
    dp.include_router(profile.router)
    dp.include_router(install_vpn.router)
    dp.include_router(profile_settings.router)
    dp.include_router(referral.router)
    dp.include_router(plans.router)
    dp.include_router(pay_plan.router)
    dp.include_router(unsubscribe.router)

    dp.include_router(user_commands.router)

    # admin handlers
    dp.include_router(get_admin_router([settings.ADMIN_ID]))


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
