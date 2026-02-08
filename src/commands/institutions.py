# src/commands/institutions.py
from telebot.types import Message
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from msg_locale import ButtonMessages, InstitutionMessages, CommonMessages
from buttons import render_main_menu, render_cancel_button
from checks import check_admin
from chat_events import event_handlers

from kafka.schemas import TokenValidationRequest
from kafka.sync_news import NewsKafkaService

from database.dao import authorize_user

class InstitutionCodeState(StatesGroup):
        waiting_for_code = State()


def register_institution_comands(bot, news):

    @bot.message_handler(func=lambda m: m.text == ButtonMessages.LOGIN_INSTITUTION)
    async def login_institution(message: Message, state: StateContext):
        await state.set(InstitutionCodeState.waiting_for_code)
        current_state = await bot.get_state(message.from_user.id, message.chat.id)
        print(f'State: {current_state}')
        await bot.send_message(message.chat.id, InstitutionMessages.CODE_MESSAGE, reply_markup=render_cancel_button())

    @bot.message_handler(state=InstitutionCodeState.waiting_for_code)
    async def process_login_institution(message: Message, state: StateContext):
        token = message.text
        print(token)
        user_id = message.from_user.id
        chat_id = message.chat.id
        
        sync_data = TokenValidationRequest(
             token = token,
             externalUserId = user_id,
             externalChatId = chat_id
        )

        
        await news.send('news.synchronized', sync_data.model_dump(mode='json'))

        print(f'sync data: {sync_data}\n{type(sync_data)}')
        # kafka logic:
        

        
        status = 'ok'

        if status == 'ok':
            await bot.send_message(message.chat.id, InstitutionMessages.ADD_TO_CHAT)
            return
        else:
            await bot.send_message(message.chat.id, InstitutionMessages.INSTITUTION_NOT_FOUND)
            await state.delete()