from database import Database
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.bot import (
    BotLabeler,
    Message)
from config import (
    ADMIN,
    DB_URL,
    hashes)
from typing import (
    List,
    Tuple)


# labeler
admin_commands = BotLabeler()


# фокус производства
@admin_commands.message(CommandRule("фокус", ['/', '!', ''], 1))
async def focus_command(message: Message, args: Tuple[str]):
    if message.from_id in ADMIN:
        async with Database(DB_URL) as db:
            # создания дефолтного ключа, если он не существует
            await db.setnx("focus", "2")

            if args[0] == '1':
                await db.set("focus", '1')
                await message.answer("✅ Успешно!")
            elif args[0] == '2':
                await db.set("focus", '2')
                await message.answer("✅ Успешно!")
            elif args[0] == '3':
                await db.set("focus", '3')
                await message.answer("✅ Успешно!")
            else:
                await message.answer("Да")
    else:
        await message.answer("⚠ Вы не являетесь администратором концерна!")


# восстановление техники
@admin_commands.message(CommandRule("восстановить", ['/', '!', ''], 17))
async def recovery_command(message: Message, args: List[str]):
    if message.from_id in ADMIN:
        itr = 0
        for index, arg in enumerate(args):
            if arg.isdigit():
                args[index] = int(arg)
            else:
                itr += 1

        if itr > 0:
            await message.answer("Да")
        else:
            async with Database(DB_URL) as db:
                # проверка на наличие нужных хэшей
                await hashes(db)

                # функция восстановления численности рода войск
                async def recovery_genus(arg1, arg2, arg3, type_unit, units):
                    await db.hincrby(type_unit, units[0], arg1)
                    await db.hincrby(type_unit, units[1], arg2)
                    await db.hincrby(type_unit, units[2], arg3)

                # техника
                civil = await db.hkeys("Гражданская техника")
                armored = await db.hkeys("Бронетехника")
                artillery = await db.hkeys("Артиллерия")
                fleet = await db.hkeys("Боевые корабли")
                aviation = await db.hkeys("Военная авиация")

                # восстановление численности родов войск
                for arg, civ in zip(args, civil):
                    await db.hincrby("Гражданская техника", civ, arg)

                await recovery_genus(args[5], args[6], args[7], "Бронетехника", armored)
                await recovery_genus(args[8], args[9], args[10], "Артиллерия", artillery)
                await recovery_genus(args[11], args[12], args[13], "Боевые корабли", fleet)
                await recovery_genus(args[14], args[15], args[16], "Военная авиация", aviation)

                await message.answer("✅ Успешно!")
    else:
        await message.answer("⚠ Вы не являетесь администратором концерна!")
  
