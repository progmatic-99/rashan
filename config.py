"""Environment Config"""

import os
from dotenv import dotenv_values

config = dotenv_values(".env")
bot_token = config["ACCESS_TOKEN"]
deployment = config["DEPLOYMENT"] or None

db_path = "/home/ec2-user/rashan.sqlite3" if deployment else "./rashan.sqlite"

