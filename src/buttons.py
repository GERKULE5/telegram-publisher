# src/buttons.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from msg_locale import ButtonMessages, CommonMessages

def render_main_menu(is_admin: bool = False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if is_admin:
        markup.add(
            KeyboardButton(ButtonMessages.LOGIN_INSTITUTION)
        )    
    else:
        markup.add(
            KeyboardButton(ButtonMessages.LOGIN_INSTITUTION)
        )
    return markup


def render_cancel_button(add_skip: bool = False, inline: bool = False):
    
    if inline:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(CommonMessages.CANCEL, callback_data="cancel"))

        return markup

    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(CommonMessages.CANCEL)
        if add_skip:
            markup.add(CommonMessages.SKIP)
        return markup