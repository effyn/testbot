import discord
import json
import os


# set the working directory to this file's directory
# this makes loading files a lot easier
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("token.txt") as f:
    token = f.read()

class Bot(discord.Client):
    async def on_message(self, message: discord.Message):
        # do nothing for now
        pass

# start the bot
bot = Bot()
bot.run(token)