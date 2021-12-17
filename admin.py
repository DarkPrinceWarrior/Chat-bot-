from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
import aiogram.utils.markdown as fmt

import config
from telebot import types
from aiogram import *

async def admin_actions(message: types.Message):
    # check for admin
    try:
        user = message.from_user.username
        if user == "MabelHUGO":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            button_1 = "Add user"
            button_2 = "Delete user"
            button_3 = "Edit user"
            keyboard.add(button_1, button_2,button_3)
            await message.answer("Hello, Admin", reply_markup=keyboard)

        else:
            await message.answer("Permission denied!")

    except BaseException:
        await message.answer("Error occurred with credentials check!")



async def any_input_handler(message: types.Message):
    if message.text == "Add user":
        # reply_markup=types.ReplyKeyboardRemove() удалить клаву
        buttons = [
            types.InlineKeyboardButton(text="ДА", callback_data="Да"),
            types.InlineKeyboardButton(text="НЕТ", callback_data="Нет")
        ]
        inline_keyboard = types.InlineKeyboardMarkup()
        inline_keyboard.add(*buttons)
        await message.reply("Точно?", reply_markup=inline_keyboard)

    elif message.text == "Delete user":
        await message.reply("Давай начнем")

    elif message.text == "Edit user":
        await message.reply("Давай начнем")

    else:
        mes = "Don't understand"
        await message.reply(
            fmt.text(
                fmt.text(fmt.hbold(mes)),  sep="\n"))