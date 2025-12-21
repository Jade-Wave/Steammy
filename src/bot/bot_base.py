from discord import Intents, File
from discord.ext import commands
import dotenv

import os


class BotBase(commands.Bot, commands.Cog):
    def __init__(self):
        super(BotBase, self).__init__(intents=Intents.all(), command_prefix="!", help_command=None)
        dotenv.load_dotenv()
        self.application_token = os.getenv("BOT_BASE")
