from aiogram.utils import exceptions
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from database import Users
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from environs import Env
import asyncio


env = Env()
env.read_env()
API_TOKEN = env.str("TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())
db = Users()


async def on_start(dp: Dispatcher):
    db.create_table_users()
    await dp.bot.send_message(chat_id=5069469905, text="The bot is running !")


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне ссылку на рилс в Instagram, и я загружу его для тебя.")


def get_download_link(instagram_url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        download_page_url = f"https://iqsaved.com/ru/download-posts/{instagram_url.split('/')[-2]}/"
        driver.get(download_page_url)

        a_tag = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/section/div/section[2]/div/ul/li/div[3]/a'))
        )
        return a_tag.get_attribute('href')
    except Exception as e:
        print(f'Ошибка при извлечении ссылки: {e}')
        return 'Ссылка не найдена'
    finally:
        driver.quit()


async def animate_loading(chat_id, message_id):
    symbols = [r'\\', '|', '/', r'\\', '|', '/']
    while True:
        for symbol in symbols:
            try:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                            text=f"Загрузка началась, "
                                                 f"пожалуйста подождите {symbol}")
                await asyncio.sleep(0.5)
            except exceptions.MessageNotModified:
                pass


@dp.message_handler(regexp=r'https?://(www\.)?instagram\.com/(reel|p)/[^/]+/')
async def download_reel(message: types.Message):
    ans = await message.answer("Загрузка началась, пожалуйста подождите. Максимум 1-2 минуты.")

    task = asyncio.create_task(animate_loading(message.chat.id, ans.message_id))

    try:
        url = message.text
        download_link = get_download_link(url)
        if db.check_user(message.from_user.id) is None:
            if message.from_user.username:
                parameters = (message.from_user.id, message.from_user.full_name, f"@{message.from_user.username}")
            else:
                parameters = (message.from_user.id, message.from_user.full_name, "Nothing")
            db.insert_data(params=parameters)

        await bot.send_video(message.from_user.id, video=download_link)
    finally:
        task.cancel()
        await bot.delete_message(chat_id=message.chat.id, message_id=ans.message_id)


@dp.message_handler(commands=["users"])
async def get_users(message: types.Message):
    await bot.send_message(chat_id=-1002149382751, text=db.get_all_users())


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_start)
