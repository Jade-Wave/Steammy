from .bot.command_handler import main as bot_main


def main():
    return bot_main()


if __name__ == '__main__':
    bot = main()
    bot.run(bot.application_token)
