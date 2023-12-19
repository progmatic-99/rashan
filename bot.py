#!/usr/bin/env python
"""
Bot starting script
"""
import logging

from telegram import Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler

from config import bot_token
from commands import COMMANDS
from handlers import start, button, help_command


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET & POST reqs being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def post_init(app: Application):
    """After the app starts polling"""

    await app.bot.set_my_commands(COMMANDS)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).post_init(post_init).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
