import logging
import os

from AI.lunch import Model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from AI import lunch
from AI import nltk_utils
import random
import config
import aiogram.utils.markdown as fmt
import numpy as np
from keras.utils.np_utils import to_categorical
from aiogram.types import ParseMode
from telebot import types
from aiogram import *

# You can set parse_mode by default. HTML or MARKDOWN
bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)

# Диспетчер для бота
dp = Dispatcher(bot)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# create and fit the model
model = Model()
model.prepare_train_labels()

@dp.message_handler(commands="start")
async def start_bot(message: types.Message):
    # для скрытия кнопок после нажатия  one_time_keyboard
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    # one way to create button with text
    button_1 = types.KeyboardButton(text="Ничего")
    button_2 = "Прыгать"
    keyboard.add(button_1, button_2)
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
        # reply_markup=types.ReplyKeyboardRemove() удалить клаву
        buttons = [
            types.InlineKeyboardButton(text="ДА", callback_data="Да"),
            types.InlineKeyboardButton(text="НЕТ", callback_data="Нет")
        ]
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(*buttons)
        await message.answer("Точно?", reply_markup=inline_keyboard)
    elif message.text == "Прыгать":
        await message.answer("Давай начнем")
    else:
        model1 = model.getModel()
        sentence = nltk_utils.tokenize(message.text)
        sentence = nltk_utils.bag_of_words(sentence, model.all_words)
        sentence = np.array(sentence)
        sentence = sentence.reshape(1, sentence.shape[0])

        prediction = model1.predict(sentence)
        tag_index = np.argmax(prediction)
        tag = model.tags[tag_index]
        bot_answer = model.getResponse(tag)


        mes = "Ты чет-то там написал"
        await message.answer(
            fmt.text(
                fmt.hunderline(mes),
                fmt.text(fmt.hbold(bot_answer," :",tag)),
                sep="\n"

            ))


@dp.callback_query_handler()
async def send_random_value(call: types.CallbackQuery):
    if call.data == "Да":
        await call.answer(text="Ну и сиди себе!", show_alert=True)
        # или просто await call.answer()
    else:
        await call.answer(text="Отлично, я знал, что ты не такой, как все", show_alert=False)
        # await call.message.answer("Отлично, я знал, что ты не такой, как все")
        # after that Telegram waits for us for 30 sec(wait for callback) and then close the watch icon


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
