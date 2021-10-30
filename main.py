import telebot

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot("2063611146:AAGzxv6wrychBuy6k1VkxctYS2L5jscbBMA", parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == "__main__":
    bot.infinity_polling()
