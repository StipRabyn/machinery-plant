from vkbottle.bot import Bot
from handlers.common import common_labeler
from handlers.admin_commands import admin_commands
from handlers.admin_text import admin_text
from vk_api import (
    api,
    labeler,
    callback)


# labelers
labeler.load(common_labeler)
labeler.load(admin_commands)
labeler.load(admin_text)


# бот
bot = Bot(api=api,
          callback=callback,
          labeler=labeler)
    
