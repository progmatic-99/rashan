"""Environment Config"""

from dotenv import dotenv_values


config = dotenv_values(".env")
bot_token = config["ACCESS_TOKEN"]
usernames = config["USERNAMES"]
