"""choose profile - first statement in bot,
(you can choose admin account if your account exists in admin_accounts db)"""
import telebot

import commands
from statements import useful_methods
from utils import key_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)
    markup = key_util.create_reply_keyboard([commands.select_obj, commands.select_flat_by_params, commands.select_storeroom, commands.commercial_build])
    bot.send_message(chat_id=chat_id,
                     text='Вас вітає рієлтор бот!Оберіть пункт в меню:',
                     reply_markup=markup)
