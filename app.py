import threading
import asyncio
import concurrent.futures
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

    # базированная многопоточность!
    schedule.every(5).seconds.do(machine_units)
    loop = asyncio.get_event_loop()
    executor = concurrent.futures.ThreadPoolExecutor(5)
    loop.set_default_executor(executor)

    async def function_one():
        while True:
            await schedule.run_pending()
            await asyncio.sleep(1)

    async def function_two():
        await bot.setup_webhook()

    async def some_callback_one():
        await function_one()

    async def some_callback_two():
        await function_two()

    def between_callback_one():
        await loop.run_until_complete(some_callback_one())

    def between_callback_two():
        await loop.run_until_complete(some_callback_two())

    threading.Thread(target=between_callback_one).start()
    threading.Thread(target=between_callback_two).start()


# обработчик POST-запросов
@app.post("/")
async def connection(req: Request, background_task: BackgroundTasks):
    event = await req.json()

    if "type" not in event.keys():
        logger.info("Пустой запрос!")
        return Response("not vk")

    if event['secret'] == SECRET_KEY:
        if event['type'] == "confirmation":
            logger.info(f"Отправлен токен подтверждения: {CONFIRMATION_TOKEN}")
            return Response(CONFIRMATION_TOKEN)

        elif event['type'] == "message_new":
            logger.info("Получено новое сообщение!")
            event['object']['message']['text'] = event['object']['message']['text'].lower()
            background_task.add_task(await bot.process_event(event))

        return Response("ok")
