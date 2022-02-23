
__all__ = [
    'send_inline_keyboard', 'send_multiline_keyboard', 'send_inline_rows_keyboard'
    ]

from telebot import types

from config import (
     IsDebug, IsDeepDebug, IsTrace, IsPrintExceptions, 
     errorlog, print_to, print_exception,
     is_webhook,
    )

from app.settings import DEFAULT_PARSE_MODE

def send_inline_keyboard(bot, message, keys, question, parse_mode=None):
    """
    """
    buttons = [[types.InlineKeyboardButton(text=text, callback_data=key) 
        for text, key in keys]]

    keyboard = types.InlineKeyboardMarkup(buttons)
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard, parse_mode=parse_mode or DEFAULT_PARSE_MODE)

def send_inline_rows_keyboard(bot, message, keys, question, parse_mode=None):
    """
    """
    buttons = [[types.InlineKeyboardButton(text=text, callback_data=key)]
        for text, key in keys]

    keyboard = types.InlineKeyboardMarkup(buttons)
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard, parse_mode=parse_mode or DEFAULT_PARSE_MODE)

def send_multiline_keyboard(bot, message, rows, question, parse_mode=None):
    """
    """
    buttons = [[types.InlineKeyboardButton(text=text, callback_data=key) 
        for text, key in row] for row in rows]

    keyboard = types.InlineKeyboardMarkup(buttons)
    bot.send_message(message.chat.id, text=question, reply_markup=keyboard, parse_mode=parse_mode or DEFAULT_PARSE_MODE)
