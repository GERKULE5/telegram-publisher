from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext


from msg_locale import ButtonMessages, InstitutionMessages, CommonMessages
from buttons import render_main_menu, render_cancel_button
from database.dao import get_institution_by_code

class InstitutionCodeState(StatesGroup):
    waiting_for_code = State()


async def register_institution_comands(bot: AsyncTeleBot):

    @bot.message_handler(func=lambda m: m.text == ButtonMessages.LOGIN_INSTITUTION)
    async def login_institution(message: Message, state: StateContext):
        await state.set(InstitutionCodeState.waiting_for_code)
        await bot.send_message(message, InstitutionMessages.CODE_MESSAGE, reply_markup=render_cancel_button())

    @bot.message_handler(InstitutionCodeState.waiting_for_code)
    async def process_login_institution(message: Message, state: StateContext):
        text = message.text
        user_id = message.from_user.id
        

        institution = await get_institution_by_code(text)

        if institution is not None:
            await state.delete()
            print(f'User: {id} added Insititution: {institution.id} with code: {institution.code}')
            return
        else:
            await bot.send_message(InstitutionMessages.INSTITUTION_NOT_FOUND)