from aiogram.utils import markdown

from config import TELEGRAM_CHANEL_URL


MESSAGE_HELP = (f"📄 {markdown.hbold('Руководство:')}\n"
                f"Вам необходимо загрузить изображение, прописать запрос, и ожидать результат🩻\n\n"
                f"Ваш личный кабинет - /account\n"
                f"{markdown.hbold('Порядок действий следующий:')}\n\n"
                f"{markdown.hblockquote('1️⃣ Шаг: Нажать - Генерация изображения')}\n"
                f"{markdown.hblockquote('2️⃣ Шаг: Загрузите изображение')}\n"
                f"{markdown.hblockquote('3️⃣ Шаг: Написать запрос (prompt) для редактирования')}\n"
                f"{markdown.hblockquote('4️⃣ Шаг: Ожидайте пока нейросеть сгенерирует изображение.')}\n(❗️Важно: Генерация изображения составляет около 20 секунд)\n\n")


NOT_SUB_MESSAGE = f"Вам необходимо подписаться на наш канал ({TELEGRAM_CHANEL_URL}), чтобы использовать бота."
