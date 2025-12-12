from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery

from ..keyboards import install_vpn_kb

from core.services import UsersService, VpnAccountService
from infra.db.connection import async_session_maker

router = Router()


devices = {
    "android": {
        "name": "Android",
        "manual": '<b>Для настройки VPN на Android:</b> \n\n'
                  '<b>1. Скачайте Happ из «<a href="https://play.google.com/store/apps/details?id=com.happproxy">Google Play</a>» или «<a href="https://github.com/FlyFrg/Happ_android_update/releases/latest/download/Happ.apk">APK-файл</a>».</b> \n'
                  '2. Нажмите на кнопку ниже, чтобы <b>подключиться в 1 клик!</b> \n\n'
                  'Если автоматическая настройка не сработала, следуйте инструкции: \n'
                  '1. Скопируйте ключ в самом низу данной инструкции, нажав на него \n'
                  '2. Откройте Happ и нажмите кнопку Вставить/Из буфера. \n'
                  '3. Выберите локацию и подключитесь. \n\n'
                  '<i>Если все же возникли проблемы, обратитесь в нашу службу поддержки</i>',
        "url_schema": "happ://add/",
    },
    "ios": {
        "name": "iOS (iPhone)",
        "manual": '<b>Для настройки VPN на Android:</b> \n\n'
                  '<b>1. Скачайте «<a href="https://apps.apple.com/ru/app/happ-proxy-utility-plus/id6746188973">Happ</a>» для России («<a href="https://apps.apple.com/us/app/happ-proxy-utility/id6504287215">Happ</a>» для других регионов)</b> \n'
                  '2. Нажмите на кнопку ниже, чтобы <b>подключиться в 1 клик!</b> \n\n'
                  'Если автоматическая настройка не сработала, следуйте инструкции: \n'
                  '1. Скопируйте ключ в самом низу данной инструкции, нажав на него \n'
                  '2. Откройте Happ и нажмите кнопку Вставить/Из буфера. \n'
                  '3. Выберите локацию и подключитесь. \n\n'
                  '<i>Если все же возникли проблемы, обратитесь в нашу службу поддержки</i>',
        "url_schema": "happ://add/",
    },
    "windows": {
        "name": "Windows",
        "manual": "Инструкция в разработке",
        "url_schema": "flclash://install-config?url=",
    },
    "macos": {
        "name": "MacOS",
        "manual": "Инструкция в разработке",
        "url_schema": "happ://add/",
    },
}

@router.callback_query(F.data.startswith("install_vpn"))
async def install_vpn_start(callback: CallbackQuery):
        await callback.message.answer("Выберите ваше устройство",
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=install_vpn_kb.get_install_vpn_keyboard(devices))

        await callback.answer()


@router.callback_query(F.data.startswith("another_device"))
async def install_vpn_start(callback: CallbackQuery):
        await callback.message.edit_text("Выберите ваше устройство",
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=install_vpn_kb.get_install_vpn_keyboard(devices))

        await callback.answer()


@router.callback_query(F.data.startswith("manual"))
async def get_manual_to_install(callback: CallbackQuery):
        callback_data = callback.data.split('_')
        device_id = callback_data[1]

        async with async_session_maker() as session:
            user_service = UsersService(session)
            user = await user_service.get_user_by_tg_id(callback.from_user.id)

            vpn_account = user.vpn_account

        await callback.message.edit_text(f'{devices[device_id]["manual"]} \n\n'
                                         f'<b>Ваш ключ, копируйте одним нажатием на него</b>👇 \n'
                                         f'<code>{vpn_account.subscription_link}</code>',
                                         parse_mode=ParseMode.HTML,
                                         reply_markup=install_vpn_kb.get_manual_keyboard(url_schema=devices[device_id]["url_schema"],
                                                                                         subscription_link=vpn_account.subscription_link),
                                         disable_web_page_preview=True)

        await callback.answer()
