from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery


from msg_locale import AuthMessages
from database.dao import get_admin

async def check_admin(bot: AsyncTeleBot, message: Message, silent: bool = False):
    if not await get_admin(message.from_user.id):
        if not silent:
            await bot.send_message(message.chat.id, AuthMessages.NOT_ADMIN)
            return False
        else: 
            return True