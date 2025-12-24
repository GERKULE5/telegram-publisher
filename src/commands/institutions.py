# src/commands/institutions.py
from telebot.types import Message
from telebot.states import State, StatesGroup
from telebot.states.asyncio.context import StateContext


from msg_locale import ButtonMessages, InstitutionMessages, CommonMessages
from buttons import render_main_menu, render_cancel_button
from database.dao import get_institution_by_code
from checks import check_admin

class InstitutionCodeState(StatesGroup):
        waiting_for_code = State()


def register_institution_comands(bot):

    @bot.message_handler(func=lambda m: m.text == ButtonMessages.LOGIN_INSTITUTION)
    async def login_institution(message: Message, state: StateContext):
        await state.set(InstitutionCodeState.waiting_for_code)
        await bot.send_message(message.chat.id, InstitutionMessages.CODE_MESSAGE, reply_markup=render_cancel_button())

    @bot.message_handler(state=InstitutionCodeState.waiting_for_code)
    async def process_login_institution(message: Message, state: StateContext):
        text = message.text
        user_id = message.from_user.id
        institution = await get_institution_by_code(text)

        if institution is not None:
            await state.delete()
            print(f'User: {user_id} added Insititution: {institution.id} with code: {institution.code}')
            return
        else:
            await bot.send_message(message.chat.id, InstitutionMessages.INSTITUTION_NOT_FOUND)