import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from app import keyboards as kb
from app.database.requests import db
from app.filters.user_filters import Subscribe, Admins
from app.image_generate import get_api_subscription_tokens
from app.routers.payment.base_payment import invoice
from app.templates.messages_templates import TEXT_FOR_PROFILE, MESSAGE_START, TEXT_FOR_ADMINS_PROFILE
from app.states import Generation


logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.callback_query(kb.DaysPriceCallbackData.filter())
async def buy(callback: CallbackQuery,
              callback_data: kb.DaysPriceCallbackData,
              state: FSMContext) -> None:
    """
    Отрабатывает на выбор определенного кол-ва генераций при покупке, а также добавляет это количество в кэш
    :param state:
    :param callback: Callback запрос
    :param callback_data: Строка-запроса сформированная для кнопки на клавиатуре
    """
    await callback.message.delete()
    days = callback_data.days
    price = callback_data.price
    await state.update_data(days=days)
    await invoice(callback, price=price)


@router.callback_query(F.data == 'account', Admins())
async def handler_account(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    tokens = await get_api_subscription_tokens()
    await callback.message.edit_text(TEXT_FOR_ADMINS_PROFILE.format(name=callback.from_user.first_name,

                                                                    user_id=callback.from_user.id,
                                                                    tokens=tokens), reply_markup=await kb.personal_area())
@router.callback_query(F.data == 'account')
async def handler_account(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    user_id = callback.from_user.id
    user_data = await db.get_user_data(user_id)
    if user_data:
        if user_data['subscription_end_date']:
            subscription_end_date = user_data['subscription_end_date'].strftime("%d.%m.%Y %H:%M")
        else:
            subscription_end_date = 'Не оформлена'
        await callback.message.edit_text(TEXT_FOR_PROFILE.format(name=callback.from_user.first_name,
                                                                 user_id=user_id,
                                                                 subscription_end_date=subscription_end_date,
                                                                 used_generations=user_data['used_generations']
                                                                 )
                                         , reply_markup=await kb.cancel())
    else:
        await callback.message.answer(f'Нажмите /start для начала')



@router.callback_query(F.data == 'newsletter', Admins())
async def handler_newsletter(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_text("Напишите ваше сообщение для рассылки:", reply_markup=await kb.cancel())
    await state.set_state(Generation.newsletter)


@router.callback_query(F.data == 'send_newsletter', Admins())
async def handler_send_newsletter(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    user_data = await state.get_data()
    text_newsletter = user_data.get('newsletter')
    await state.clear()

    users = await db.get_user_list()
    count = 0

    for u in users:
        try:
            await callback.message.bot.send_message(chat_id=u.id, text=text_newsletter)
            count += 1
        except Exception as e:
            logger.error(f'Ошибка отправки сообщения пользователю:{u.id} - {e}')
    await callback.message.answer(f'Отправлено {count} сообщений из {len(users)}')



@router.callback_query(F.data == 'cancel')
async def handler_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(MESSAGE_START, reply_markup=await kb.start_menu())


@router.callback_query(F.data == 'generation', Subscribe())
async def handler_generation_types(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text('Что хотите сделать?', reply_markup=await kb.generations_menu())


@router.callback_query(F.data == 'generation', ~Subscribe())
async def handler_type_cloth_callback(callback: CallbackQuery) -> None:
    """
    Отрабатывает при неоформленной подписке
    :param callback: Callback запрос
    """
    await callback.message.edit_text(f'У вас нет доступных генераций', reply_markup=await kb.cancel())


@router.callback_query(kb.TypeGenerationCallbackData.filter(), Subscribe())
async def handler_generation(callback: CallbackQuery,
                             callback_data: kb.TypeGenerationCallbackData,
                             state: FSMContext) -> None:
    """
    Отрабатывает при оформленной подписке
    :param state:
    :param callback: Callback запрос
    :param callback_data: Строка-запроса сформированная для кнопки на клавиатуре
    """
    type_gen = callback_data.type_gen
    await state.update_data(type_gen=type_gen)

    match type_gen:
        case 'request':
            await callback.message.edit_text(f'1️⃣ Напишите ваш запрос (подсказку) для создания изображения:\n\n'
                                             f'Совет:\n{markdown.hblockquote("Подробно опишите то, что должно быть изображено.")}',
                                             reply_markup=await kb.cancel())
            await state.set_state(Generation.prompt)
        case 'image_and_request':
            await callback.message.edit_text(f'1️⃣ Отправь изображение:\n\n'
                                             f'Совет:\n{markdown.hblockquote("Доступные форматы: png, jpg, jpeg или webp")}\n'
                                             f'❗️️Важно:\n{markdown.hblockquote("Я не умею создавать изображения на которых 2 и более человек")}',
                                             reply_markup=await kb.cancel())
            await state.set_state(Generation.image)
        case 'animation':
            await callback.message.edit_text(f'1️⃣ Отправь изображение:\n\n'
                                             f'Совет:\n{markdown.hblockquote("Доступные форматы: png, jpg, jpeg или webp")}'
                                             f'❗️️Важно:\n{markdown.hblockquote("Я не умею создавать изображения на которых 2 и более человек")}',
                                             reply_markup=await kb.cancel())
            await state.set_state(Generation.image)
        case 'improve':
            await callback.message.edit_text(f'1️⃣ Отправь изображение:\n\n'
                                             f'Совет:\n{markdown.hblockquote("Доступные форматы: png, jpg, jpeg или webp")}'
                                             f'❗️️Важно:\n{markdown.hblockquote("Я не умею создавать изображения на которых 2 и более человек")}',
                                             reply_markup=await kb.cancel())
            await state.set_state(Generation.image)
