import datetime
import threading
import asyncio
from typing import Sequence

import steam

from Steammy.src.bot.bot_base import BotBase
import discord.ext.commands.context
import discord.ext.tasks
from discord.message import Message
from Steammy.src.steam_api.basic_connection import SteamIntegration


def setup_steam(bot):
    bot.steam_integration = SteamIntegration()


def populate_commands(bot):
    @bot.command(name="ping")
    async def ping(message: Message):
        await message.channel.send("pong")

    @bot.command(name="help")
    async def help(message: Message):
        await message.channel.send(f"----**STEAMMY**----\n\n"
                                   f"_command prefix_ - !\n\n"
                                   f"**ping** - pong\n"
                                   f"**help** - Show this message\n"
                                   f"**info** - Steammy description\n"
                                   f"**search_user** - Find Steam user\n"
                                   f"**top_played** - User's top played games\n"
                                   f"    _steam64id_ - Steam user 64ID\n"
                                   f"    _number_ - [optional] number of games to show (default 5)\n"
                                   f"**app_details** - Get app details for a given <country> (default is UA)\n"
                                   f"    _Name/GameID_ - Game ID/Name\n"
                                   f"    country _<UA>_ - [optional] \"country\" + country code to track price in\n"
                                   f"**register_tracker** - register your server (guild) for game tracker."
                                   f"This action is mandatory for game tracking\n"
                                   f"**start_tracker** - Start Steam sale tracker\n"
                                   f"**stop_tracker** - Stop Steam sale tracker\n"
                                   f"**track_game** - Track Steam sale of a given game in a given country\n"
                                   f"    _Name/GameID_ - Game ID/Name\n"
                                   f"    country _<UA>_ - [optional] \"country\" + country code to track price in\n"
                                   f"**untrack_game** - Stop tracking Steam sale of a given game in a given country\n"
                                   f"    _Name/GameID_ - Game ID/Name\n"
                                   f"    country _<UA>_ - [optional] \"country\" + country code to track price in\n"
                                   f"**list_track** - Show all tracked games\n"
                                   f"**track_now** - Show sales for tracked games without need to wait\n"
                                   )

    @bot.command(name="info")
    async def info(message: Message):
        await message.channel.send(f"Hey, I'm **Steammy** - an interactive bot created "
                                   f"for tracking different Steam stuff")

    @bot.command(name="search_user")
    async def search_user(message: Message):
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
    async def top_played(message: Message):
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
    async def app_details(message: Message):
        content = message.message.content.replace('!app_details ', '')
        parsed = content.split(' country ')
        game = parsed[0]
        country = "UA"
        if len(parsed) > 1:
            country = parsed[1]
        await message.send(
            f"{bot.steam_integration.get_application_info(game, country)}"
        )

    @discord.ext.tasks.loop(hours=2)
    async def discounter(message: Message):
        result = bot.steam_integration.run_discount_check(message)
        if result != "":
            await message.send(f"{result}")

    @bot.command(name="register_tracker")
    async def register_tracker(message: Message):
        await message.send(
            f"{bot.steam_integration.register_guild_tracker(message)}"
        )

    @bot.command(name="start_tracker")
    async def start_tracker(message: Message):
        if discounter.is_running():
            await message.send("Tracker is already running")
        discounter.start(message)
        await message.send(
            f"Successfully started tracker"
        )

    @bot.command(name="stop_tracker")
    async def stop_tracker(message: Message):
        if not discounter.is_running():
            await message.send("Tracker is not running")
        discounter.stop()
        await message.send("Successfully stopped tracker")

    @bot.command(name="track_game")
    async def track_game(message: Message):
        content = message.message.content.replace('!track_game ', '')
        parsed = content.split(' country ')
        game = parsed[0]
        country = "UA"
        if len(parsed) > 1:
            country = parsed[1]
        await message.send(f"{bot.steam_integration.add_game_for_track(message, game, country)}")

    @bot.command(name="untrack_game")
    async def untrack_game(message: Message):
        content = message.message.content.replace('!untrack_game ', '')
        await message.send(f"{bot.steam_integration.remove_game_for_track(message, content)}")

    @bot.command(name="list_track")
    async def list_track(message: Message):
        await message.send(bot.steam_integration.see_games_on_track(message))

    @bot.command(name="track_now")
    async def track_now(message: Message):
        result = bot.steam_integration.run_discount_check(message)
        if result != "":
            await message.send(f"{result}")
        else:
            await message.send("No games are being tracked or there are no sales going on at the moment")


def main():
    bot = BotBase()
    setup_steam(bot)
    populate_commands(bot)
    bot.apps = steam.Apps(bot)
    return bot
