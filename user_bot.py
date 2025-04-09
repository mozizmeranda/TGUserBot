from pyrogram import Client, filters
from pyrogram.types import Message
from environs import Env
import asyncio


env = Env()
env.read_env()

api_id = env.str("API_ID")
api_hash = env.str("API_HASH")
phone = env.str("PHONE")
login = "A"

channel_link = "-1002683245680"


bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


@bot.on_message(filters.chat(chats=-1001725812090))
async def echo(client: Client, message: Message):
    if message.from_user is None:
        await message.reply(text="Люди в шоке")

@bot.on_message(filters.chat(chats=6287458105))
async def e(client: Client, message: Message):
    if message.text == "1":
        await message.reply(text="Fuck you!!")

asyncio.run(bot.run())
# if __name__ == "__main__":
#     asyncio.run(bot.run())
#     bot.send_message(chat_id=6287458105, text="Bot has started working.")

