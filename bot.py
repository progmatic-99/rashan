#!/usr/bin/env python
"""
Bot starting script
"""

import os
import sys

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
    add,
    recents,
    restart,
    get_all_items,
    get_item,
    get_item_quantity,
    items_usage,
    get_price,
    help_command,
    PRICE,
    QUANTITY,
    ALL_ITEMS,
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
    application.bot_data["restart"] = False

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
    bulk_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", add)],
        states={
            ALL_ITEMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_all_items)]
        },
        fallbacks=[MessageHandler(filters.TEXT, help_command)],
    )

    application.add_handler(conv_handler)
    application.add_handler(bulk_conv_handler)
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("recents", recents))
    application.add_handler(CommandHandler("items_usage", items_usage))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

    if application.bot_data["restart"]:
        os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == "__main__":
    main()
