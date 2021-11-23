import logging
import random
from aiogram.utils import executor
from db_query import Mysql_queries
import config
from telebot import types
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import BotBlocked

# You can set parse_mode by default. HTML or MARKDOWN
bot = Bot(config.TOKEN)

# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands="start")
async def start_bot(message: types.Message):
    await message.reply("Hello")


async def any_input_handler(message: types.Message):
    await message.reply("Shake it")


@dp.message_handler(commands="block")
async def cmd_block(message: types.Message):
    await asyncio.sleep(10.0)  # Здоровый сон на 10 секунд
    await message.reply("Вы заблокированы")


@dp.errors_handler(exception=BotBlocked)
async def error_bot_blocked(update: types.Update, exception: BotBlocked):
    # Update: объект события от Telegram. Exception: объект исключения
    # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
    print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")

    # Такой хэндлер должен всегда возвращать True,
    # если дальнейшая обработка не требуется.
    return True


# alternative version of specifying the handler
dp.register_message_handler(any_input_handler, lambda x: True)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
