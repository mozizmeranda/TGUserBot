from pyrogram import Client, filters
from pyrogram.types import Message
from environs import Env
import asyncio
import time


env = Env()
env.read_env()

api_id = env.str("API_ID")
api_hash = env.str("API_HASH")
phone = env.str("PHONE")
login = "A"

channel_link = env.list("CHANNEL_LINK")
channel_link = list(map(int, env.list("CHANNEL_LINK")))
print(channel_link)
# lst = [-1002683245680, -1001725812090, 6287458105, -1001861451231]


bot = Client(name=login, api_id=api_id, api_hash=api_hash, phone_number=phone)


# @bot.on_message(filters.chat(chats=-1001725812090))
# async def echo(client: Client, message: Message):
#     if message.from_user is None:
#         print("CALL")
#         await bot.send_message(chat_id=6287458105, text="Comment was written")
#         await message.reply(text="Люди в шоке")

@bot.on_message(filters.chat(chats=channel_link))
async def echo(client: Client, message: Message):
    await message.reply(text="Люди в шоке")


# @bot.on_message(filters.chat(chats=lst))
# async def e(client: Client, message: Message):
#     if message.text == "1":
#         await message.reply(text="Fuck you!!")

asyncio.run(bot.run())
# if __name__ == "__main__":
#     asyncio.run(bot.run())
#     bot.send_message(chat_id=6287458105, text="Bot has started working.")

