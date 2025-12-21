import asyncio
from os import getenv
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery


load_dotenv()


from msg_locale import CommonMessages
from chat_events import event_handlers



bot = AsyncTeleBot(
    token=getenv('BOT_TOKEN')
)

event_handlers(bot)


@bot.message_handler(commands=['start'])
async def start(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, CommonMessages.welcome_message)


if __name__ == '__main__':
    asyncio.run(bot.infinity_polling())


