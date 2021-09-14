import telebot
import commands
from statements import useful_methods
from utils import db_util, key_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)
    houses = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.HouseObj,
                                                       all_objects=True)
    house_data = [{house.house_name: house.house_id} for house in houses]
    markup = key_util.create_inline_keyboard(callback_data=True, title_to_data=house_data)
    bot.send_message(chat_id=chat_id,
                     text='Вас вітає рієлтор бот!Оберіть об`єкт:',
                     reply_markup=markup)


def handle_callback(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    if call and call.data and call.message:
        chat_id = useful_methods.id_from_message(call.message)
        # todonow change statement to select floor
        # db_util.from_db_get_statement(chat_id=chat_id, message_text=)

        data = call.data
        house = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.HouseObj,
                                                          identifier=db_util.HouseObj.house_id,
                                                          value=data)
        if isinstance(house, db_util.HouseObj):
            sections = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.HouseSection,
                                                                 identifier=db_util.HouseSection.house_obj_id,
                                                                 value=house.house_id,
                                                                 get_type='many')
            sections_data = [{"{} - {} секція".format(house.house_name, section.section_id): section.section_id} for section in sections]
            markup = key_util.create_inline_keyboard(callback_data=True, title_to_data=sections_data)
            useful_methods.try_delete_message(call.message, bot)
            bot.send_message(chat_id=chat_id,
                             text='Оберіть секцію:',
                             reply_markup=markup)

