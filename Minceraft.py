# bot.py
import os
try:
    import discord
except ImportError:
    os.system("pip3 install discord")
    print("Installed discord")


def Parsecommand(message):
    command = message.content.split(" ")
    if command[0] == "/Echo":
        command.pop(0)
        return command
    elif command[0] == "/Locate":
        global COMM
        COMM = message.channel
        return "Communication channel set to #" + str(COMM)
    elif command[0] == "/Broadcast":
        command.pop(0)
        minecraft_inject("/say " + str(command))
        return "Broadcasting into server: " + command
    elif command[0] == "/Help":
        return "Commands: /Echo, /Locate, /Broadcast, /Help"


def minecraft_inject(message):
    os.system("screen -r \n " + str(message))


try:
    with open("Creds.txt", "r") as f:
        data = f.read().splitlines()
        TOKEN = data[0].split("=")[1]
        GUILD = data[1].split("=")[1]
        print(TOKEN)
        f.close()
except FileNotFoundError:
    TOKEN = input("Enter token: ")


client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Remote Host Server!'
    )
    await member.dm_channel.send("Join the server at: remotehost.ddns.net")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "/" in message.content:
        roles = [role.name for role in message.author.roles]
        if "Admin" in roles:
            statement = Parsecommand(message)
            if statement != None:
                await message.channel.send(statement)
        else:
            if message.content == "/Help":
                await message.channel.send("Join the server at: remotehost.ddns.net")
            await message.channel.send("You do not have permission to use this command")


client.run(TOKEN)
