import random

import telebot
import config
from telebot import types

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(config.TOKEN, parse_mode=None)

filters = ['start', 'hello', 'hi', "whatsup"]


@bot.message_handler(filters)
def send_welcome(message):
    greetng_sticker = open("static/sticker.webp", "rb")
    bot.send_sticker(message.chat.id, greetng_sticker)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("🎲 Рандомное число")
    item2 = types.KeyboardButton("😀 Как дела?")

    markup.add(item1, item2)

    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name} my name is "
                                      f"'{bot.get_me().first_name}' bot ",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def echo_all(message):
    if message.chat.type == 'private':
        if message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 1000)))
        elif message.text == '😀 Как дела?':

            # inline keyboard
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо!", callback_data='good')
            item2 = types.InlineKeyboardButton("Так себе", callback_data='bad')
            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'У бота все хорошо, а у тебя?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Сложный запрос((')


# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    bot.reply_to(message, "You sent document or audio")


# Handles inline keyboard input
@bot.callback_query_handler(func=lambda m: True)
def inline_callback(call):
    try:
        if call.message:
            if call.data == 'good':
                print("We are here - inline_callback")
                bot.send_message(call.message.chat.id,
                                 'Отлично, мы с тобой на одной волне!)')
            else:
                bot.send_message(call.message.chat.id,
                                 'Что ж, пора разобраться, почему так!!!')

            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text='Мой ответ будет таким:',
                                  reply_markup=None)

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="Просто тестовое уведомл")

    except Exception as e:
        print(repr(e))


if __name__ == "__main__":
    bot.infinity_polling()
