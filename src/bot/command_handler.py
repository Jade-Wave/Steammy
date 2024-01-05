from .bot_base import BotBase
import discord.ext.commands.context
from SteamTrackerBot.src.steam_api.basic_connection import SteamIntegration


def setup_steam(bot):
    bot.steam_integration = SteamIntegration()


def populate_commands(bot):
    @bot.command(name="ping")
    async def ping(message):
        await message.channel.send("pong")

    @bot.command(name="help")
    async def help(message):
        await message.channel.send(f"**ping** - pong\n"
                                   f"**help** - show this message\n"
                                   f"**info** - SteamTrackerBot description\n")

    @bot.command(name="info")
    async def info(message):
        await message.channel.send(f"**SteamTrackerBot** is an interactive bot created "
                                   f"for tracking different Steam stuff")

    @bot.command(name="search_user")
    async def search_user(message):
        await message.channel.send(
            f"Searching: {message.message.content.replace('!search_user ', '')},\n"
            f"Response is: "
            f"{bot.steam_integration.users.search_user(message.message.content.replace('!search_user ', ''))}"
        )


def main():
    bot = BotBase()
    setup_steam(bot)
    populate_commands(bot)
    return bot
