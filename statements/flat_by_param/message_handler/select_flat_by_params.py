"""choose profile - first statement in bot,
(you can choose admin account if your account exists in admin_accounts db)"""
import telebot
from statements import main_menu
import commands
from statements import useful_methods


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)
    useful_methods.change_statement(statement=commands.select_flat_by_params, message=message, chat_id=chat_id)
    main_menu.handle_message(message, bot)
