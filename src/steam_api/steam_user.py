import datetime
import requests
import os
import pathlib

class SteamUser:

    def __init__(self, user_dict, user_tag):
        for key in user_dict.keys():
            self.__setattr__(key, user_dict[key])
        self.tag = user_tag
        if "lastlogoff" in self.__dict__.keys():
            self.lastlogoff = datetime.datetime.fromtimestamp(user_dict['lastlogoff'])
        else:
            self.lastlogoff = "Unknown"

        self.resources_folder = pathlib.Path.joinpath(
            pathlib.Path(__file__).parent.resolve().parent.resolve(),
            "resources"
        )

        self.games = []

    def get_top_games(self, amount):
        result = ""
        games = sorted(self.games, key=lambda game: game.playtime_forever)[::-1]
        top_5 = games[:5]
        for game in top_5:
            result += (f"-----------------------------\n"
                       f"**Name**: {game.name}\n"
                       f"**Total playtime**: {round(game.playtime_forever / 60,2)}\n")

        return result

    def save_avatar(self):
        if not os.path.exists(self.resources_folder):
            os.mkdir(self.resources_folder)
        avatar_data = requests.get(url=self.avatarfull)
        avatar_path = pathlib.Path.joinpath(self.resources_folder, f'{self.tag}.jpg')
        if not os.path.exists(avatar_path):
            with open(avatar_path, 'wb') as avatar_file:
                avatar_file.write(avatar_data.content)
        return avatar_path

    def pretty_print(self):
        return (f"**User tag**: {self.tag}\n"
                f"**Visible name**: {self.personaname}\n"
                f"**SteamID**: {self.steamid}\n"
                f"**Last time online**: {self.lastlogoff}"
                )

