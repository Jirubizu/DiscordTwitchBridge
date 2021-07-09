from discordbot import DiscordBot
from discord.webhook import RequestsWebhookAdapter, Webhook
from twitchio.chatter import Chatter
from twitchio.ext import commands
from twitchio.user import User
import os

class TwitchBot(commands.Bot):
    def __init__(self):
        super().__init__(token=os.environ['TMI_TOKEN'],
                         client_secret=os.environ['CLIENT_ID'],
                         prefix=os.environ['BOT_PREFIX'],
                         initial_channels=[os.environ['CHANNEL']])
        self.webhook_id = os.environ['WEBHOOK_ID']
        self.webhook_token = os.environ['WEBHOOK_TOKEN']
        self.initialised = False
        self.user_profiles = {}

    async def event_ready(self):
        print(f"{os.environ['BOT_NICK']} is online!")
        self.initialised = True

    async def event_message(self, message):
        chatter: Chatter = message.author
        # make sure the bot ignores itself
        if message.echo:
            return
        
        # Add to memory pool to prevent multiple requests
        if not self.user_profiles[chatter.name]:
            self.user_profiles[chatter.name] = await chatter.user()

        #Send message to discord via webhook
        webhook_client = Webhook.partial(int(self.webhook_id),
                                         self.webhook_token,
                                         adapter=RequestsWebhookAdapter())
        username = self.build_username(chatter)
        webhook_client.send(message.content,
                            username=username,
                            avatar_url=self.user_profiles[chatter.name].profile_image)

    def build_username(self, chatter: Chatter):
        username = ""
        if chatter.is_mod:
            username += "[MOD]"
        if chatter.is_subscriber:
            username += "[SUB]"

        return username + " " + chatter.display_name
