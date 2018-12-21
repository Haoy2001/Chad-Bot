"""This is a cog for a discord.py bot.
It adds a currency which can be transfered

Commands:


"""

from discord.ext import commands
from discord import Member
import asyncio
import json
from pprint import pprint
from discord.utils import find

class Coin():
    
    def __init__(self, client):
        self.client = client

        self.logo = open("data/logo.txt", "r").read()
        
        #load balances
        try:
            coin = open("data/coin.json", "r")
            self.balances = json.load(coin)
            coin.close()
        except IOError:
            print("Fatal Error: Balances could not be read")
            self.client.logout()

        #load other info
        try:
            coin = open("data/info.json", "r")
            self.infojson = json.load(coin)
            coin.close()
        except IOError:
            print("Fatal Error: Info could not be read")
            self.client.logout()


    def updateData(self):
        try:
            coin = open("data/coin.json", "w")
            json.dump(self.balances, coin)
            coin.close()
        except IOError:
            print("Fatal Error: Balances could not be written")
            self.client.logout()

        try:
            coin = open("data/info.json", "w")
            json.dump(self.infojson, coin)
            coin.close()
        except IOError:
            print("Fatal Error: Info could not be written")
            self.client.logout()

    async def most(self):
        topbal = [(key, val) for key, val in self.balances.items()]
        topbal.sort(key=lambda x: x[1])
        topbal.reverse()
    
        topprint = []

        for key, bal in topbal:
            info = await self.client.get_user_info(key)
            out = (info.name)[:11].ljust(11, " ") + " - " + str(bal)
            topprint.append(out)
        return topprint

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
        name='give',  # if this is omitted the function name will be used
        brief='Give Chad Coin to someone',  # shown when users execute "help"
        description='Usage: chad coin give amount @mention',  # shown when users execute "help example"
        alias=['transfer', 't', 'g']
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
            await ctx.channel.send("Nice Try :joy: :joy: :joy: :joy: :joy:")
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

        self.infojson["volume"] += amount
        self.updateData()
        await ctx.channel.send(f"Transfered {amount} from `{ctx.author.name}` to `{ctx.message.mentions[0].name}`")

    @coin.command(
        name='info',
        brief='Gets info about Chad Coin',
        description='Usage: chad coin info'
    )
    async def info(self, ctx):
        logocopy = self.logo

        total = str(sum(self.balances.values())).center(15)
        volume = str(self.infojson["volume"]).center(13)

        topr = await self.most()

        logocopy = logocopy.replace("a##############", total)
        logocopy = logocopy.replace("b############", volume)
        logocopy = logocopy.replace("c################", topr[0].center(17))
        logocopy = logocopy.replace("d################", topr[1].center(17))
        logocopy = logocopy.replace("e################", topr[2].center(17))
        # logocopy.replace("", )
        await ctx.channel.send(logocopy)

    @coin.command(
        name='balance',  # if this is omitted the function name will be used
        brief='Check your or someone\'s balance',  # shown when users execute "help"
        description='Usage: chad coin balance [@mention]',  # shown when users execute "help example"
        aliases = ['bal', 'b']
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
        
        #check if querying itself
        elif ctx.message.mentions[0].id == 522792224447266820:
            await ctx.channel.send('I have ' + suffix)
        else:
            await ctx.channel.send(f'`{ctx.message.mentions[0].name}` has ' + suffix)



    @coin.command(
        name='top',
        brief='Gets richest users',
        description='Usage: chad coin top',
    )
    async def top(self, ctx):
        await ctx.channel.send("```" + "\n".join(await self.most()) + "```")  



    @coin.command(
        name='buy',
        brief='How to buy chad coin',
        description='Usage: chad coin buy'
    )
    async def buy(self, ctx):
        await ctx.channel.send("Chad Coin is in alpha and has no real value")
        #await ctx.channel.send("Chad Coin can be bought from Hao at a rate of $1 per 100 Chad Coins")

    @coin.command(
        name='sell',
        brief='How to sell chad coin',
        description='Usage: chad coin buy'
    )
    async def sell(self, ctx):
        await ctx.channel.send("Chad Coin is in alpha and has no real value")
        #await ctx.channel.send("Chad Coin can be sold to Hao at a rate of 100 Chad Coins per $1")


def setup(client):
    client.add_cog(Coin(client))