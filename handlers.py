"""Handlers for bot commands"""


from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from db import DB
from logger import logger


ITEM, QUANTITY, PRICE = range(3)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Start command"""
    start_text = """What did you buy today??"""
    curr_user = update.message.from_user.username
    ctx.user_data["curr_user"] = curr_user

    logger.info("Conversation started with '%s'", curr_user)
    await update.message.reply_text(start_text)

    return ITEM


async def get_item(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Getting the item"""
    item = update.message.text
    user = ctx.user_data["curr_user"]
    ctx.user_data["item"] = item

    logger.info("'%s' added '%s'", user, item)
    await update.message.reply_text("How many did you buy??")

    return QUANTITY


async def get_item_quantity(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Getting the item"""
    quantity = update.message.text
    item = ctx.user_data["item"]
    user = ctx.user_data["curr_user"]
    ctx.user_data["quantity"] = quantity

    logger.info("'%s' bought '%s' of '%s'", user, quantity, item)
    await update.message.reply_text(f"How much did you buy {item} for??")

    return PRICE


async def get_price(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Gets the price of the item"""
    user = update.message.from_user.username
    price = update.message.text
    ctx.user_data["price"] = price
    quantity = ctx.user_data["quantity"]
    item = ctx.user_data["item"]
    price_text = f"{user} added {quantity} of {item} for '₹{price}'"

    logger.info(price_text)
    db = DB()
    db.add_item(ctx.user_data)
    await update.message.reply_text(price_text)

    return ConversationHandler.END


async def help_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    curr_user = update.message.from_user.username
    logger.info("'%s' accessed /help command!!", curr_user)

    await update.message.reply_text("Use /start to test this bot.")
