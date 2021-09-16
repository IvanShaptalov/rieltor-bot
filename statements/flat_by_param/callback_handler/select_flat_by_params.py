import telebot

import commands
from statements import useful_methods
from statements.main_menu import get_house_obj
from utils import db_util


def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    if call and call.data and call.message:
        chat_id = useful_methods.id_from_message(call.message)
        house = get_house_obj(call_id=call.data)
        useful_methods.change_statement(statement=commands.filtering, chat_id=chat_id, message=call.message)
        bot.send_message(chat_id=chat_id,
                         text='Введіть пункти фільтрації наступним чином\n(тільки цифри та коми, без слів в дужках):\n'
                              '5(кількість кімнат),(ціна за м2)1000-2000,(загальна площа)100-200\nприклад:\n5,1000-2000,100-200')

    # todonext create filtering flats using house > rooms, price, area

