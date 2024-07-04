from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TELEGRAM_CHANEL_URL



class GenerationAmountCallbackData(CallbackData, prefix="gen_amount"):
    gen_amount: int
    price: float


class TypeGenerationCallbackData(CallbackData, prefix="type_gen"):
    type_gen: str



PRICE_FOR_GENERATIONS = {
    7: 199,
    14: 400,
    31: 549,
}


async def start_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Генерация', callback_data='generation'))
    keyboard.add(InlineKeyboardButton(text='Личный кабинет', callback_data='account'))
    keyboard.adjust(1)
    return keyboard.as_markup()


async def generations_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Генерация по запросу', callback_data=TypeGenerationCallbackData(type_gen='request').pack()))
    keyboard.add(InlineKeyboardButton(text='Генерация по изображению и запросу', callback_data=TypeGenerationCallbackData(type_gen='image_and_request').pack()))
    keyboard.add(InlineKeyboardButton(text='Генерация анимации', callback_data=TypeGenerationCallbackData(type_gen='animation').pack()))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='cancel'))
    keyboard.adjust(1)
    return keyboard.as_markup()


async def cancel():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    return keyboard.as_markup()


async def subscribe():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='✅Подписаться', url=TELEGRAM_CHANEL_URL))
    return keyboard.as_markup()


async def generations():
    keyboard = InlineKeyboardBuilder()
    for gen, price in PRICE_FOR_GENERATIONS.items():
        keyboard.button(text=str(gen), callback_data=GenerationAmountCallbackData(gen_amount=gen, price=price).pack())
    keyboard.add(InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    keyboard.adjust(2)
    return keyboard.as_markup()
