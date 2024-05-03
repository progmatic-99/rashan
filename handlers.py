"""Handlers for bot commands"""

import sqlite3
from datetime import datetime
import prettytable as pt
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from db import DB, BulkItemStructure
from utils import parse_item_info, format_time
from logger import logger


ITEM, ALL_ITEMS, QUANTITY, PRICE, SEARCH = range(5)


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
    """
    Parse all the items
    - item_name: str
    - quantity: text (1kg, 1, 1L)
    - price: int
    """
    user = update.message.from_user.username
    user_input = update.message.text.strip().split("\n")
    all_items: BulkItemStructure = []

    for item_data in user_input:
        cleaned_data = parse_item_info(item_data)
        name = cleaned_data["item_name"]
        quantity = cleaned_data["quantity"]
        price = cleaned_data["price"]

        if not price.isdigit() and int(price) <= 0:
            await update.message.reply_text(f"Enter valid price for {name}")
            return ALL_ITEMS

        all_items.append((name, quantity, price))

    db = DB()

    try:
        db.add_bulk_items(all_items)
        logger.info("'%s' added multiple items.", user)

        table = pt.PrettyTable(["Name", "Quantity", "Price"])
        total_price = 0
        for item in all_items:
            name, quantity, price = item
            total_price += int(price)
            table.add_row([name, quantity, price])

        await update.message.reply_text(
            f"Following items were added by {user}:\n```{table}```\nTotal Price: {total_price}",
            parse_mode="MarkdownV2",
        )
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
    """Getting the item quantity"""

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

    if not price.isdigit() and int(price) <= 0:
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


async def recents(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Get the recently added 5 items"""
    db = DB()
    items = None
    curr_user = update.message.from_user.username

    try:
        items = db.recent_items()
    except sqlite3.Error as e:
        logger.error(e)
        await update.message.reply_text(e)

    if not isinstance(items, str):
        table = pt.PrettyTable(["Name", "Quantity", "Price", "Time"])
        for name, quantity, price, time in items:
            # sqlite3 returns a str for datetime
            time = format_time(time)

            table.add_row([name, quantity, price, time])

        logger.info("Recent items table sent to '%s'", curr_user)
        await update.message.reply_text(f"```{table}```", parse_mode="MarkdownV2")
    else:
        logger.info("No recent items in db!!")
        await update.message.reply_text(items)


async def items_usage(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Get the item monthly stats from data"""

    # month & year needs to be in str
    curr_month = datetime.now().strftime("%m")
    curr_year = datetime.now().strftime("%Y")
    curr_user = update.message.from_user.username

    db = DB()
    try:
        result = db.get_monthly_usage(curr_month, curr_year)
    except sqlite3.Error as e:
        logger.error(e)
        await update.message.reply_text(e)

    if not isinstance(result, str):
        table = pt.PrettyTable(["Name", "Total Quantity", "Total Price"])
        for name, quantity, price in result:
            table.add_row([name, quantity, price])

        logger.info("Monthly item usage sent to %s.", curr_user)
        await update.message.reply_text(f"```{table}```", parse_mode="MarkdownV2")
    else:
        logger.info("No recent result in db!!")
        await update.message.reply_text(result)


async def help_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""

    help_text = """
/start: To add a single item
/add: To add multiple items
/recents: To show recently added items
/search: To show last purchased info of an item
/items_usage: Gets all items usage in the current month
/help : show you this output
    """

    await update.message.reply_text(f"```{help_text}```", parse_mode="MarkdownV2")


async def restart(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Restarts the bot"""
    ctx.bot_data["restart"] = True
    curr_user = update.message.from_user.username

    logger.info("'%s' restarted the bot!!", curr_user)
    await update.message.reply_text("Restarting the bot!!")
    ctx.application.stop_running()


async def search(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Searches the item & returns the latest entry"""
    text = "Provide item name.."
    curr_user = update.message.from_user.username
    ctx.user_data["curr_user"] = curr_user

    logger.info("Search started with '%s'", curr_user)
    await update.message.reply_text(text)

    return SEARCH


async def last_purchased_item(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> int:
    """Gets the last purchased date of item"""
    item = update.message.text.strip()
    curr_user = update.message.from_user.username

    if item:
        db = DB()
        try:
            result = db.search_item(item)
        except sqlite3.Error as e:
            logger.error(e)
            await update.message.reply_text(e)

        if not isinstance(result, str):
            table = pt.PrettyTable(["Name", "Quantity", "Price", "Time"])
            for name, quantity, price, time in result:
                time = format_time(time)
                table.add_row([name, quantity, price, time])

            logger.info("Item last purchased info sent to %s.", curr_user)
            await update.message.reply_text(f"```{table}```", parse_mode="MarkdownV2")
        else:
            logger.info("No recent result in db!!")
            await update.message.reply_text(result)

        return ConversationHandler.END
    else:
        await update.message.reply_text("Enter valid item!!")
        return SEARCH
