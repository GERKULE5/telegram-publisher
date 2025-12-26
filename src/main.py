# src/main.py
import asyncio
from os import getenv
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message
from telebot.asyncio_storage import StateMemoryStorage
from telebot.states.asyncio.context import StateContext



load_dotenv()


from msg_locale import CommonMessages
from chat_events import event_handlers
from database.database import create_tables
from checks import check_admin
from buttons import render_main_menu
from commands.institutions import register_institution_comands
from redis_client.client import redis_connection
from kafka.manager import KafkaManager



kafka_manager = None

async def handle_kafka_response(response):
    from commands.institutions import process_auth_response
    await process_auth_response(bot, response)

async def initialize_kafka():
    global kafka_manager
    kafka_manager = await KafkaManager().initialize(handle_kafka_response)
    return kafka_manager


state_storage = StateMemoryStorage() # В проде поменять на Redis!!

bot = AsyncTeleBot(
    token=getenv('BOT_TOKEN'),
    state_storage=state_storage,
    parse_mode="markdown"
)

from telebot.states.asyncio.middleware import StateMiddleware
bot.setup_middleware(StateMiddleware(bot))

from telebot import asyncio_filters
bot.add_custom_filter(asyncio_filters.StateFilter(bot))



@bot.message_handler(commands=['start'])
async def start(message: Message):
    chat_id = message.chat.id
    is_admin = await check_admin(bot, message)
    await bot.send_message(chat_id, CommonMessages.WELCOME_MESSAGE, reply_markup=render_main_menu(is_admin))


@bot.message_handler(func=lambda m: m.text == CommonMessages.CANCEL)
async def handle_cancel_commands(message: Message, state: StateContext):
    await state.delete()
    is_admin = await check_admin(bot, message, silent=True)
    await bot.send_message(
        message.chat.id, 
        CommonMessages.CANCEL_ACTION,
        reply_markup=render_main_menu(is_admin)
    )


event_handlers(bot)
register_institution_comands(bot)


@bot.message_handler(func=lambda m: True)
async def echo_all(message: Message):
    current_state = await bot.get_state(message.from_user.id, message.chat.id)

    if current_state:
        return
    is_admin = await check_admin(bot, message, silent=True)
    await bot.reply_to(
        message,
        CommonMessages.ECHO_ALL,
        reply_markup = render_main_menu(is_admin)
    )

async def main():
    await create_tables()
    await redis_connection()

    await initialize_kafka()

    try:
        await bot.infinity_polling()
    finally:
        if kafka_manager:
            # Stoping kafka
            pass


if __name__ == '__main__':
    asyncio.run(main())


