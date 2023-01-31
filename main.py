# python -m venv venv - команда для создания виртуального окружения вторая Venv - название папки
# виртуальное окружение хранит все подгружаемые библиотеки. При загрузке на сервер окружение позволяет выполнять код из библиотек
# https://t.me/STONECx3 - stone


from aiogram import executor
from handlers import dp

async def on_start(_):
    print('Бот запущен')

executor.start_polling(dp, skip_updates=True, on_startup=on_start)
