from io import BytesIO
from vkbottle.bot import BotLabeler
from vkbottle.callback import BotCallback
from vkbottle import (
    PhotoMessageUploader,
    API)
from config import (
    SECRET_KEY,
    TOKEN,
    URL)


# инициализация
api = API(token=TOKEN)
labeler = BotLabeler()
uploader = PhotoMessageUploader(api)
image_handler = BytesIO()

callback = BotCallback(url=URL,
                       title="Негев",
                       secret_key=SECRET_KEY)
    
