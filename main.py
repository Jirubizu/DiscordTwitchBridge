from twitchiobot import TwitchBot
from discordbot import DiscordBot
import asyncio


def run():
    twitch_bot = TwitchBot()
    discord_bot = DiscordBot()

    discord_bot.twitch_bot = twitch_bot

    loop = asyncio.get_event_loop()
    task1 = loop.create_task(twitch_bot._connection._connect())
    task2 = loop.create_task(discord_bot.start())
    gathered = asyncio.gather(task1, task2, loop=loop)
    loop.run_until_complete(gathered)


if __name__ == "__main__":
    run()
