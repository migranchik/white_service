from bot.bot_instance import bot
from infra.db.models import PlanBase


class NotificationsService:
    @staticmethod
    async def send_payment_success(
            tg_id: int,
            plan: PlanBase,
    ):
        text = (
            f"Подписка <code>{plan.description}</code> успешно подключена! С деталями можете ознакомиться в Профиле\n"
            f"Для установки нажмите ⚡️Установить VPN⚡️ в главном меню \n\n"
            f"Спасибо, что выбираете WhiteVPN 🧡"
        )
        await bot.send_message(chat_id=tg_id, text=text, parse_mode="HTML")

    @staticmethod
    async def send_payment_failed(tg_id: int, plan: PlanBase):
        text = (f"❌ Оплата подписки Premium <code>{plan.description}</code> была отменена — возможно, вы забыли оплатить. \n\n"
                f"Попробуйте оплатить еще раз или выберите другой тариф. \n\n"
                f"<i>Если возникла проблема обратитесь к нам за помощью</i>"
        )
        await bot.send_message(chat_id=tg_id, text=text, parse_mode="HTML")
