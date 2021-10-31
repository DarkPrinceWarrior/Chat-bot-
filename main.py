import telebot
import config

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot(config.TOKEN, parse_mode=None)

filters = ['start','hello', 'hi', "whatsup"]


@bot.message_handler(filters)
def send_welcome(message):
    greetng_sticker = open("static/sticker.webp","rb")
    bot.send_sticker(message.chat.id,greetng_sticker)
    bot.send_message(message.chat.id, f"Hello {message.from_user.first_name} my name is "
                                      f"'{bot.get_me().first_name}' bot ")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    bot.reply_to(message, "You sent document or audio")


if __name__ == "__main__":
    bot.infinity_polling()
