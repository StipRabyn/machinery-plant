from vkbottle import (
    KeyboardButtonColor,
    Keyboard,
    Text)


# панель администратора
admin_panel = (
    Keyboard(one_time=False, inline=False)
    .add(Text("Ключи"), color=KeyboardButtonColor.POSITIVE)
    .add(Text("Восстановление"), color=KeyboardButtonColor.POSITIVE)
    .row()
    .add(Text("Инквизиция"), color=KeyboardButtonColor.PRIMARY)
    .add(Text("Производственный фокус"), color=KeyboardButtonColor.PRIMARY)
).get_json()
