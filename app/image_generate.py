"""
URL: https://docs.leonardo.ai/recipes
"""

import io
import asyncio
import logging
import sys
from typing import Dict

import requests
import json

from app.translator import text_translator
from config import LEONARDO_AI_TOKEN


logger = logging.getLogger(__name__)


api_key = LEONARDO_AI_TOKEN
authorization = "Bearer %s" % api_key
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": authorization
}


async def _generate_motion(payload: Dict) -> str:
    """
    Генерация видео
    :param payload:
    :return: Ссылка на видео
    """
    url = "https://cloud.leonardo.ai/api/rest/v1/generations-motion-svd"
    response = requests.post(url, json=payload, headers=headers)
    logger.info("Получение видео")
    logger.info(response.json())
    generation_id = response.json()['motionSvdGenerationJob']['generationId']
    url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id
    await asyncio.sleep(60)
    response = requests.get(url, headers=headers)
    logger.info(f"Данные видео: {response.json()}")

    image_url = response.json()['generations_by_pk']['generated_images'][0]['motionMP4URL']
    return image_url


async def _generate_image(payload: Dict) -> str:
    """
    :param payload: словарь с полезной нагрузкой
    :return: URL изображения
    """
    url = "https://cloud.leonardo.ai/api/rest/v1/generations"

    response = requests.post(url, json=payload, headers=headers)
    logger.info("Статус генерации изображения: %s" % response.status_code)
    generation_id = response.json()['sdGenerationJob']['generationId']
    url = "https://cloud.leonardo.ai/api/rest/v1/generations/%s" % generation_id
    await asyncio.sleep(20)
    logger.info('Получение генерации изображения')
    response = requests.get(url, headers=headers)
    logger.info(f"Данные изображения: {response.json()}")
    image_url = response.json()['generations_by_pk']['generated_images'][0]['url']
    return image_url


async def _upload_image(image_file: io.BytesIO, extension):
    """
    Загрузка изображения в LeonardoAI
    :param image_file:
    :param extension: png | jpg | jpeg | webp
    :return: id изображения на серверах LeonardoAI
    """

    url = "https://cloud.leonardo.ai/api/rest/v1/init-image"
    payload = {"extension": extension}
    response = requests.post(url, json=payload, headers=headers)    # Получить заранее заданный URL-адрес для загрузки изображения

    # Загрузить изображение по заданному URL-адресу
    fields = json.loads(response.json()['uploadInitImage']['fields'])
    url = response.json()['uploadInitImage']['url']

    # Чтобы получить изображение позже
    image_id = response.json()['uploadInitImage']['id']
    files = {'file': image_file}
    response = requests.post(url, data=fields, files=files)  # Header is not needed
    logger.info("Статус загрузки изображения по заранее указанному URL-адресу: %s" % response.status_code)
    return image_id


async def generate_image_by_image(image_file: io.BytesIO, extension: str, prompt: str) -> str | None:
    """
    Метод Leonardo: Generate with Image to Image Guidance using Uploaded Images
    Url: https://docs.leonardo.ai/reference/creategeneration
    :param image_file: файл
    :param extension: расширение файла
    :param prompt: текстовая подсказка для изображения
    :return: URL изображения
    """
    modelId = "1e60896f-3c26-4296-8ecc-53e2afecc132"

    text = await text_translator(prompt)    # перевод текста
    logger.info(f"Подсказка: {text}")
    if not text:
        return None

    image_id = await _upload_image(image_file, extension)

    payload = {
        "height": 512,
        "modelId": modelId,  # Setting model ID to Leonardo Diffusion XL
        "prompt": text,
        "width": 512,
        "init_image_id": image_id,  # Разрешено только одно изображение
        "init_strength": 0.5,  # Должно быть между 0.1 and 0.9
        "num_images": 1,
        # "presetStyle": 'CREATIVE',
        # "photoRealVersion": "v1",
    }

    url_image = await _generate_image(payload=payload)
    return url_image


async def generate_image_by_text_prompt(prompt: str):
    """
    Метод Leonardo: Generate Images Using Image Prompts
    URL: https://docs.leonardo.ai/reference/creategeneration
    """
    modelId = "b24e16ff-06e3-43eb-8d33-4416c2d75876"  # Leonardo Creative model

    text = await text_translator(prompt)    # перевод текста
    logger.info(f"Подсказка: {text}")
    if not text:
        return None

    payload = {
        "alchemy": True,
        "num_images": 1,
        "height": 512,
        "modelId": modelId,
        "prompt": text,
        "width": 512,
        # "init_strength": 0.5,
        "presetStyle": 'CREATIVE',
        # "photoRealVersion": "v1", - не работает
    }

    url_image = await _generate_image(payload=payload)
    return url_image


async def generate_motion_by_image(image_file: io.BytesIO, extension: str):
    """
    Метод Leonardo: Generate Motion Using Uploaded Images
    url: https://docs.leonardo.ai/docs/generate-motion-using-uploaded-images
    """
    image_id = await _upload_image(image_file, extension)
    logger.info(f'image_id: {image_id}')
    payload = {
        "imageId": image_id,
        "isInitImage": True,
        "motionStrength": 5
    }
    url_motion = await _generate_motion(payload=payload)
    return url_motion



if __name__ == "__main__":
    logging.basicConfig(
        stream=sys.stdout,
        # filename='log.log',
        level=logging.INFO,
        encoding='utf-8',
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%m.%d.%Y',
    )
    IMAGE_FILE = "C://Users/faerf/PycharmProjects/telegram_bot_AI_generation_images/app/workspace/test.jpg"
    with open(IMAGE_FILE, 'rb') as file:
        image_bytes = io.BytesIO(file.read())
        # asyncio.run(generate_image_by_image(file, prompt="Create an image of a bear in sea.", extension='jpg'))
        # asyncio.run(generate_motion_by_image(image_file=image_bytes, extension='jpg'))

        # image_bytes = io.BytesIO(file.read())
        # asyncio.run(generate_image_by_image(file, prompt="Create an image of a bear in sea.", extension='jpg'))

    asyncio.run(generate_image_by_text_prompt(prompt="Создайте образ медведя в облаках. Очень детализировано"))

