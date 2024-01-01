from .bot_base import BotBase


def populate_commands(bot):
    @bot.command(name="ping")
    async def ping(message):
        await message.channel.send("pong")

    @bot.command(name="help")
    async def help(message):
        await message.channel.send(f"**ping** - pong\n"
                                   f"**help** - show this message\n"
                                   f"**info** - LegoUkraineBot description\n")

    @bot.command(name="info")
    async def info(message):
        await message.channel.send(f"**LegoUkraineBot** is an interactive bot created "
                                   f"specifically for Lego Ukraine server")


def main():
    bot = BotBase()
    populate_commands(bot)
    return bot
