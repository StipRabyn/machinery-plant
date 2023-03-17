import random
import matplotlib.pyplot as plt
from database import Database
from config import (
    DB_URL,
    hashes)
from vkbottle.bot import (
    BotLabeler,
    Message)
from vk_api import (
    uploader,
    image_handler)


# labeler
common_labeler = BotLabeler()


# список команд
@common_labeler.message(text=['команды', '!команды', '/команды'])
async def commands_txt(message: Message):
    await message.reply("📋 Список команд:\n\n"
                        "Реестр -- вывод списка и диаграммы техники\n"
                        "Админ -- панель администратора (доступна только манулам)")


# реестр военной техники
@common_labeler.message(text=['реестр', '!реестр', '/реестр'])
async def list_txt(message: Message):
    # подключение к базе данных
    async with Database(DB_URL) as db:
        # проверка на наличие нужных хэшей
        await hashes(db)

        # функция подсчета суммы единиц техники
        async def function(unit_type):
            result = 0
            for unit in await db.hkeys(unit_type):
                result += int(await db.hget(unit_type, unit))
            return result

        # техника
        armored = await db.hgetall("Бронетехника")
        artillery = await db.hgetall("Артиллерия")
        fleet = await db.hgetall("Боевые корабли")
        aviation = await db.hgetall("Военная авиация")
        civil = await db.hgetall("Гражданская техника")

        # создание круговой диаграммы
        sizes = {"Бронетехника": await function("Бронетехника"),
                 "Артиллерия": await function("Артиллерия"),
                 "Боевые корабли": await function("Боевые корабли"),
                 "Военная авиация": await function("Военная авиация"),
                 "Гражданская техника": await function("Гражданская техника")}

        for key, value in list(sizes.items()):
            if value <= 0:
                del sizes[key]

        plt.pie(sizes.values(),
                labels=sizes.keys(),
                explode=random.sample((0.1, 0.1, 0.1, 0.1, 0.1), len(sizes.keys())),
                autopct="%1.1f%%",
                shadow=True)
        plt.axis('equal')
        plt.legend(loc='best')
        plt.savefig(image_handler, format="png")
        plt.close()

        # сохранение круговой диаграммы
        image = image_handler.getvalue()
        image_handler.seek(0)
        photo = await uploader.upload(image)

        # вывод реестра
        await message.answer(f"⛴ Гражданская техника\n\n"
                             
                             f"Автомобили: {civil['Автомобиль']}\n"
                             f"Морские суда: {civil['Морское судно']}\n"
                             f"Воздушные суда: {civil['Воздушное судно']}\n"
                             f"Поезда: {civil['Поезд']}\n"
                             f"Трактора: {civil['Трактор']}\n\n"
                             
                             f"✈ Военная техника\n\n"
                             
                             f"Бронетехника:\n"
                             f"Основные боевые танки: {armored['Основной боевой танк']}\n"
                             f"Танкетки: {armored['Танкетка']}\n"
                             f"Бронетранспортеры: {armored['Бронетранспортер']}\n\n"
                             
                             f"Артиллерийские установки:\n"
                             f"Самоходные: {artillery['Самоходная установка']}\n"
                             f"Зенитные: {artillery['Зенитная установка']}\n"
                             f"Буксируемые: {artillery['Буксируемая установка']}\n\n"
                             
                             f"Боевые корабли:\n"
                             f"Корветы: {fleet['Корвет']}\n"
                             f"Боевые катера: {fleet['Боевой катер']}\n"
                             f"Десантные корабли: {fleet['Десантный корабль']}\n\n"

                             f"Военная авиация:\n"
                             f"Бомбардировщики: {aviation['Бомбардировщик']}\n"
                             f"Ударные вертолеты: {aviation['Ударный вертолет']}\n"
                             f"Истребители: {aviation['Истребитель']}",

                             attachment=photo)
    
