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
    async def search_by_tag(message):
        username = message.message.content.replace('!search_user ', '')
        user = bot.steam_integration.get_steam_user(username)
        if user != "The user was not found":
            print_data = user.pretty_print()
            avatar = discord.File(user.save_avatar())
        else:
            print_data = str(user)
            avatar = None
        await message.send(
            f"Searching: {username}:\n{print_data}\n",
            file=avatar
        )


def main():
    bot = BotBase()
    setup_steam(bot)
    populate_commands(bot)
    return bot
