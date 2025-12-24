from telebot.types import ChatMemberUpdated

def event_handlers(bot):
    @bot.my_chat_member_handler()
    async def on_bot_added_to_chat(member: ChatMemberUpdated):
        chat_id = member.chat.id
        chat_type = member.chat.type
        chat_name = member.chat.title
        status = member.new_chat_member.status

        print(f'Bot added to chat as {status}: id: {chat_id} | name: {chat_name} | type: {chat_type}')

        