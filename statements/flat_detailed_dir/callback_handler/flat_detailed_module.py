import telebot
import commands
from statements import useful_methods
from utils import db_util, key_util


def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    # todonow create flat detailed info
    if call.data and call.message:
        chat_id = useful_methods.id_from_message(call.message)
        useful_methods.try_delete_message(call.message, bot)
        useful_methods.change_statement(statement=commands.flat_detailed, call=call, chat_id=chat_id)

        data, flat_desc = get_from_db_prepare_data(call)
        send_message(call, bot, data, flat_desc)


def get_from_db_prepare_data(call: telebot.types.CallbackQuery):
    flat = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.FreeFlat,
                                                     identifier=db_util.FreeFlat.flat_id,
                                                     value=call.data)
    if isinstance(flat, db_util.FreeFlat):
        result_data = [{'Забронювати': flat.flat_id}]
        flat_desc = f"Поверх: {flat.floor}-й \nЦіна:{flat.price} грн\nПлоща:{flat.total_area} м2 \nКількість кімнат:{flat.rooms}"
        return result_data, flat_desc


def send_message(call: telebot.types.CallbackQuery, bot: telebot.TeleBot, data_to_markup, flat_description):
    chat_id = useful_methods.id_from_message(call.message)
    if data_to_markup is None:
        bot.send_message(chat_id=chat_id,
                         text='Сталася помилка, оберіть квартиру пізніше.')
    else:
        markup = key_util.create_inline_keyboard(callback_data=True, title_to_data=data_to_markup)

        bot.send_message(chat_id=chat_id,
                         text=f'Квартира:\n{flat_description}',
                         reply_markup=markup)
