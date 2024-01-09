import threading
import asyncio

import steam

from Steammy.src.bot.bot_base import BotBase
import discord.ext.commands.context
import discord.ext.tasks
from Steammy.src.steam_api.basic_connection import SteamIntegration


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

    @bot.command(name="top_played")
    async def top_played(message):
        content = message.message.content.replace('!top_played ', '')
        parsed = content.split(" ")
        amount = 5
        steamid = parsed[0]
        if len(parsed) > 1:
            amount = int(parsed[1])
        await message.send(
            f"5 owned games:\n"
            f"{bot.steam_integration.top_played_games(steamid=steamid, amount=amount)}"
        )

    @bot.command(name="app_details")
    async def app_details(message):
        content = message.message.content.replace('!app_details ', '')
        parsed = content.split(' country ')
        game = parsed[0]
        country = "UA"
        if len(parsed) > 1:
            country = parsed[1]
        await message.send(
            f"{bot.steam_integration.get_application_info(game, country)}"
        )

    @discord.ext.tasks.loop(minutes=1)
    async def discounter(message):
        result = bot.steam_integration.run_discount_check()
        if result != "":
            await message.send(f"{result}")

    @bot.command(name="start_tracker")
    async def start_tracker(message):
        discounter.start(message)
        await message.send(
            f"Successfully started tracker"
        )

    @bot.command(name="stop_tracker")
    async def stop_tracker(message):
        discounter.stop()
        await message.send("Successfully stopped tracker")

    @bot.command(name="track_game")
    async def track_game(message):
        content = message.message.content.replace('!track_game ', '')
        parsed = content.split(' country ')
        game = parsed[0]
        country = "UA"
        if len(parsed) > 1:
            country = parsed[1]
        await message.send(f"{bot.steam_integration.add_game_for_track(game, country)}")

    @bot.command(name="untrack_game")
    async def untrack_game(message):
        content = message.message.content.replace('!untrack_game ', '')
        await message.send(f"{bot.steam_integration.remove_game_for_track(content)}")

    @bot.command(name="list_track")
    async def list_track(message):
        await message.send(bot.steam_integration.see_games_on_track())


def main():
    bot = BotBase()
    setup_steam(bot)
    populate_commands(bot)
    bot.apps = steam.Apps(bot)
    return bot
