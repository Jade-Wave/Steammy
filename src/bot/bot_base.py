from discord import Intents, File
from discord.ext import commands


class BotBase(commands.Bot):
    def __init__(self):
        super(BotBase, self).__init__(intents=Intents.all(), command_prefix="!", help_command=None)
        self.application_token = "MTE5MTUwMDcyMTQwNTgyNTEwNg.GCnvQC.2XT-zZql3zuEEMipKC8PApe8XzauAjEXJMXoMg"

