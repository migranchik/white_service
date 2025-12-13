from aiogram import Router
from bot.middlewares.admin_only import AdminOnly
from bot.handlers.admin.broadcast import admin_broadcast_router

def get_admin_router(admin_ids: list[int]) -> Router:
    r = Router()
    r.include_router(admin_broadcast_router)
    r.message.filter(AdminOnly(admin_ids))
    r.callback_query.filter(AdminOnly(admin_ids))
    return r
