from aiogram.utils import markdown


from config import TELEGRAM_CHANEL_URL

MESSAGE_START = "🤖 Привет, Я твой умный помощник для создания, изменения и анимирования изображений\n\n"\
                 f"{markdown.hbold('Вот что я умею:')} \n"\
                 f"{markdown.hblockquote('- Создавать картинки по вашему запросу 🩵')}\n"\
                 f"{markdown.hblockquote('- Изменять ваши фото и картинки 💚')}\n"\
                 f"{markdown.hblockquote('- Анимировать любые изображения 🤯')}\n"\
                 f"{markdown.hblockquote('- Улучшать качество изображений 🔮')}\n\n"\
                 f"{markdown.hbold('❗️ Важно')}\n\n"\
                 f"{markdown.hblockquote('Советуем Вам писать более подробное описание для изменения вашей картинки, чтобы получить более качественный результат')}\n"\
                 f"/help - помощь\n"


MESSAGE_START_FOR_NEW_USERS = "Здравствуйте!, {name}!\n"\
                f"Хотите получить такой же результат?\n\n"\
                f"{MESSAGE_START}\n"\
                f"Попробуйте загрузить любое изображение и указать что вам нужно  📸\n\n" \
                f"Успехов в создании прекрасного 🎉📸🌟\n\n" \
                              f"/start - начать\n\n"


MESSAGE_HELP = (f"📄 {markdown.hbold('Руководство:')}\n"
                f"Вам необходимо загрузить изображение, прописать запрос, и ожидать результат🩻\n\n"
                f"Ваш личный кабинет - /account\n"
                f"{markdown.hbold('Порядок действий следующий:')}\n\n"
                f"{markdown.hblockquote('1️⃣ Шаг: Нажать - Начать')}\n"
                f"{markdown.hblockquote('2️⃣ Шаг: Загрузите изображение')}\n"
                f"{markdown.hblockquote('3️⃣ Шаг: Написать запрос для редактирования')}\n"
                f"{markdown.hblockquote('4️⃣ Шаг: Ожидайте пока нейросеть сгенерирует изображение.')}\n\n"
                f"❗️Важно: Генерация изображения составляет более 20 секунд\n")


NOT_SUB_MESSAGE = f"Вам необходимо подписаться на наш канал ({TELEGRAM_CHANEL_URL}), чтобы использовать бота."



TEXT_FOR_PROFILE = f'📱 Личный кабинет:\n\n'\
                  'Имя: {name}\n'\
                  'ID: {user_id}\n'\
                  'Подписка: {subscription_end_date}\n'\
                  'Использовано генераций: {used_generations}\n\n'\
                  f'Купить генерации: /buy\n'\
                  f'Нажмите /start для генерации изображения'


TEXT_FOR_ADMINS_PROFILE = f'📱 Личный кабинет админа:\n\n'\
                  'Имя: {name}\n'\
                  'ID: {user_id}\n'\
                  'Количество оставшихся LeonardoAI API токенов: {tokens}\n'\
                  'Получить список пользователей: \n/get_user_list\n'\




