import telebot


def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    print(call)