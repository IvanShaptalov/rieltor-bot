import telebot
import commands
from statements import useful_methods
from utils import db_util, key_util


def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    # solved create flat detailed info
    # solved add send message to administrator and send info to them about this client

    if call.data and call.message:
        chat_id = useful_methods.id_from_message(call.message)
        data, flat_desc = get_from_db_prepare_data(call.data)
        useful_methods.change_statement(statement=commands.connect_to_manager, message=call.message, chat_id=chat_id)
        send_message(call, bot, data, flat_desc)


def get_from_db_prepare_data(call_data):
    flat = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.FreeFlat,
                                                     identifier=db_util.FreeFlat.flat_id,
                                                     value=call_data)
    if isinstance(flat, db_util.FreeFlat):
        result_data = [{'Забронювати': flat.flat_id}]
        price = useful_methods.format_num(flat.price)
        flat_desc = f"Поверх : {flat.floor}-й \nЦіна :{price} {flat.currency}\nПлоща :{flat.total_area} м² \nКількість кімнат :{flat.rooms}"
        return result_data, flat_desc


def send_message(call: telebot.types.CallbackQuery, bot: telebot.TeleBot, data_to_markup, flat_description):
    chat_id = useful_methods.id_from_message(call.message)
    if data_to_markup is None:
        useful_methods.change_statement(statement=commands.connect_to_manager, message=call.message, chat_id=chat_id)
        bot.send_message(chat_id=chat_id,
                         text='Сталася помилка, оберіть квартиру пізніше.')
    else:
        markup = key_util.create_inline_keyboard(callback_data=True, title_to_data=data_to_markup)
        useful_methods.try_delete_message(call.message, bot)
        bot.send_message(chat_id=chat_id,
                         text=f'Квартира:\n{flat_description}',
                         reply_markup=markup)
