from aiogram import html, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app import keyboards as kb
from app.database.requests import db
from app.filters.user_filters import AvailableGeneration
from app.routers.payment.base_payment import invoice
from app.templates.messages_templates import MESSAGE_HELP
from app.states import Generation

router = Router(name=__name__)


@router.callback_query(F.data == 'generation', ~AvailableGeneration())
async def handler_type_cloth_callback(callback: CallbackQuery) -> None:
    """
    Отрабатывает при недостаточном кол-ве генераций
    :param callback: Callback запрос
    """
    await callback.message.edit_text(f'У вас нет доступных генераций\n'
                                     f'Выберите:', reply_markup=await kb.generations())


@router.callback_query(kb.GenerationAmountCallbackData.filter())
async def buy(callback: CallbackQuery,
              callback_data: kb.GenerationAmountCallbackData,
              state: FSMContext) -> None:
    """
    Отрабатывает на выбор определенного кол-ва генераций при покупке, а также добавляет это количество в кэш
    :param state:
    :param callback: Callback запрос
    :param callback_data: Строка-запроса сформированная для кнопки на клавиатуре
    """
    await callback.message.delete()
    gen_amount = callback_data.gen_amount
    price = callback_data.price
    await state.update_data(gen_amount=gen_amount)
    await invoice(callback, price=price)


@router.callback_query(F.data == 'account')
async def handler_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()

    user_id = callback.from_user.id
    user_data = await db.get_user_data(user_id)
    if user_data:
        await callback.message.edit_text(f'Личный кабинет:\n\n'
                                         f'Имя: {callback.from_user.first_name}\n'
                                         f'ID: {user_id}\n'
                                         f'Доступно генераций: {user_data["available_generations"]}\n'
                                         f'Использовано генераций: {user_data["used_generations"]}\n\n'
                                         f'Купить генерации: /buy\n'
                                         f'Нажмите /start для генерации изображения'
                                         , reply_markup=await kb.cancel())
    else:
        await callback.message.answer(f'Нажмите /start для начала')


@router.callback_query(F.data == 'cancel')
async def handler_cancel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(MESSAGE_HELP, reply_markup=await kb.start_menu())


@router.callback_query(F.data == 'generation')
async def handler_generation_types(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text('Выберите тип генерации:', reply_markup=await kb.generations_menu())


@router.callback_query(kb.TypeGenerationCallbackData.filter(), AvailableGeneration())
async def handler_generation(callback: CallbackQuery,
                             callback_data: kb.TypeGenerationCallbackData,
                             state: FSMContext) -> None:
    """
    Отрабатывает на выбор определенного кол-ва генераций при покупке, а также добавляет это количество в кэш
    :param state:
    :param callback: Callback запрос
    :param callback_data: Строка-запроса сформированная для кнопки на клавиатуре
    """
    type_gen = callback_data.type_gen
    await state.update_data(type_gen=type_gen)

    match type_gen:
        case 'request':
            await callback.message.edit_text(f'1️⃣ Напишите запрос (prompt) для генерации изображения',
                                             reply_markup=await kb.cancel())
            await state.set_state(Generation.prompt)
        case 'image_and_request':
            await callback.message.edit_text(f'1️⃣ Загрузите изображение в формате: png, jpg, jpeg или webp',
                                             reply_markup=await kb.cancel())
            await state.set_state(Generation.image)
        case 'animation':
            await callback.message.edit_text(f'1️⃣ Загрузите изображение в формате: png, jpg, jpeg или webp',
                                             reply_markup=await kb.cancel())
            await state.set_state(Generation.image)




