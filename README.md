# 🛒 Rashan Bot 🤖

## > Sorry, if this is a fast video as github won't let me upload longer videos.

https://github.com/progmatic-99/rashan/blob/master/rashan-fast-demo.mp4


> Rashan Bot is a Telegram bot designed to help you manage your expenses and track item usage conveniently within the Telegram app. With Rashan Bot, you can easily add, edit, delete expenses, view recent expenses, and track item usage in the current month.

## Features

📝 **Expense Management**:
- **/start**: Starts the bot & add single expense.
- **/add**: Add multiple expenses together.
- **/edit**: Edit an expense.
- **/delete**: Delete an expense.
- **/recents**: View recent expenses.

📊 **Item Usage Tracking**:
- **/items_usage**: Get item usage in the current month.

🆘 **Help**:
- **/help**: Get information about the bot.

## Database Usage

Rashan Bot utilizes the SQLite3 database to store expense entries. It follows the singleton pattern for the database connection, ensuring efficient and reliable data management.

## Getting Started

To use Rashan Bot, simply start a chat with the bot and use the provided commands to manage your expenses and track item usage.

## Installation

1. Clone the repository:

    `git clone https://github.com/progmatic-99/rashan`

2. Create a virtualenv & install dependencies:

    `python3 -m venv env && python3 -m pip install -r requirements.txt`

3. Set up your Telegram bot token in `config.py`.

4. Run the bot using: `python3 bot.py`
