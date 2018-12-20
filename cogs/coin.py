"""This is a cog for a discord.py bot.
It adds a currency which can be transfered

Commands:


"""

from discord.ext import commands
from discord import Member
import asyncio
import json

class Coin():
    def __init__(self, client):
        self.client = client
        
        #load data
        try:
            coin = open("data/coin.json", "r")
            self.balances = json.load(coin)
            coin.close()
        except IOError:
            print("Fatal Error: Balances could not be read")
            self.client.logout()


    def updateData(self):
        try:
            coin = open("data/coin.json", "w")
            json.dump(self.balances, coin)
            coin.close()
        except IOError:
            print("Fatal Error: Balances could not be written")
            self.client.logout()

    #chad coin group
    @commands.group(
        name='coin',  # if this is omitted the function name will be used
        brief='Access the features of Chad Coin',  # shown when users execute "help"
        description='How to use chad coin',  # shown when users execute "help example"
        aliases=['c']  # alternative ways to execute the command
    )
    async def coin(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("Incorrect usage you dumb monkey! type `chad help coin` to get gud")

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

        if len(args) != 2 or len(ctx.message.mentions) != 1:
            await ctx.channel.send("Incorrect usage you dumb monkey! type `chad help coin give` to get gud")
            return
        cfrom = str(ctx.author.id)
        cto = str(ctx.message.mentions[0].id)

        amount = 0

        try:
            amount = int(args[0])
        except:
            await ctx.channel.send("Incorrect usage you dumb monkey! type `chad help coin give` to get gud")
            return
        
        if(amount < 1):
            await ctx.channel.send("Nice Try")
            return

        if not self.balances.__contains__(str(cfrom)):
            self.balances[cfrom] = 0

        if not self.balances.__contains__(str(cto)):
            self.balances[cto] = 0

        if self.balances[cfrom] < amount:
            await ctx.channel.send(f"You can't afford that, you only have {self.balances[cfrom]} Chad Coins")
            return
        else:
            self.balances[cfrom] -= amount
            self.balances[cto] += amount

        self.updateData()
        await ctx.channel.send(f"Transfered {amount} from {ctx.author[:-5]} to {str(ctx.message.mentions[0])[:-5]}")

    @coin.command(
        name='buy',  # if this is omitted the function name will be used
        brief='How to buy chad coin',  # shown when users execute "help"
        description='Usage: chad coin buy'  # shown when users execute "help example"
    )
    async def buy(self, ctx):
        await ctx.channel.send("Chad Coin can be bought from Hao at a rate of $1 per 100 Chad Coins")

    @coin.command(
        name='sell',  # if this is omitted the function name will be used
        brief='How to sell chad coin',  # shown when users execute "help"
        description='Usage: chad coin buy'  # shown when users execute "help example"
    )
    async def sell(self, ctx):
        await ctx.channel.send("Chad Coin can be sold to Hao at a rate of 100 Chad Coins per $1")

    @coin.command(
        name='balance',  # if this is omitted the function name will be used
        brief='Check your or someone\'s balance',  # shown when users execute "help"
        description='Usage: chad coin balance [@mention]',  # shown when users execute "help example"
        aliases = ['bal']
    )
    async def bal(self, ctx, *args):
        #self balance
        target = ""
        if len(args) == 0:
            target = str(ctx.author.id)
        else:
            target = str(ctx.message.mentions[0].id)

        if not self.balances.__contains__(target):
            self.balances[target] = 0
            print(self.balances)

        balance = self.balances[target]

        suffix = ""

        if balance == 0:
            suffix = "no chad coins :open_mouth:"
        elif balance == 1:
            suffix = "a chad coin :joy:"
        elif balance > 1000:
            suffix = f"{balance} chad coins :moneybag:"
        else:
            suffix = f"{balance} chad coins :money_with_wings:"

        if len(args) == 0:
            await ctx.channel.send(f'You have ' + suffix)
        else:
            await ctx.channel.send(f'{str(ctx.message.mentions[0])[:-5]} has ' + suffix)


def setup(client):
    client.add_cog(Coin(client))