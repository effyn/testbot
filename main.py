import discord
import json
import os
from asyncio import iscoroutinefunction as is_a_coroutine

# set the working directory to this file's directory
# this makes loading files a lot easier
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("token.txt") as f:
    token = f.read()

class DB:
    # change the path if you want to, defaults to data.json
    def __init__(self, path: str = "data.json"):
        self.path = path
        self._data: dict = None

    def load(self) -> dict:
        try:
            with open(self.path) as f:
                self._data = json.load(f)
        except FileNotFoundError:
             self._data = {}

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self._data, f)

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def __getitem__(self, key: str):
        try:
            return self._data[key]
        except KeyError:
            return None

class Bot(discord.Client):
    async def on_message(self, message: discord.Message):
        # do nothing for now
        pass

# initialize the bot and "database" hAhAhaHaHaH
bot, commands, db = Bot(), DB()

# commands go here
# there will be a decorator for registering them (@bot.command)

# load from the "database" file
db.load()

# run the bot
bot.run(token)