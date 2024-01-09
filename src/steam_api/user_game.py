from steam.apps import Apps

class UserGame(Apps):
    def __init__(self, game_dict, client):
        super(UserGame, self).__init__(client=client)
        for key in game_dict.keys():
            self.__setattr__(key, game_dict[key])