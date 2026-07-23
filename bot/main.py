import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from bot.handlers import router
from bot.storage import LeadStorage


async def run() -> None:
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise SystemExit("BOT_TOKEN is not set (put it into .env, see .env.example)")

    logging.basicConfig(level=logging.INFO)
    bot = Bot(token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    dispatcher["lead_storage"] = LeadStorage(os.environ.get("DB_PATH", "leads.db"))
    await dispatcher.start_polling(bot)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
