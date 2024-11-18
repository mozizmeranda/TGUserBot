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

channel_link = env.str("CHANNEL_LINK")


bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


@bot.on_message(filters.chat(chats=channel_link))
async def echo(client: Client, message: Message):
    if message.from_user is None:
        await message.reply(text="Люди в шоке")


asyncio.run(bot.run())
