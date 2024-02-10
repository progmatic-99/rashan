#!/usr/bin/env python
"""
Bot starting script
"""

from telegram import Update
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ConversationHandler,
    filters,
)

from config import bot_token
from commands import COMMANDS
from handlers import (
    start,
    get_item,
    get_item_quantity,
    get_price,
    help_command,
    PRICE,
    QUANTITY,
    ITEM,
)
from db import DB


async def post_init(app: Application):
    """After the app starts polling"""

    await app.bot.set_my_commands(COMMANDS)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token).post_init(post_init).build()
    db = DB()
    db.setup()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ITEM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_item)],
            QUANTITY: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_item_quantity)
            ],
            PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_price)],
        },
        fallbacks=[MessageHandler(filters.TEXT, help_command)],
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
