"""Logger"""
import logging


LOG_FMT = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
    filename="./bot.log",
    filemode="w+",
)
# set higher logging level for httpx to avoid all GET & POST reqs being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(LOG_FMT)
logging.getLogger(__name__).addHandler(console)

logger = logging.getLogger(__name__)
