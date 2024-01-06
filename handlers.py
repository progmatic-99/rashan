"""Handlers for bot commands"""


from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from config import usernames
from logger import logger


ITEM, PRICE = range(2)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Start command"""
    start_text = """What did you buy today??"""
    curr_user = update.message.from_user.username
    ctx.user_data["curr_user"] = curr_user

    if curr_user in usernames:
        logger.info("Conversation started with '%s'", curr_user)
        await update.message.reply_text(start_text)
    else:
        logger.info("Invalid user: %s", curr_user)
        await update.message.reply_text("Not allowed, try /help !!")

    return ITEM


async def help_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""

    await update.message.reply_text("Use /start to test this bot.")


async def get_item(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Getting the item"""
    item = update.message.text
    user = ctx.user_data["curr_user"]
    ctx.user_data["item"] = item

    logger.info("'%s' added '%s'", user, item)
    await update.message.reply_text(f"How much did you buy {item} for??")

    return PRICE


async def get_price(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Gets the price of the item"""
    user = update.message.from_user.username
    price = update.message.text
    ctx.user_data["price"] = price
    price_text = "'%s' added '%s' for '₹%s'" % (user, ctx.user_data["item"], price)

    logger.info(price_text)
    await update.message.reply_text(price_text)

    return ConversationHandler.END
