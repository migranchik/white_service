from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery

from configs.settings import settings
from core.services import UsersService, VpnAccountService, SubscriptionsService
from infra.db.connection import async_session_maker
from infra.vpn_panel.remnwave_gateway import RemnawaveGateway
from ..keyboards import main_menu_reply_button, main_menu_kb, subscribe_kb
from ..utils.ref_code_creator import RefCodeCreator
from ..utils.sub_link_creator import SubLinkCreator
from ..bot_instance import bot

router = Router()
remnawave_gateway = RemnawaveGateway()

async def is_subscribed(service_bot, user_id: int) -> bool:
    try:
        member = await service_bot.get_chat_member(chat_id=settings.CHANNEL_ID, user_id=user_id)
        return member.status in ("member", "administrator", "creator")
    except TelegramBadRequest:
        # например бот не админ/не видит участников/не тот chat_id
        return False


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    text = message.text or ""
    parts = text.split(maxsplit=1)
    ref_payload = parts[1] if len(parts) == 2 else None

    async with async_session_maker() as session:
        user_service = UsersService(session)
        vpn_account_service = VpnAccountService(session)
        subscriptions_service = SubscriptionsService(session)

        user, is_new = await user_service.register_user(
            tg_id=message.from_user.id,
            username=message.from_user.username,
            ref_code=RefCodeCreator.create(message.from_user.id),
            raw_ref_payload=ref_payload,
        )

    if is_new:
        # 👋 новый пользователь
        if message.from_user.username:
            remnawave_user = await remnawave_gateway.create_panel_user(username=message.from_user.username)
        else:
            remnawave_user = await remnawave_gateway.create_panel_user(username=f"tgid{message.from_user.id}")


        vpn_account = await vpn_account_service.register_vpn_account(
            user=user,
            external_id=str(remnawave_user.uuid),
            subscription_link=SubLinkCreator.create(remnawave_user.short_uuid),
        )

        await subscriptions_service.activate_or_extend(
            user_id=user.id,
            vpn_account=vpn_account,
            duration_days=7
        )

        if user.referred_by_id:
            await message.answer(
                "Привет! Ты успешно зарегистрировался по реферальной ссылке 🎉 Подарок от нас — 7 дней <b>PREMIUM</b> подписки\n",
                parse_mode=ParseMode.HTML,
            )
        else:
            await message.answer(
                "Привет! 👋\n\n"
                "Добро пожаловать в WhiteVPN. Мы уже выдали тебе 7 дней <b>PREMIUM</b> подписки\n",
                parse_mode=ParseMode.HTML,
            )

    if not await is_subscribed(bot, message.from_user.id):
        await message.answer(
            "Чтобы начать пользоваться нашим сервисом, нужно быть подписанным на канал 👇\n\n"
            "Подпишись и нажми «Проверить подписку».",
            reply_markup=subscribe_kb.get_subscribe_keyboard(settings.CHANNEL_URL)
        )
        return

    await message.answer("⚡️",
                         reply_markup=main_menu_reply_button.main_menu_reply_button)

    await message.answer("🐝 Меню",
                         reply_markup=main_menu_kb.main_menu_keyboard)


@router.message(F.text == 'Главное меню')
async def main_menu_from_text_keyboard(message: types.Message):
    if not await is_subscribed(bot, message.from_user.id):
        await message.answer(
            "Чтобы начать пользоваться нашим сервисом, нужно быть подписанным на канал 👇\n\n"
            "Подпишись и нажми «Проверить подписку».",
            reply_markup=subscribe_kb.get_subscribe_keyboard(settings.CHANNEL_URL)
        )
        return
    await message.answer("⚡️")
    await message.answer("🐝 Меню",
                         reply_markup=main_menu_kb.main_menu_keyboard)


@router.callback_query(F.data.startswith("back_to_main_menu"))
async def back_to_mai_menu(callback: CallbackQuery):
    msg = callback.message
    await msg.delete()
    if not await is_subscribed(bot, callback.from_user.id):
        await msg.answer(
            "Чтобы начать пользоваться нашим сервисом, нужно быть подписанным на канал 👇\n\n"
            "Подпишись и нажми «Проверить подписку».",
            reply_markup=subscribe_kb.get_subscribe_keyboard(settings.CHANNEL_URL)
        )
        return

    await msg.answer("🐝 Меню",
                         reply_markup=main_menu_kb.main_menu_keyboard)

    await callback.answer()


@router.callback_query(F.data.startswith("check_sub"))
async def check_subscription(callback: CallbackQuery):
    if await is_subscribed(bot, callback.from_user.id):
        await callback.message.edit_text("✅ Подписка подтверждена! Ниже упрощенное и удобное меню")
        await callback.message.answer("⚡️")
        await callback.message.answer("🐝 Меню",
                                      reply_markup=main_menu_kb.main_menu_keyboard)
        await callback.answer()
        return

    await callback.answer("Пока не вижу подписку. Подпишись и попробуй ещё раз.", show_alert=True)