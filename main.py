# Work with Python 3.6
import discord
import string
import random

TOKEN = 'NTIyNzkyMjI0NDQ3MjY2ODIw.DvSeuQ.NJvdqM05l7WqJ1VZpBzU33Kcy-E'

filt = set(open("badwords.txt").read().split(", "))
jamie = open("jaime.txt").read().splitlines()

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    msg = ""
    parts = message.content.split(" ")

    for part in parts:
        if part in filt:
            msg += "No swearing on my Christian Minecraft Server \n"
            msg += message.author.mention + " has been kicked."
            await client.send_message(message.channel, msg)
            await client.kick(message.author)
            return
    
    if message.content.startswith('uwu'):
        msg += random.choice(jamie)
        await client.send_message(message.channel, msg)
        return

    if message.content.startswith('rps'):
        
        play = parts[1].lower()

        if play in ["rock", "r"]:
            msg += "\nI play paper :newspaper:\nYou Lose! :regional_indicator_l:"
        elif play in ["paper", "p"]:
            msg += "\nI play scissors :scissors:\nYou Lose! :regional_indicator_l:"
        elif play in ["scissor", "s", "scissors"]:
            msg += "\nI play rock :gem:\nYou Lose! :regional_indicator_l:"
        else:
            msg += "Ur bad lol you don't know how to play rps"

        await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)