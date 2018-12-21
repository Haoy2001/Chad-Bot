from discord.ext import commands
from datetime import datetime as dt
import random
import re


class Uwu():
    def __init__(self, client):
        self.client = client

    async def on_message(self, msg):
        #print(msg)
        pass
def setup(client):
    client.add_cog(Uwu(client))