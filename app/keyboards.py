from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import TELEGRAM_CHANEL_URL



class DaysPriceCallbackData(CallbackData, prefix="days"):
    days: int
    price: float


class TypeGenerationCallbackData(CallbackData, prefix="type_gen"):
    type_gen: str



PRICE_FOR_GENERATIONS = {
    7: 299,
    14: 600,
    31: 1100,
}


async def start_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Начать', callback_data='generation'))
    keyboard.add(InlineKeyboardButton(text='Личный кабинет', callback_data='account'))
    keyboard.adjust(1)
    return keyboard.as_markup()


async def personal_area():
    keyboard = InlineKeyboardBuilder()
    # keyboard.add(InlineKeyboardButton(text='Начать', callback_data='generation'))
    # keyboard.add(InlineKeyboardButton(text='Оставшиеся токены', callback_data='tokens'))
    keyboard.add(InlineKeyboardButton(text='Рассылка сообщения', callback_data='newsletter'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='cancel'))
    keyboard.adjust(1)
    return keyboard.as_markup()


async def generations_menu():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='🌠Создать картинку по запросу', callback_data=TypeGenerationCallbackData(type_gen='request').pack()))
    keyboard.add(InlineKeyboardButton(text='🎧Создать музыкальное произведение', callback_data=TypeGenerationCallbackData(type_gen='music_create').pack()))
    keyboard.add(InlineKeyboardButton(text='👥Изменить своё фото', callback_data=TypeGenerationCallbackData(type_gen='image_and_request').pack()))
    keyboard.add(InlineKeyboardButton(text='🧪Анимировать картинку', callback_data=TypeGenerationCallbackData(type_gen='animation').pack()))
    keyboard.add(InlineKeyboardButton(text='🔮Улучшить качество фото', callback_data=TypeGenerationCallbackData(type_gen='improve').pack()))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='cancel'))
    keyboard.adjust(1)
    return keyboard.as_markup()


async def cancel():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Меню', callback_data='cancel'))
    return keyboard.as_markup()


async def send_newsletter():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Отправить', callback_data='send_newsletter'))
    keyboard.add(InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    return keyboard.as_markup()


async def subscribe():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='✅Подписаться', url=TELEGRAM_CHANEL_URL))
    return keyboard.as_markup()


async def generations():
    keyboard = InlineKeyboardBuilder()
    for days, price in PRICE_FOR_GENERATIONS.items():
        keyboard.button(text=str(days), callback_data=DaysPriceCallbackData(days=days, price=price).pack())
    keyboard.add(InlineKeyboardButton(text='Отменить', callback_data='cancel'))
    keyboard.adjust(2)
    return keyboard.as_markup()
