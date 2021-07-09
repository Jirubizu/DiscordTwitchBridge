import os
from twitchiobot import TwitchBot
from discord.ext import commands
from discord.message import Message

class DiscordBot(commands.Bot):
    def __init__(self):
        self.token = os.environ['BOT_TOKEN']
        self.channel_id = int(os.environ['BOT_CHANNEL_ID'])
        self.channel = None
        self.prefix = os.environ['BOT_PREFIX']
        self.twitch_bot: TwitchBot = None
        self.initialised = False
        super().__init__(command_prefix=self.prefix)

    def start(self):
        return super().start(self.token)

    async def on_ready(self):
        self.channel = self.get_channel(self.channel_id)
        print("Bot is ready")
        self.initialised = True

    async def on_message(self, message: Message):
        # If the twitch side is not initialised don't attpemt to do anything else.
        if not self.twitch_bot.initialised:
            return
        
        if message.channel.id != self.channel_id or message.webhook_id:
            return
        
        twitch_chat = self.twitch_bot.get_channel(os.environ['CHANNEL'])
        await twitch_chat.send(f"{message.author.display_name}:{message.content}")
