"""Environment Config"""

import os
from dotenv import dotenv_values

if os.environ.get("DEPLOYMENT") == "PROD":
    bot_token = os.environ.get("ACCESS_TOKEN")
    db_path = "/var/db/rashan.sqlite3"
else:
    config = dotenv_values(".env")
    bot_token = config["ACCESS_TOKEN"]
    usernames = config["USERNAMES"]
