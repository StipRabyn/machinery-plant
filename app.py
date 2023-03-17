import threading
import asyncio
import aioschedule as schedule
from loguru import logger
from bot import bot
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

    async def function_one():
        while True:
            await schedule.run_pending()
            await asyncio.sleep(1)

    async def function_two():
        await bot.setup_webhook()

    threading.Thread(target=asyncio.run, args=(function_one(),)).start()
    threading.Thread(target=asyncio.run, args=(function_two(),)).start()


# обработчик POST-запросов
@app.post("/pallas")
async def connection(req: Request, background_task: BackgroundTasks):
    event = await req.json()

    if "type" not in event.keys():
        logger.info("Empty request!")
        return Response("not vk")

    if event == SECRET_KEY:
        if event['type'] == "confirmation":
            return Response(CONFIRMATION_TOKEN)

        elif event['type'] == "message_new":
            event['object']['message']['text'] = event['object']['message']['text'].lower()
            background_task.add_task(await bot.process_event(event))

        return Response("ok")
    
