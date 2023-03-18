from vkbottle import Bot
from vk_api import (
    api,
    labeler,
    callback)
from handlers import (
    common,
    admin_commands,
    admin_text)


# labelers
labeler.load(common.common_labeler)
labeler.load(admin_commands.admin_commands)
labeler.load(admin_text.admin_text)


# бот
bot = Bot(api=api,
          callback=callback,
          labeler=labeler)
    
