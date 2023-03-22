from database import Database
from keyboards import admin_panel
from vkbottle.bot import (
    BotLabeler,
    Message)
from config import (
    ADMIN,
    DB_URL,
    hashes)


# labeler
admin_text = BotLabeler()


# тестовая временная команда
@admin_text.private_message(text='лют кал')
async def lut_kal(message: Message):
    async with Database(DB_URL) as db:
        await message.answer(await db.hgetall('times'))


# панель администратора
@admin_text.private_message(text=['админ', '!админ', '/админ'])
async def admin_txt(message: Message):
    if message.from_id in ADMIN:
        await message.answer("Караси — род лучеперых рыб семейства карповых", keyboard=admin_panel)
    else:
        await message.answer("⚠ Вы не являетесь администратором концерна!")


# фокус производства
@admin_text.message(text=['производственный фокус', 'производственный фокус', '/производственный фокус'])
async def focus_txt(message: Message):
    if message.from_id in ADMIN:
        async with Database(DB_URL) as db:
            await hashes(db)
            focus = await db.get("focus")

            if focus == '1':
                focus = "Военный"
            elif focus == '2':
                focus = "Сбалансированный"
            else:
                focus = "Гражданский"

            await message.reply(f"🏭 Ваш фокус производства техники: {focus}\n"
                                "Для установления фокуса введите следующую команду:\n\n"
                                "!фокус 1 / 2 / 3\n\n"
                                "1 -- Военный\n2 -- Сбалансированный\n3 -- Гражданский")
    else:
        await message.answer("⚠ Вы не являетесь администратором концерна!")


# восстановление техники
@admin_text.private_message(text=['восстановление', '!восстановление', '/восстановление'])
async def recovery_txt(message: Message):
    if message.from_id in ADMIN:
        await message.reply("♻ Для восстановления техники введите следующую команду с числами в угловых скобках:\n\n"
                            "!восстановить <автомобили> <морские суда> <воздушные суда> <поезда> <трактора> "
                            "<основные боевые танки> <танкетки> <бронетранспортеры> <самоходные> <зенитные> "
                            "<буксируемые> <корветы> <боевые катера> <десантные корабли> <бомбардировщики> "
                            "<ударные вертолеты> <истребители>")
    else:
        await message.answer("⚠ Вы не являетесь администратором концерна!")


# ключи базы данных
@admin_text.private_message(text=['ключи', '!ключи', '/ключи'])
async def keys_txt(message: Message):
    if message.from_id in ADMIN:
        async with Database(DB_URL) as db:
            cap = "🔑 Ключи базы данных:\n\n"
            for key in await db.keys():
                cap += key + "\n"

            await message.reply(cap)
    else:
        await message.answer("⚠ Вы не являетесь администратором концерна!")


# очистка базы данных
@admin_text.private_message(text=['инквизиция', '!инквизиция', '/инквизиция'])
async def inquisition_txt(message: Message):
    if message.from_id in ADMIN:
        async with Database(DB_URL) as db:
            keys = await db.keys()
            for key in keys:
                if key in ("Гражданская техника", "Бронетехника", "Военная авиация",
                           "Боевые корабли", "Артиллерия"):
                    await db.delete(key)

        await message.answer("✅ Успешно!")
    else:
        await message.answer("⚠ Вы не являетесь администратором концерна!")
    
