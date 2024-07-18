import datetime
import logging

from aiogram.filters import Filter
from aiogram.types import Message

from config import ADMIN_LIST
from app.database.requests import db


class Subscribe(Filter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id

        user_data = await db.get_user_data(user_id)
        used_generations = user_data.get('used_generations')
        subscription_end_date = user_data.get('subscription_end_date')

        if used_generations < 3 or user_id in ADMIN_LIST:
            logging.info(f'user: {user_id} | used_generations: {used_generations}')
            return True
        if subscription_end_date is None or subscription_end_date < datetime.datetime.now():
            logging.info(f'subscription_end_date: {subscription_end_date}')
            return False
        elif user_data.get('daily_generation') > 20:
            return False
        elif subscription_end_date > datetime.datetime.now():
            return True



class Admins(Filter):
    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        if user_id in ADMIN_LIST:
            return True


