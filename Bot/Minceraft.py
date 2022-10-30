# bot.py
import os
import glob
import shlex
import time
try:
    import discord
except ImportError:
    os.system("pip3 install discord")
    print("Installed discord")


def Parsecommand(message, permission):
    command = shlex.split(message.content, posix=False)
    # remove slash from command
    command[0] = command[0][1:]
    # important this command is not common use as the return value is important
    if command[0] == "list":
        global PATH
        minecraft_inject("list^M")
        time.sleep(2)
        log = get_latest_file(str(PATH) + "/logs/*")
        try:
            with open(log, "r") as f:
                lines = f.read()
                lines = lines.split("\n")
                text = lines[len(lines) - 3] + " " + lines[len(lines) - 2]
                text = text.split(" ")
                for i in range(len(text)):
                    if "[" in text[i] or "]" in text[i]:
                        text[i] = ""
                text = [x for x in text if x != '']
                return " ".join(text)
        except:
            return "log file not found"

    elif command[0] == "help":
        global COMMANDS
        global PERMISSIONS
        text = ""
        for i in range(len(COMMANDS)):
            text = text + COMMANDS[i] + " - " + PERMISSIONS[i] + "\n"
        return text

    else:
        global RETURNS
        Permission_Ranking = ["Guest", "User", "Trustee", "Admin"]

        if not command[0] in COMMANDS:  # checks for valid command
            return "Command not found. Try /help"
        index = COMMANDS.index(command[0])

        # check for acceptable permissions
        if Permission_Ranking.index(PERMISSIONS[index]) > Permission_Ranking.index(permission):
            return "You do not have permission to use this command"

        # actuate command
        minecraft_inject(" ".join(command) + "^M")

        # return value
        returnval = RETURNS[index]

        returnval = returnval.split(" ")
        for i in range(len(returnval)):
            if "*par" in returnval[i]:
                if (len(command) - 1 >= int(returnval[i][4:])):
                    returnval[i] = command[int(returnval[i][4:])]
                else:
                    returnval[i] = "default"

        returnval = " ".join(returnval)
        return returnval


def minecraft_inject(message):
    os.system("screen -S Bedrock -p 0 -X stuff \"" + str(message) + "\"")


def get_latest_file(path):
    list_of_files = glob.glob(path)
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file


try:  # pull oauth token from file and other constants data
    with open("Creds.txt", "r") as f:
        data = f.read().splitlines()
        TOKEN = data[0].split("=")[1]
        GUILD = data[1].split("=")[1]
        PATH = data[2].split("=")[1]
        f.close()
except FileNotFoundError:
    TOKEN = input("Enter token: ")

try:  # import commands and permissions
    with open("Commands.txt", "r") as f:
        commands = f.read().splitlines()
        commands.pop(0)
        COMMANDS = []
        PERMISSIONS = []
        RETURNS = []
        for command in commands:
            if command[0] == "":
                print("empty line")
            else:
                COMMANDS.append(command.split(",")[0])
                PERMISSIONS.append(command.split(",")[1])
                RETURNS.append(command.split(",")[2])
        print(COMMANDS)
        f.close()
except FileNotFoundError:
    commands = []
    print("Commands.txt not found")

# initiate discord bot
client = discord.Client(intents=discord.Intents.all())


@client.event  # on ready post to console
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


@client.event  # on join guild DM them
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Remote Host Server!'
    )
    await member.dm_channel.send("Join the server at: remotehost.ddns.net")


@client.event  # on message
async def on_message(message):  # ignore self
    if message.author == client.user:
        return

    if "/" in message.content:
        roles = [role.name for role in message.author.roles]
        if ("Admin" in roles):
            permission = 'Admin'
        elif ("Trustee" in roles):
            permission = 'Trustee'
        elif ("User" in roles):
            permission = 'User'
        statement = Parsecommand(message, permission)
        if statement != None:
            await message.channel.send(statement)

client.run(TOKEN)
