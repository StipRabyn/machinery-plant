import time 
import datetime
import asyncio
from random import choice
from loguru import logger
from vk_bot import bot 
from vk_api import api
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
    async with Database(DB_URL) as db:

        # функция ключа для таймера
        async def clock():  
            hour = int(time.strftime("%H", time.localtime()))
            minutes = int(time.strftime("%M", time.localtime()))

            if minutes >= 49:
                minutes_hour = hour * 60 + minutes + 10
                hour = minutes_hour // 60
                minutes = minutes_hour % 60
            else:
                minutes += 10

            times = {"hour": hour,
                     "minutes": minutes}

            await db.hmset("timer", times)

        # функция с циклом таймера
        async def timer():
            while True:
                if await db.exists("timer"):
                    hash_unit = await db.hgetall("timer")
                    await db.delete("timer")
                    await db.hmset("timer", hash_unit)
                else:
                    await clock()

                timerr = await db.hgetall("timer")
                time_unit = datetime.time(int(timerr['hour']), 
                                          int(timerr['minutes']))
                time_now = datetime.time(int(time.strftime("%H", time.localtime())),
                                         int(time.strftime("%M", time.localtime())))

                if time_now >= time_unit:
                    if choice(tuple(range(1, 4))) == 1:
                        await clock()
                        await machine_units(2000000002)
                    else:
                        await clock()
                        await api.messages.send(peer_id=2000000004,
                                                message="Да",
                                                random_id=0)

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
