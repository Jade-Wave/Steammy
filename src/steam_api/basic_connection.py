import steam

from .steam_user import SteamUser

class SteamIntegration(steam.Steam):
    def __init__(self):
        key = "CA3C1B047F7F4EB60DEF412D4AAD9595"
        super(SteamIntegration, self).__init__(key)
        self.located_users = {}

    def get_steam_user(self, username, steamid):
        if username not in self.located_users.keys():
            user = self.users.search_user(search=username)
            if user == "No match":
                return "The user was not found"
            steam_user = SteamUser(user_dict=user['player'], user_tag=username)
            self.located_users[username] = steam_user
        return self.located_users[username]
