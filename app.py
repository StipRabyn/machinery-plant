import threading
import asyncio
import aioschedule as schedule
from loguru import logger
from vk_bot import bot
from machines import machine_units
from config import (
    SECRET_KEY,
    CONFIRMATION_TOKEN)
from fastapi import (
    FastAPI,
    Request,
    Response,
    BackgroundTasks)


# инициализация сервера
app = FastAPI()


# запуск стартап-функции
@app.on_event("startup")
async def startup_function():
    logger.info("Setup server...")

    await bot.setup_webhook()


# обработчик POST-запросов
@app.post("/")
async def connection(req: Request, background_task: BackgroundTasks):
    event = await req.json()

    if "type" not in event.keys():
        logger.info("Empty request!")
        return Response("not vk")

    if event['secret'] == SECRET_KEY:
        if event['type'] == "confirmation":
            logger.info(f"Отправлен токен подтверждения: {CONFIRMATION_TOKEN}")
            return Response(CONFIRMATION_TOKEN)

        elif event['type'] == "message_new":
            event['object']['message']['text'] = event['object']['message']['text'].lower()
            background_task.add_task(await bot.process_event(event))
            
        return Response("ok")
