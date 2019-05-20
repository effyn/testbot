import asyncio
import json
import os

import discord

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

    def get(self, key: str, default=None):
        try:
            return self._data[key]
        except KeyError:
            return default

    # use this if lookups are likely to miss
    def get2(self, key: str, default=None):
        if key in self._data:
            return self._data[key]
        return default

    def __setitem__(self, key: str, value):
        self._data[key] = value

    def __getitem__(self, key: str):
        return self.get(key)

class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        # pass along any supplied arguments
        super().__init__(*args, **kwargs)

        # dict for invoking commands
        self._commands = {}
        # a dict holding all bot data
        self.data = DB()
        self.data.load()

    def command(self, coroutine):
        # this is a decorator for commands.

        # all coroutines should accept:
        # - a discord.Message parameter
        # - the arguments passed to the command (as *args)
        # this will be enforced later; it's 1 AM right now
        # and i dont feel like sorting it out :P
        if not asyncio.iscoroutinefunction(coroutine):
            raise Exception("Command function is not a coroutine")

        self._commands[coroutine.__name__] = coroutine
        return coroutine

    def parse_message(self, prefix: str, message: discord.Message):
        # ignore bot's own messages
        if message.author == self.user:
            return None, None

        # NOTE: system_content keeps discord's formatting in tact
        # this could become confusing so im just making it clear
        pre = message.system_content.split(prefix, 1)

        # if there's content to the left (of the prefix)
        # or no content to the right, return None
        if pre[0] or not pre[1]:
            return None, None

        # split all tokens, including the command
        command_args = pre[1].split()

        try:
            # return the command and the rest of the tokens (args)
            return self._commands[command_args[0]], command_args[1:]
        except KeyError:
            # command was not found
            return None, None

    async def on_message(self, message: discord.Message):
        # for now, assume that "prefix" is likely not set, and default to "."
        command, args = self.parse_message(self.data.get2("prefix", "."), message)
        if command:
            await command(message, *args)

# initialize the bot
bot = Bot()

####################
# commands go here #
####################

@bot.command
async def test(message: discord.Message, *args):
    await message.channel.send("Testing!")

@bot.command
async def rem(message: discord.Message, *args):
    if len(args) < 1 or not args[0].isdigit():
        return await message.channel.send("Usage: `rem seconds (text)`")
    sent: discord.Message = await message.channel.send(":zzz:")
    await asyncio.sleep(int(args[0]))
    await sent.edit(content=f'{message.author.mention}\n:alarm_clock: {" ".join(args[1:])}')

# NOTE: this must always be the last line of the file, since it is a blocking operation
# run the bot
bot.run(token)
