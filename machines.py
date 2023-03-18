import random
from database import Database
from vk_api import api
from config import (
    MACHINES,
    DB_URL,
    hashes)


async def machine_units():
    # функция отправки сгенерированного юнита
    async def send_unit(type_unit, unit):
        await api.messages.send(peer_id=2000000003,
                                message=f"Произведена единица {type_unit}: {unit}",
                                random_id=0)

    # подключение к базе данных
    async with Database(DB_URL) as db:
        # проверка на наличие нужных хэшей
        await hashes(db)

        # фокус производства
        if await db.get("focus") == "1":
            options = (1, 2, 3)
        elif await db.get("focus") == "2":
            options = (1, 2, 2)
        else:
            options = (1, 1, 1)

        random_number = random.randint(1, 4)

        # генерация военной техники
        if random_number == options[0] or random_number == options[1] or random_number == options[2]:
            keys = []
            for key in MACHINES['Военная техника'].keys():
                keys.append(key)

            machine = random.choice(keys)

            if random.randint(1, 4) == 2:
                index = 0
                await send_unit("военной техники", MACHINES['Военная техника'][machine][index])
            else:
                if random.randint(1, 2) == 2:
                    index = 1
                    await send_unit("военной техники", MACHINES['Военная техника'][machine][index])
                else:
                    index = 2
                    await send_unit("военной техники", MACHINES['Военная техника'][machine][index])

            await db.hincrby(machine, MACHINES['Военная техника'][machine][index], 1)

        # генерация гражданской техники
        else:
            machine = random.choice(MACHINES['Гражданская техника'])
            await send_unit("гражданской техники", machine)
            await db.hincrby("Гражданская техника", machine, 1)
    
