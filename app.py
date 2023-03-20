import time
import datetime
import asyncio
from random import choice
from loguru import logger
from vk_bot import bot
from machines import machine_units
from database import Database
from config import (
    DB_URL,
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
    logger.info("Setup timer...")

    # базированный таймер!
    async def timer():
        async with Database(DB_URL) as db:
            # функция ключа для таймера
            async def clock():
                times = {"hour": int(time.strftime("%H", time.localtime())),
                         "minutes": int(time.strftime("%M", time.localtime())) + 13}

                await db.hmset("timer", times)

            # создание дефолтного ключа для таймера
            if "timer" not in await db.keys():
                await clock()

            # цикл таймера
            while True:
                timerr = await db.hgetall("timer")
                time_unit = datetime.time(int(timerr['hour']), int(timerr['minutes']))
                time_now = datetime.time(int(time.strftime("%H", time.localtime())),
                                         int(time.strftime("%M", time.localtime())))

                if time_now >= time_unit:
                    if choice(tuple(range(1, 4))) == 1:
                        await machine_units(2000000002)
                        await clock()
                    else:
                        await machine_units(2000000001)
                        await clock()

                await asyncio.sleep(1)

    asyncio.create_task(timer())


# обработчик POST-запросов
@app.post('/')
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
