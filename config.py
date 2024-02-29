"""Environment Config"""

import os
from dotenv import dotenv_values

if os.environ.get("DEPLOYMENT") == "PROD":
    bot_token = os.environ.get("ACCESS_TOKEN")
else:
    config = dotenv_values(".env")
    bot_token = config["ACCESS_TOKEN"]
    usernames = config["USERNAMES"]
