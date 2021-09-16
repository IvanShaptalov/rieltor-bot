import telebot

import commands
import config_interpreter
from statements import useful_methods
from utils import db_util, key_util


def get_from_db_prepare_data(call: telebot.types.CallbackQuery):
    flat = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.FreeFlat,
                                                     identifier=db_util.FreeFlat.flat_id,
                                                     value=call.data)
    if isinstance(flat, db_util.FreeFlat):
        flat_desc = f"Поверх: {flat.floor}-й \nЦіна:{flat.price} грн\nПлоща:{flat.total_area} м2 \nКількість кімнат:{flat.rooms}"
        return flat_desc


def send_message(call, bot, flat_desc):
    if call.message and flat_desc:
        username = useful_methods.firstname_from_message(call.message)
        chat_id = useful_methods.id_from_message(call.message)
        useful_methods.try_delete_message(call.message, bot)
        bot.send_message(chat_id=chat_id,
                         text=f'Квартира:\n{flat_desc}\n{username}')


def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    if call.data and call.message:
        chat_id = useful_methods.id_from_message(call.message)
        useful_methods.change_statement(statement=commands.connect_to_manager, message=call.message, chat_id=chat_id)
        flat_desc = get_from_db_prepare_data(call)
        username = call.from_user.username
        if flat_desc:
            useful_methods.notify_admins(bot,  f'Нове замовлення:\n{flat_desc}\n{username}')
            send_message_to_user(bot, call.message, flat_desc)


def send_message_to_user(bot: telebot.TeleBot, message: telebot.types.Message, message_text):
    chat_id = useful_methods.id_from_message(message)
    markup = key_util.create_inline_keyboard(
        link=config_interpreter.manager_link, title_to_data=[{'Звʼязатися з менеджером': 0}])
    bot.send_message(chat_id=chat_id,
                     text='Натисніть на кнопку звʼязатися з менеджером',
                     reply_markup=markup)
