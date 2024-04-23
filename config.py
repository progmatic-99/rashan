"""Environment Config"""

from dotenv import dotenv_values

config = dotenv_values(".env")

DB_PATH = "./rashan.sqlite"

if "DEPLOYMENT" in config:
    bot_token = config["ACCESS_TOKEN"]
    DB_PATH = "/home/ec2-user/rashan.sqlite3"
else:
    bot_token = config["ACCESS_TOKEN_DEV"]
