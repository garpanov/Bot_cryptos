import asyncio
from aiogram import Bot, Dispatcher, types
import os
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from database.engine import drop_db, create_db, session_maker
from database.middlewares_db import DataBaseSession


from handlers.user_private import router_for_user_private
from handlers.admin_private import admin_router
from common.commands_private import commands

bot = Bot(os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(admin_router)
dp.include_router(router_for_user_private)


async def on_startup(bot):

    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('бот лег')

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=commands, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())