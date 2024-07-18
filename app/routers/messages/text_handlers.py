import io
import logging

import aiohttp
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from app import keyboards as kb
from app.states import Generation

logger = logging.getLogger(__name__)

router = Router(name=__name__)


@router.message(Generation.newsletter, F.text)
async def get_prompt(message: Message, state: FSMContext) -> None:
    await state.update_data(newsletter=message.text)
    await message.answer(text=f'Уверены?\n\n'
                              f'Сообщение:\n'
                              f'{message.text}',
                         reply_markup=await kb.send_newsletter())


