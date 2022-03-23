import time
from threading import Thread

import schedule
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot, Dispatcher, executor, types

import api
from loader import bot


def update(a):
    schedule.every().monday.at("00:01").do(api.update_limits)

    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    th = Thread(target=update, args=(1,))
    th.start()

    api.add_user('Main Admin', 'A_token', '1042486357', 500000, 500000, 'admin', 'address_USDT')
    api.add_coin('USDT', 'TRC-20', 'address')
    from handlers import dp

    executor.start_polling(dp)
