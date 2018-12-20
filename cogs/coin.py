"""This is a cog for a discord.py bot.
It adds a currency which can be transfered

Commands:


"""

from discord.ext import commands
from discord import Member
import asyncio


class Coin():
    def __init__(self, client):
        self.client = client
        self.logo = open("data/logo.txt", "r").read()

    #chad coin group
    @commands.group(
        name='coin',  # if this is omitted the function name will be used
        brief='Access the features of Chad Coin',  # shown when users execute "help"
        description='How to use chad coin',  # shown when users execute "help example"
        aliases=['c']  # alternative ways to execute the command
    )
    async def coin(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("Incorrect usage you dumb monkey! type `chad help coin` for more info")

    @coin.command(
        name='info',  # if this is omitted the function name will be used
        brief='Gets info about Chad Coin',  # shown when users execute "help"
        description='Usage: chad coin info',  # shown when users execute "help example"
    )
    async def info(self, ctx, *args):
        logocopy = self.logo
        await ctx.channel.send(logocopy)

    @coin.command(
        name='give',  # if this is omitted the function name will be used
        brief='Give Chad Coin to someone',  # shown when users execute "help"
        description='Usage: chad coin give amount @mention'  # shown when users execute "help example"
    )
    async def give(self, ctx, *args):
        print(len(args))
        await ctx.channel.send(f'{args[0]} {args[1]}')


def setup(client):
    client.add_cog(Coin(client))