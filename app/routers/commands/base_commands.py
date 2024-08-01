import os.path

from aiogram import Router, html
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from app import keyboards as kb
from app.database.requests import db
from app.filters.user_filters import Admins
from app.image_generate import get_api_subscription_tokens
from app.templates.messages_templates import MESSAGE_HELP, TEXT_FOR_PROFILE, MESSAGE_START_FOR_NEW_USERS, MESSAGE_START, \
    TEXT_FOR_ADMINS_PROFILE
from config import MEDIA_DIR

router = Router(name=__name__)

VIDEO = FSInputFile(f'{MEDIA_DIR}/promo.mp4')


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    Метод для обработки команды '/start', для отправки приветственного сообщения.
    Добавляет пользователя в БД, в случае его отсутствия.
    :param message: Сообщение-entity
    :param state: Состояние
    """
    user_id = message.from_user.id

    user_data = await db.get_user_data(user_id=user_id)

    if not user_data:
        name = message.from_user.first_name
        username = message.from_user.username
        await db.add_user(user_id=user_id, name=name, username=username)
        mess = 'Вам доступно 3 генерации\n' \
               '/buy - покупка генераций'
        await message.bot.send_video(chat_id=message.chat.id,
                                         caption=MESSAGE_START_FOR_NEW_USERS.format(name=html.bold(message.from_user.full_name)) + mess,
                                         allow_sending_without_reply=True,
                                         video=VIDEO,
                                         reply_markup=await kb.start_menu(),
                                     )
        # media_group = MediaGroupBuilder(
        #     caption=MESSAGE_START_FOR_NEW_USERS.format(name=html.bold(message.from_user.full_name)) + mess)
        # media_group.add(type='photo', media=FSInputFile(f'{MEDIA_DIR}/original.jpg'))
        # media_group.add(type='photo', media=FSInputFile(f'{MEDIA_DIR}/result.jpg'))
        # await message.bot.send_media_group(user_id, media=media_group.build())
    else:
        await message.bot.send_video(chat_id=message.chat.id,
                                         caption=MESSAGE_START,
                                         allow_sending_without_reply=True,
                                         video=VIDEO,
                                         reply_markup=await kb.start_menu(),
                                     )
    await state.clear()


@router.message(Command('help'))
async def command_help_handler(message: Message, state: FSMContext) -> None:
    """
    Метод для обработки команды '/help', для отправки инструктирующего сообщения.
    :param message: Сообщение-entity
    :param state: Состояние
    """
    await state.clear()
    await message.answer(text=MESSAGE_HELP, reply_markup=await kb.start_menu())


@router.message(Command('buy'))
async def command_buy_handler(message: Message, state: FSMContext) -> None:
    """
    Метод для обработки команды '/buy', для покупки генераций.
    :param message: Сообщение-entity
    :param state: Состояние
    """
    await state.clear()
    await message.answer(f'Выберите платёжный план, который хотите приобрести:\n\n'
                         f'💛1 неделя - 299 руб.\n'
                         f'🩵2 недели - 600 руб.\n'
                         f'❤️Месяц - 1100 руб.\n',
                         reply_markup=await kb.generations())



@router.message(Command('get_user_list'), Admins())
async def command_get_user_list_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    users_sequence = await db.get_user_list()
    users_list = []
    for i, user in enumerate(users_sequence, start=1):
        users_list.append(f'{i}. {user.name} - @{user.username}')

    await message.answer('Список пользователей:\n'
                         '№  |  Имя  |  username   \n\n' + '\n'.join(users_list), reply_markup=await kb.cancel())


@router.message(Command('account'), Admins())
async def command_account_handler(message: Message, state: FSMContext) -> None:
    await state.clear()
    tokens = await get_api_subscription_tokens()
    await message.answer(TEXT_FOR_ADMINS_PROFILE.format(name=message.from_user.first_name,
                                                        user_id=message.from_user.id,
                                                        tokens=tokens), reply_markup=await kb.personal_area())


@router.message(Command('account'))
async def command_account_handler(message: Message, state: FSMContext) -> None:
    """
    Метод для обработки команды '/account'
    :param message: Сообщение-entity
    :param state: Состояние
    """
    await state.clear()

    user_id = message.from_user.id
    user_data = await db.get_user_data(user_id)
    if user_data:
        if user_data['subscription_end_date']:
            subscription_end_date = user_data['subscription_end_date'].strftime("%d.%m.%Y %H:%M")
        else:
            subscription_end_date = 'Не оформлена'
        await message.answer(TEXT_FOR_PROFILE.format(name=message.from_user.first_name,
                                                     user_id=user_id,
                                                     subscription_end_date=subscription_end_date,
                                                     used_generations=user_data['used_generations']))
    else:
        await message.answer(f'Нажмите /start для начала')
