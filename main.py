import telebot

# You can set parse_mode by default. HTML or MARKDOWN
bot = telebot.TeleBot("2063611146:AAGzxv6wrychBuy6k1VkxctYS2L5jscbBMA", parse_mode=None)

filters = ['start', 'help', 'hello', 'hi']


@bot.message_handler(filters)
@bot.message_handler(func=lambda msg: msg.text.encode("utf-8") == "U+1F618")
def send_welcome(message):
    bot.reply_to(message, "Yeah pretty easy")


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# Handles all sent documents and audio files
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    bot.reply_to(message, "You sent document or audio")


# <- passes a PollAnswer type object to your function
# @bot.poll_handler()
# def handle_poll(answers):
#     pass


if __name__ == "__main__":
    bot.infinity_polling()
