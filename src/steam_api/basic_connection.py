import asyncio
import datetime
import time
import steam
import pathlib
import os
from discord.message import Message

import threading

from Steammy.src.steam_api.steam_user import SteamUser
from Steammy.src.steam_api.user_game import UserGame


class SteamIntegration(steam.Steam):
    def __init__(self):
        self.game_track = None
        self.serializer_file = None
        self.resources_folder = pathlib.Path.joinpath(
            pathlib.Path(__file__).parent.resolve().parent.resolve(),
            "resources"
        )
        key = "CA3C1B047F7F4EB60DEF412D4AAD9595"
        super(SteamIntegration, self).__init__(key)
        self.located_users = {}
        self.break_the_cycle = False
        try:
            self.run_loop = asyncio.get_running_loop()
        except RuntimeError:
            self.run_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.run_loop)
        self.message = None

    def get_app_id(self, game, country):
        found_games = self.apps.search_games(game, country=country)['apps']
        if len(found_games) == 0:
            return f"Did not find any games that match: {game}"
        game_id = found_games[0]['id'][0]
        return game_id

    def see_games_on_track(self, message: Message):
        self.serializer_file = f"{self.resources_folder}/{message.guild.id}.tracker"
        with open(self.serializer_file, "r") as reader:
            self.game_track = [game.strip().split(":") for game in reader.readlines()]

        output = ""
        for appid, country in self.game_track:
            game_data = self.apps.get_app_details(
                app_id=appid,
                country=country,
                filters=f"basic,price_overview,screenshots"
            )
            game_data = game_data[str(appid)]['data']
            output += f"**Name**: {game_data['name']}, **Country**: {country}\n"
        return output if output != "" else "No games are tracked for this guild"

    def add_game_for_track(self, message: Message, game, country="UA"):
        self.serializer_file = f"{self.resources_folder}/{message.guild.id}.tracker"
        with open(self.serializer_file, "r") as reader:
            self.game_track = [game.strip().split(":") for game in reader.readlines()]

        if not game.isdigit():
            game = self.get_app_id(game, country)

        if [game, country] not in self.game_track:
            self.game_track.append([game, country])

            with open(self.serializer_file, "w") as writer:
                for this_game in self.game_track:
                    writer.write(f"{':'.join([str(this_game[0]), str(this_game[1])])}\n")

            return f'Successfully added {game} to track list'
        else:
            return f"{game} is already tracked"

    def remove_game_for_track(self, message: Message, game):
        self.serializer_file = f"{self.resources_folder}/{message.guild.id}.tracker"
        with open(self.serializer_file, "r") as reader:
            self.game_track = [game.strip().split(":") for game in reader.readlines()]

        if not game.isdigit():
            game = self.get_app_id(game, country="UA")

        for track_game in self.game_track:
            if game == track_game[0]:
                self.game_track.remove(track_game)

                with open(self.serializer_file, "w") as writer:
                    for this_game in self.game_track:
                        writer.write(f"{':'.join([str(this_game[0]), str(this_game[1])])}\n")

                return f"Successfully untracked {game}"
        return f"{game} is not tracked. Could not untrack"

    def clear_tracking_list(self, message: Message):
        self.serializer_file = f"{self.resources_folder}/{message.guild.id}.tracker"
        self.game_track = []
        with open(self.serializer_file, "w") as nothing:
            pass
        return "Successfully cleared tracking list"

    def stop_tracking(self):
        self.break_the_cycle = True
        return "Tracker is stopping"

    def run_discount_check(self, message: Message):
        self.serializer_file = f"{self.resources_folder}/{message.guild.id}.tracker"
        with open(self.serializer_file, "r") as reader:
            self.game_track = [game.strip().split(":") for game in reader.readlines()]
        app_sales = ""
        for appid, country in self.game_track:
            game_data = self.apps.get_app_details(
                app_id=appid,
                country=country,
                filters=f"basic,price_overview,screenshots"
            )

            game_data = game_data[str(appid)]['data']
            game_price_info = game_data["price_overview"]
            if game_price_info['discount_percent'] > 0:
                app_sales += (f"**{game_data['name']}**:\n"
                              f"    **Original price**: {game_price_info['initial_formatted']}\n"
                              f"    **Price on sale**: {game_price_info['final_formatted']}\n"
                              f"    **Discount**: -{game_price_info['discount_percent']}%\n\n")
        return app_sales

    def register_guild_tracker(self, message: Message):
        self.serializer_file = f"{self.resources_folder}/{message.guild.id}.tracker"
        if not os.path.exists(self.serializer_file):
            with open(self.serializer_file, "w") as nothing:
                pass
            return f"Guild {message.guild.name} (ID {message.guild.id}) was successufully registered"
        else:
            return f"Guild {message.guild.name} (ID {message.guild.id}) is already registered"

    def get_application_info(self, game, country="UA"):
        if not game.isdigit():
            game = self.get_app_id(game, country)
        game_data = self.apps.get_app_details(
            app_id=game,
            country=country,
            filters=f"basic,price_overview,screenshots"
        )

        game_data = game_data[str(game)]['data']

        output = (f"**Name**: {game_data['name']}\n"
                  f"**AppID**: {game_data['steam_appid']}\n"
                  # f"**Generic info**: {game_data['about_the_game']}\n"
                  f"**Price**: {game_data['price_overview']['final_formatted']}\n")

        if game_data['price_overview']['discount_percent'] > 0:
            output += (f"**=====SALE=====**\n"
                       f"    __Original price__:      {game_data['price_overview']['initial_formatted']}\n"
                       f"    __Sale percentage__: -{game_data['price_overview']['discount_percent']}%")

        return output

    def get_steam_user(self, key):
        if key not in self.located_users.keys():
            if key.isdigit():
                user = self.users.get_user_details(steam_id=key)
                if not user:
                    return "The user was not found"
                steam_user = SteamUser(user_dict=user['player'], user_tag="Unknown")
                self.located_users[steam_user.steamid] = steam_user
            else:
                user = self.users.search_user(search=key)
                if user == "No match":
                    return "The user was not found"
                steam_user = SteamUser(user_dict=user['player'], user_tag=key)
                key = steam_user.steamid
                self.located_users[steam_user.steamid] = steam_user
        return self.located_users[key]

    def top_played_games(self, steamid, amount=5):
        if steamid not in self.located_users.keys():
            self.get_steam_user(steamid)
        generic_data = self.users.get_owned_games(steam_id=steamid, include_appinfo=True, includ_free_games=True)
        total_games = generic_data['game_count']
        games_owned = generic_data['games']
        self.located_users[steamid].games = [UserGame(game, self) for game in games_owned]

        output = f"Total games owned: {total_games}\n"
        output += self.located_users[steamid].get_top_games(amount=amount)

        return output
