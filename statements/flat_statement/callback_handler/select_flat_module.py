import telebot

import commands
from statements import useful_methods
from utils import db_util, key_util


def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    if call.data and call.message:
        chat_id = useful_methods.id_from_message(call.message)
        data = get_from_db_prepare_data(call.data)
        useful_methods.change_statement(statement=commands.flat_detailed, message=call.message, chat_id=chat_id)
        send_message(call, bot, data)

    # solved show floors to user


def get_from_db_prepare_data(call_data):
    def flat_filter(flat):
        if isinstance(flat, db_util.FreeFlat):
            if int(flat.floor) == int(floor) and int(flat.price) != 0 and int(flat.total_area) != 0:
                return flat

    if len(call_data.split('-')) == 2:
        section_id = call_data.split('-')[0]
        floor = call_data.split('-')[1]
        if not section_id.isdigit() or not floor.isdigit():
            return None
        section = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.HouseSection,
                                                            identifier=db_util.HouseSection.section_id,
                                                            value=section_id)
        if isinstance(section, db_util.HouseSection):
            flats = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.FreeFlat,
                                                              identifier=db_util.FreeFlat.section_id,
                                                              value=section.section_id,
                                                              get_type='many')
            pre_result_flats = list(filter(flat_filter, flats))
            result_flats = [{f'Ціна:{useful_methods.format_num(flat.price)} Кількість кімнат:{flat.rooms}': flat.flat_id} for flat in pre_result_flats]
            return result_flats
    # solved part


def send_message(call: telebot.types.CallbackQuery, bot: telebot.TeleBot, data_to_markup):
    chat_id = useful_methods.id_from_message(call.message)
    useful_methods.try_delete_message(call.message, bot)
    if data_to_markup is None:
        useful_methods.change_statement(statement=commands.connect_to_manager, message=call.message, chat_id=chat_id)
        bot.send_message(chat_id=chat_id,
                         text='Сталася помилка, оберіть поверх пізніше.')
    else:
        markup = key_util.create_inline_keyboard(callback_data=True, title_to_data=data_to_markup)

        bot.send_message(chat_id=chat_id,
                         text='Оберіть квартиру',
                         reply_markup=markup)
