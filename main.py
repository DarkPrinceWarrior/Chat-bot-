import logging
import random
import aiogram.utils.markdown as fmt
from aiogram.types import ParseMode
from aiogram.utils import executor
from db_query import Mysql_queries
import config
from telebot import types
import asyncio
from aiogram import Bot, Dispatcher
from aiogram import *
from aiogram.utils.exceptions import BotBlocked

# You can set parse_mode by default. HTML or MARKDOWN
bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)

# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)




@dp.message_handler(commands="start")
async def start_bot(message: types.Message):
     # для скрытия кнопок после нажатия  one_time_keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    # one way to create button with text
    button_1 = types.KeyboardButton(text="Ничего")
    button_2 = "Прыгать"
    keyboard.add(button_1,button_2)
    # create button like variable string
    await message.answer("Что делать?", reply_markup=keyboard)

@dp.message_handler(commands="special_buttons")
async def cmd_special_buttons(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(text="Запросить геолокацию", request_location=True))
    keyboard.add(types.KeyboardButton(text="Запросить контакт", request_contact=True))
    keyboard.add(types.KeyboardButton(text="Создать викторину",
                                      request_poll=types.KeyboardButtonPollType(type=types.PollType.QUIZ)))
    await message.answer("Выберите действие:", reply_markup=keyboard)


# # type /block to block the user
# @dp.message_handler(commands="block")
# async def cmd_block(message: types.Message):
#     await asyncio.sleep(10.0)  # Здоровый сон на 10 секунд
#     await message.reply("Вы заблокированы")
#
#
# # handle the exception if user blocked the bot before
# @dp.errors_handler(exception=BotBlocked)
# async def error_bot_blocked(update: types.Update, exception: BotBlocked):
#     # Update: объект события от Telegram. Exception: объект исключения
#     # Здесь можно как-то обработать блокировку, например, удалить пользователя из БД
#     print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
#
#     # Такой хэндлер должен всегда возвращать True,
#     # если дальнейшая обработка не требуется.
#     return True


async def any_input_handler(message: types.Message):
    if message.text == "Ничего":
        #reply_markup=types.ReplyKeyboardRemove()
        await message.answer("Окей")
    elif message.text == "Прыгать":
        await message.answer("Давай начнем")
    else:
        mes = "Ты чет-то там написал"
        await message.answer(
            fmt.text(
                fmt.hunderline(mes),
                fmt.text(fmt.hbold("ИСПРАВЬ!")),
                sep="\n"

            ))



# indeed there is fun "answer_dice" in Message
@dp.message_handler(commands="dice")
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@dp.message_handler(content_types=[types.ContentType.ANIMATION])
async def echo_document(message: types.Message):
    await message.reply_animation(message.animation.file_id)


@dp.message_handler(content_types=[types.ContentType.DOCUMENT])
async def download_doc(message: types.Message):
    # Скачивание в каталог с ботом с созданием подкаталогов по типу файла
    await message.document.download()



# alternative version of specifying the handler
# can use it without (lambda x: True)
dp.register_message_handler(any_input_handler)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
