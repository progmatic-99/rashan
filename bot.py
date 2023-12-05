import asyncio
import telegram
from dotenv import dotenv_values

config = dotenv_values(".env")


async def main():
    bot = telegram.Bot(config["ACCESS_TOKEN"])

    async with bot:
        print(await bot.get_me())


if __name__ == "__main__":
    asyncio.run(main())
