import random
import string

import telebot

from utils import key_util


def id_from_message(message: telebot.types.Message) -> int:
    """get chat id from message -> message.text.id, returns int or None"""
    assert message.chat.id
    chat_id = message.chat.id
    return chat_id


def id_from_user(from_user: telebot.types.User):
    """get chat id using from_user object -> message.text.id, returns int or None"""
    assert from_user.id
    chat_id = from_user.id
    return chat_id


def replace_call_data(call: telebot.types.CallbackQuery):
    inline_symbols = key_util.inline_symbols
    for inline_symbol in inline_symbols:
        if inline_symbol in call.data:
            call.data = call.data.replace(inline_symbol, '')


def rand_string(str_length):
    letters = string.ascii_letters
    st = ''
    st = st.join(random.choice(letters) for i in range(str_length))
    return st


def rand_num(n_min, n_max):
    number = random.randint(n_min, n_max)
    return number


def try_delete_message(message: telebot.types.Message, bot: telebot.TeleBot):
    try:
        bot.delete_message(chat_id=id_from_message(message), message_id=message.id)
    except Exception as e:
        print('cant delete message: ', e)
