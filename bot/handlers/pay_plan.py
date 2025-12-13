from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from infra.db.connection import async_session_maker
from core.services import PlansService, PaymentsService, UsersService

from ..states.email_states import EmailStates
from ..utils.validators import validate_email

from ..keyboards import pay_plan_kb

router = Router()


@router.callback_query(F.data.startswith("choose_plan_"))
async def profile_menu(callback: CallbackQuery, state: FSMContext):
    plan_id = int(callback.data.split("_")[2])
    await state.update_data(plan_id=plan_id)

    async with async_session_maker() as session:
        user_service = UsersService(session)
        email = await user_service.get_email(callback.from_user.id)
        if email is None:
            await callback.message.answer("Отправьте ваш Email, туда мы пришлем чек")
            await state.set_state(EmailStates.send_email)
            await callback.answer()
            return

    async with async_session_maker() as session:
        payment_service = PaymentsService(session)

        confirmation_url = await payment_service.create_yookassa_payment_for_plan(
            user_tg_id=callback.from_user.id,
            plan_id=plan_id,
            email=email,
        )

    await callback.message.answer("🐝Спасибо, что выбираете нас! \n"
                                  "Оплачивая подписку Premium, вы соглашаетесь с <a href='https://telegra.ph/Publichnaya-oferta-na-okazanie-uslug-12-13-4'>оферотой</a>",
                                  reply_markup=pay_plan_kb.get_payment_button(confirmation_url))


    await callback.answer()


@router.message(EmailStates.send_email)
async def get_user_email(message: Message, state: FSMContext):
    email = message.text.strip()
    async with async_session_maker() as session:
        user_service = UsersService(session)
        email_is_exist = await user_service.check_existing_user_by_email(email)

    if not validate_email(email):
        await message.answer("Введите свой Email в правильном формате, пожалуйста!")
        return

    if email_is_exist:
        await message.answer("Данный Email уже привязан к другому аккаунту!")
        return

    async with async_session_maker() as session:
        user_service = UsersService(session)
        user = await user_service.set_email(message.from_user.id, email)

    data = await state.get_data()
    plan_id = data["plan_id"]

    async with async_session_maker() as session:
        payment_service = PaymentsService(session)

        confirmation_url = await payment_service.create_yookassa_payment_for_plan(
            user_tg_id=message.from_user.id,
            plan_id=plan_id,
            email=email,
        )

    await message.answer("🐝Спасибо, что выбираете нас! \n"
                         "Оплачивая подписку Premium, вы соглашаетесь с <a href='https://telegra.ph/Publichnaya-oferta-na-okazanie-uslug-12-13-4'>оферотой</a>",
                         reply_markup=pay_plan_kb.get_payment_button(confirmation_url),
                         parse_mode=ParseMode.HTML)

    await state.clear()