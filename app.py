import asyncio
import nest_asyncio
import aioschedule as schedule
from loguru import logger
from worker import async_worker
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
    logger.info("Setup timer...")

    # базированный таймер!
    schedule.every(60).minutes.do(machine_units)
    nest_asyncio.apply()

    @async_worker
    async def times():
        while True:
            await schedule.run_pending()

    await asyncio.sleep(1)

    asyncio.run(times())
    asyncio.set_event_loop(asyncio.new_event_loop())


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
