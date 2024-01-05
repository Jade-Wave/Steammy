import steam


class SteamIntegration(steam.Steam):
    def __init__(self):
        key = "CA3C1B047F7F4EB60DEF412D4AAD9595"
        super(SteamIntegration, self).__init__(key)
        self.users.search_user(search="hh_u_mm_a_nn")
