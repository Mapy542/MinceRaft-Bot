# bot.py
import discord

try:
    with open("Creds.txt", "r") as f:
        data = f.read().splitlines()
        TOKEN = data[0].split("=")[1]
        print(TOKEN)
        f.close()
except FileNotFoundError:
    TOKEN = input("Enter token: ")


client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
