"""Handlers for bot commands"""


import sqlite3
import re
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from db import DB, BulkItemStructure
from logger import logger


ITEM, ALL_ITEMS, QUANTITY, PRICE = range(4)


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Start command"""
    start_text = """What did you buy today??"""
    curr_user = update.message.from_user.username
    ctx.user_data["curr_user"] = curr_user

    logger.info("Conversation started with '%s'", curr_user)
    await update.message.reply_text(start_text)

    return ITEM


async def add(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Gets the data in bulk"""
    helper_text = """Add multiple items in this format, separated by newline:
        item_name_1 quantity_1 price_1
        item_name_2 quantity_2 price_2
        ...
        item_name_n quantity_n price_n
    """
    curr_user = update.message.from_user.username
    ctx.user_data["curr_user"] = curr_user

    logger.info("Conversation started with '%s'", curr_user)
    await update.message.reply_text(helper_text)

    return ALL_ITEMS


async def get_all_items(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Parse all the items
    - item_name: str
    - quantity: text (1kg, 1, 1L)
    - price: int
    """
    user = update.message.from_user.username
    user_input = update.message.text.strip().split("\n")
    print(user_input)
    all_items: BulkItemStructure = []

    for item_data in user_input:
        cleaned_data = re.sub(r"\s+", " ", item_data)
        print(cleaned_data)
        name, quantity, price = cleaned_data.split()
        print(name, quantity, price)
        if not price.isdigit() and price <= 0:
            await update.message.reply_text(f"Enter valid price for {name}")
            return ALL_ITEMS

        all_items.append((name, quantity, price))
        print(all_items)

    db = DB()

    try:
        db.add_bulk_items(all_items)
        logger.info("'%s' added multiple items.", user)
    except sqlite3.Error as e:
        logger.error(e)
        await update.message.reply_text(e)
        return ALL_ITEMS

    return ConversationHandler.END


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

    logger.info("'%s' bought '%s' '%s'", user, quantity, item)
    await update.message.reply_text(f"How much did you buy {item} for??")

    return PRICE


async def get_price(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Gets the price of the item"""
    user = update.message.from_user.username
    price = update.message.text

    if not price.isdigit() and price <= 0:
        await update.message.reply_text("Enter valid price!!")
        return PRICE

    ctx.user_data["price"] = price
    quantity = ctx.user_data["quantity"]
    item = ctx.user_data["item"]
    price_text = f"{user} added {quantity} {item} for '₹{price}'"

    db = DB()

    try:
        db.add_item(ctx.user_data)
        logger.info(price_text)
    except sqlite3.Error as e:
        logger.error(e)
        await update.message.reply_text(e)
        return PRICE

    await update.message.reply_text(price_text)

    return ConversationHandler.END


async def help_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""

    help_text = """
    /start -> To add a single item
    /add -> To add multiple items
    /help -> show you this output```
    """

    await update.message.reply_text(help_text)


async def restart(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Restarts the bot"""
    ctx.bot_data["restart"] = True

    await update.message.reply_text("Restarting the bot!!")
    ctx.application.stop_running()
