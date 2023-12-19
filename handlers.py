"""Handlers for bot commands"""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from config import usernames


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command"""

    keyboard = [
        [
            InlineKeyboardButton("Add Expenses", callback_data="1"),
            InlineKeyboardButton("Edit Expenses", callback_data="2"),
        ],
        [
            InlineKeyboardButton("Delete Expenses", callback_data="3"),
            InlineKeyboardButton("Recent Expenses", callback_data="4"),
        ],
        [InlineKeyboardButton("Help", callback_data="5")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    curr_user = update.message.from_user.username

    if curr_user in usernames:
        await update.message.reply_text("Please choose:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Not allowed, try /help !!")


async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()

    await query.edit_message_text(text=f"Selected option: {query.data}")


async def help_command(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")
