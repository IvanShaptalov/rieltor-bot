import random
import string

import telebot
from icecream import ic

from utils import key_util, db_util


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
        print('try delete...')
        bot.delete_message(chat_id=id_from_message(message), message_id=message.id)
        print('deleted.')
    except Exception as e:
        print('cant delete message: ', e)


def firstname_from_message(message: telebot.types.Message):
    return message.from_user.first_name


def change_statement(statement, chat_id, message):
    # solved changed to > select flat in floor > flat_statement
    firstname = firstname_from_message(message=message)
    db_util.from_db_get_statement(chat_id=chat_id, message_text=statement, first_name=firstname)


def notify_admins(bot: telebot.TeleBot, message_text):
    admins = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.Admin,
                                                       all_objects=True)
    result_admins = [admin.chat_id for admin in admins]
    ic('try send info to admins')
    for admin_chat_id in result_admins:
        try:
            bot.send_message(chat_id=admin_chat_id,
                             text=message_text)
            print(f'sent {message_text} to admin{admin_chat_id}')
        except Exception as e:
            print(e)
            print(f"Error while try to send notify to admin {admin_chat_id}")
    ic('send info to admins done.')
