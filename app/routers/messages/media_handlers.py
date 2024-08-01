import io
import logging

import aiohttp
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown
from aiogram.utils.chat_action import ChatActionSender

from app.database.requests import db
from app import image_generate
from app import keyboards as kb
from app.states import Generation

logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(Generation.image, F.photo)
async def get_image(message: Message, state: FSMContext) -> None:
    image = io.BytesIO()
    await message.bot.download(file=message.photo[-1].file_id, destination=image)
    await state.update_data(image=image)
    user_data = await state.get_data()
    if user_data.get('type_gen') == 'animation' or user_data.get('type_gen') == 'improve':
        await _generate_image(message, state)
        return
    else:
        await message.answer(f"2️⃣ Шаг: Опишите подробно что вы хотите получить на картинке\n\n"
                             f'Совет:\n{markdown.hblockquote("Подробно опишите то, что должно быть изображено.")}', reply_markup=await kb.cancel())
        await state.set_state(Generation.prompt)


@router.message(Generation.prompt, F.text)
async def get_prompt(message: Message, state: FSMContext) -> None:
    await state.update_data(prompt=message.text)
    await _generate_image(message, state)


@router.message(Generation.image, ~F.image)
async def incorrect_photo(message: Message) -> None:
    await message.answer(text=f'Загрузите изображение',
                         reply_markup=await kb.cancel())


@router.message(Generation.prompt, ~F.text)
async def incorrect_prompt(message: Message) -> None:
    await message.answer(text=f'Вы должны дать подсказку для генератора изображений',
                         reply_markup=await kb.cancel())


async def _generate_image(message: Message, state: FSMContext):
    await message.answer_dice(emoji='🎲')
    await message.answer('Запрос принят! Начинаю творить!\n'
                         'Подождите немного, это займет некоторое время!')

    user_data = await state.get_data()
    image_file = user_data.get('image')
    prompt = user_data.get('prompt')
    type_gen = user_data.get('type_gen')
    logger.info(f"Пользователь: {message.from_user.id} создал запрос на генерацию: {type_gen}")

    await state.clear()
    try:
        async with ChatActionSender.upload_photo(bot=message.bot,
                                                 chat_id=message.chat.id):
            extension = 'jpg'
            match type_gen:
                case 'request':
                    url = await image_generate.generate_image_by_text_prompt(prompt=prompt)
                case 'image_and_request':
                    url = await image_generate.generate_image_by_image(image_file, extension='jpg', prompt=prompt)
                case 'improve':
                    url = await image_generate.universal_upscaler_image(image_file, extension='jpg')
                case 'animation':
                    url = await image_generate.generate_motion_by_image(image_file=image_file, extension='jpg')
                    extension = 'mp4'
            if url:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        result_bytes = await response.read()
                await message.reply_document(
                    document=types.BufferedInputFile(
                        file=result_bytes,
                        filename='Результат.{}'.format(extension)
                    )
                )
                logger.info("Удачная отправка файла пользователю")
    except Exception as e:
        logger.error(f"Ошибка при отправке генерации: {e}")
        await message.answer(
            text=f'К сожалению боту не удалось сгенерировать ваш запрос.', reply_markup=await kb.cancel())
    try:
        await db.add_used_and_daily_generation(message.from_user.id)
    except Exception as e:
        logger.error(f"Ошибка при запросе в базу данных: {e}")




