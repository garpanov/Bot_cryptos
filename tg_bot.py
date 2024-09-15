import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from database.engine import drop_db, create_db, session_maker
from database.middlewares_db import DataBaseSession

from handlers.user_private import router_for_user_private
from handlers.admin_private import admin_router
from common.commands_private import commands

# Ваши настройки
TOKEN = os.getenv("TOKEN")
WEB_SERVER_HOST = "0.0.0.0"  # Публичный доступ
WEB_SERVER_PORT = 8080
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://bot-cryptos.onrender.com{WEBHOOK_PATH}"
WEBHOOK_SECRET = "my-secret"

bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_router(admin_router)
dp.include_router(router_for_user_private)

async def on_startup(bot: Bot) -> None:
    run_param = False
    if run_param:
        await drop_db()

    await create_db()

    # Удаление старого вебхука, если он был установлен
    await bot.delete_webhook()
    # Установка нового вебхука
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)

async def on_shutdown(bot: Bot) -> None:
    print('бот лег')
    await bot.delete_webhook()

async def main() -> None:
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    # Создание веб-сервера aiohttp
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    await bot.set_my_commands(commands=commands, scope=types.BotCommandScopeAllPrivateChats())
    # Запуск веб-сервера
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    asyncio.run(main())
