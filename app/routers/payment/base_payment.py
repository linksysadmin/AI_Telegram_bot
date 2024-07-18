import datetime
import json
from datetime import timedelta

from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice
from aiogram import types, Router, F, html

from app.database.requests import db
from app.templates.messages_templates import TEXT_FOR_PROFILE
from config import PAYMENT_TOKEN

router = Router()


async def invoice(callback, price: float) -> None:
    """
    Метод для отправки счетов. В случае успеха отправленное сообщение возвращается.
    :param callback: Callback запрос
    :param price: Сумма
    """

    await callback.bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='Генерации',
        description='Активация генераций',
        provider_token=PAYMENT_TOKEN,
        currency='rub',
        # is_flexible=False,
        prices=[
            LabeledPrice(label=f'Генерации', amount=100 * int(price)),
        ],
        payload='invoice-payload',
        provider_data=json.dumps(
            {'receipt':
                {'items': [
                    {'description': 'Активация генераций',
                     'quantity': '1',
                     'amount': {
                         'value': str(price),
                         'currency': 'RUB',
                     },
                     'vat_code': 1,
                     }
                ], 'email': 'mail@mail.ru',
                },

            }),
        need_email=False,
        send_email_to_provider=False,
    )


@router.pre_checkout_query(lambda query: True)
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery) -> None:
    """
    Как только пользователь подтвердит свои данные об оплате и доставке,
     Bot API отправляет окончательное подтверждение в форме обновления с полем pre_checkout_query
    :param pre_checkout_query: Уникальный идентификатор запроса, на который необходимо ответить.
    """
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id,
                                                           ok=True)  # Укажите True, если все в порядке (товар есть в наличии и т.п.)
    # и бот готов приступить к оформлению заказа.
    # Используйте False, если есть какие-либо проблемы.


@router.message(F.successful_payment)
async def successful_payment(message: types.Message,
                             state: FSMContext) -> None:
    """
    Метод при успешном платеже.
    Получает основную информацию об успешном платеже и сохраняет запись в базе данных
    """
    user_id = message.from_user.id
    purchase_amount = message.successful_payment.total_amount // 100
    user_data_cache = await state.get_data()
    user_data = await db.get_user_data(message.from_user.id)

    subscription_end_date_actual = user_data['subscription_end_date']
    if subscription_end_date_actual:
        subscription_end_date = subscription_end_date_actual + timedelta(days=user_data_cache['days'])
    else:
        subscription_end_date = datetime.datetime.now() + timedelta(days=user_data_cache['days'])

    await db.subscribe_user(user_id, subscription_end_date)
    await db.add_payment(user_id, purchase_amount, subscription_end_date)
    await message.bot.send_message(message.chat.id,
                                   f"✅ {html.bold('Оформлена подписка до:')}\n"
                                   f"{html.pre(subscription_end_date.strftime('%d.%m.%Y %H:%M'))}\n"
                                   f"/start - начать\n"
                                   f"Успешной генерации 📸🎉!")
