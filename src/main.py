import asyncio
from os import getenv
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot.states.asyncio.context import StateContext


load_dotenv()


from msg_locale import CommonMessages
from chat_events import event_handlers
from database.database import create_tables
from checks import check_admin
from buttons import render_main_menu
from commands.institutions import register_institution_comands
from redis_client.client import redis_connection


bot = AsyncTeleBot(
    token=getenv('BOT_TOKEN'),
    parse_mode="markdown"
)


@bot.message_handler(commands=['start'])
async def start(message: Message):
    chat_id = message.chat.id
    is_admin = await check_admin(bot, message, silent=False)
    await bot.send_message(chat_id, CommonMessages.WELCOME_MESSAGE, reply_markup=render_main_menu(is_admin))


@bot.message_handler(state="*", func=lambda m: m.text == CommonMessages.CANCEL)
async def handle_cancel_commands(message: Message, state: StateContext):
    state.delete()
    user_id = message.from_user.id
    await bot.send_message(
        message, 
        CommonMessages.CANCEL_ACTION,
        reply_markup=render_main_menu(is_admin=check_admin(user_id))
    )

async def main():
    event_handlers(bot)
    await register_institution_comands(bot)
    await create_tables()
    await redis_connection()
    await bot.infinity_polling()

if __name__ == '__main__':
    asyncio.run(main())


