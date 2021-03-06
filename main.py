import datetime
import os
import threading
import time

import telebot
from icecream import ic

import commands
import config_interpreter
from statements import statement_switcher
from utils import db_util, api

error_count = 0


def start_polling():
    ic('bot started')
    db_util.create_db()
    ic('db created (if not exist)')
    global error_count
    try:
        bot.polling()
    except Exception as error:
        print(error)
        time.sleep(5)
        ic(error_count)
        error_count += 1
        if error_count > 5:
            print('end')
            return
        start_polling()


bot = telebot.TeleBot(config_interpreter.BOT_TOKEN)


def start_bot_work():
    # text handling (just message,text)
    # user not blocked bot
    @bot.message_handler(content_types=['text'])
    def answer(message):

        if isinstance(message, telebot.types.Message):
            # select current user statement
            user_st_m = db_util.from_db_get_statement(message.chat.id, message.text, message.from_user.first_name)

            # select func to call
            func_message = statement_switcher.select_statement_message(user_st_m)

            # create client cabinet if not exist

            ic(user_st_m, func_message)
            # in argument : [message|callback], bot only, call function
            if func_message:
                func_message(message=message, bot=bot)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_answer(call):
        user_st_c = None
        if call.message:
            message = call.message
            user_st_c = db_util.from_db_get_statement(message.chat.id, message.text, message.from_user.first_name)
        elif call.from_user:
            user_st_c = db_util.from_db_get_statement(call.from_user.id, commands.start_menu, call.from_user.first_name)

        if user_st_c:
            func_callback = statement_switcher.select_statement_callback(user_st_c)
            ic(user_st_c, func_callback)
            # in argument : [message|callback], bot only
            if func_callback:
                func_callback(call=call, bot=bot)

    start_polling()


def update_info():
    if threading.active_count() < 5:
        thread = threading.Thread(target=_update)
        thread.setName('api worker')
        thread.start()


def _update():
    while True:
        seconds = datetime.timedelta(hours=12).total_seconds()
        print('sleep 12 hours')
        time.sleep(seconds)
        api.save_all_data_to_db()


if __name__ == '__main__':
    db_util.create_db()
    if os.environ.get('load_data'):
        print('load data detected: load')
        api.save_all_data_to_db()
    print("count ", db_util.get_count(db_util.UserStatements))
    update_info()
    start_bot_work()
    # todonext ????????????:???????????? , ????????
