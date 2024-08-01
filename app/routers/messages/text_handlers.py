import logging

from aiogram import Router, F
from aiogram.client.session import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.utils.chat_action import ChatActionSender

from app import keyboards as kb
from app.database.requests import db
from app.music_generate import generate
from app.states import Generation, GenerationMusic

logger = logging.getLogger(__name__)
router = Router(name=__name__)


@router.message(Generation.newsletter)
async def get_prompt(message: Message, state: FSMContext) -> None:
    await state.update_data(message_id=message.message_id)
    await message.answer(text=f'Уверены?\n\n', reply_markup=await kb.send_newsletter())


@router.message(F.text, GenerationMusic.lyric)
async def get_lyric(message: Message, state: FSMContext):
    """ User adds his lyrics """
    await state.set_data({'lyric': message.text})
    await state.set_state(GenerationMusic.tag)
    await message.reply(
        text="🎵Теперь добавьте пожелания в звучании🎵\n\nНапример: <b>тяжелый рок, мужской голос</b>" \
             "<blockquote>Для лучшего соответствия вашим ожиданиям описывайте жанр песни, ее настроение, какие инструменты играют</blockquote>" \
             "<blockquote>❗️Старайтесь не использовать в запросе конкретных исполнителей и их песни</blockquote>",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text='Отмена', callback_data='cancel')
        ]]))


@router.message(F.text, GenerationMusic.tag)
async def get_tag_n_generate(message: Message, state: FSMContext):
    """
    User adds his prompts and waits until he earns audio.
    """

    await message.answer_dice('🎲')
    data = await state.get_data()
    logger.info(f"Пользователь: {message.from_user.id} создал запрос на генерацию музыки")

    await state.clear()
    try:
        await message.answer(
            text=
            'Ваш запрос получен, песня генерируется, подождите пожалуйста. Это может занять некоторое время.'
        )

        async with ChatActionSender.record_voice(bot=message.bot,
                                                 chat_id=message.chat.id):
            link = await generate(data['lyric'], message.text)
            async with aiohttp.ClientSession() as session:
                async with session.get(link[0]) as response:
                    result_bytes = await response.read()
                    await message.reply_document(document=BufferedInputFile(
                        file=result_bytes, filename='music.mp3'))
                await message.answer(
                    text=
                    "<b>Сейчас отправим второй вариант, пока ждете, можете послушать первый🎧</b>"
                )
                async with session.get(link[1]) as response:
                    result_bytes = await response.read()
                    await message.reply_document(document=BufferedInputFile(
                        file=result_bytes, filename='music.mp3'))
    except Exception as e:
        logger.error(f"Ошибка при отправке генерации: {e}")
        await message.answer(
            text=f'Ваш трек настолько крут 🤟, что нейросеть Аврора впала в анабиоз 😔\n'
                 f'Попробуйте произвести генерацию снова 😜', reply_markup=await kb.cancel())
    try:
        await db.add_used_and_daily_generation(message.from_user.id)
    except Exception as e:
        logger.error(f"Ошибка при запросе в базу данных: {e}")
