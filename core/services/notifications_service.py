from bot.bot_instance import bot


class NotificationsService:
    @staticmethod
    async def send_payment_success(
            tg_id: int,
    ):
        text = (
            "Подписка успешно подключена!\n"
            "Для установки нажмите ⚡️Установить VPN⚡️ в главном меню \n\n"
            "Спасибо, что выбираете WhiteVPN 🧡"
        )
        await bot.send_message(chat_id=tg_id, text=text, parse_mode="HTML")

    @staticmethod
    async def send_payment_failed(tg_id: int):
        text = ("❌ Оплата подписки была отменена — возможно, вы забыли оплатить. \n\n"
                "Попробуйте оплатить еще раз или выберите другой тариф. \n\n"
                "<i>Если возникла проблема обратитесь к нам за помощью</i>"
        )
        await bot.send_message(chat_id=tg_id, text=text, parse_mode="HTML")
