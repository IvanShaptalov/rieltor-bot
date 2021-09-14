import telebot

import commands
from statements import useful_methods
from utils import key_util, db_util


def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    if call.data and call.message:
        chat_id = useful_methods.id_from_message(call.message)
        useful_methods.change_statement(statement=commands.select_flat, call=call, chat_id=chat_id)
        data = get_from_db_prepare_data(call)
        send_message(call, bot, data)


# solved show floors to user
def get_from_db_prepare_data(call: telebot.types.CallbackQuery):
    section = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.HouseSection,
                                                        identifier=db_util.HouseSection.section_id,
                                                        value=call.data)
    if isinstance(section, db_util.HouseSection):
        flats = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.FreeFlat,
                                                          identifier=db_util.FreeFlat.section_id,
                                                          value=section.section_id,
                                                          get_type='many')
        if flats:
            floor_index = 0
            # solved sort and unique data
            flat_floors_data = [{int(flat.floor): f"{section.section_id}-{flat.floor}"} for flat in flats]
            unique = list(map(dict, set(tuple(sorted(flat.items())) for flat in flat_floors_data)))

            return unique


# solved part


def send_message(call: telebot.types.CallbackQuery, bot: telebot.TeleBot, data_to_markup):
    chat_id = useful_methods.id_from_message(call.message)
    useful_methods.try_delete_message(call.message, bot)
    if data_to_markup is None:
        bot.send_message(chat_id=chat_id,
                         text='В цій секції немає вільних квартир')
    else:
        markup = key_util.create_inline_keyboard(callback_data=True, title_to_data=data_to_markup)

        bot.send_message(chat_id=chat_id,
                         text='Оберіть поверх',
                         reply_markup=markup)