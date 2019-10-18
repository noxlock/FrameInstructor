""" A Discord bot that utilizes fANZYo's T7 API
to send back frame data as a Discord embed message
"""

import discord
import requests
from environs import Env

# reading the environment variable from the .env file
ENV = Env()
ENV.read_env()
CLIENT_KEY = ENV("CLIENT_KEY")

CLIENT = discord.Client()


# could also be fetched via the api, but it's probably easier to just store it globally
CHAR_LIST = ["Akuma", "Alisa", "Anna", "Armorking", "Asuka", "Bob", "Bryan", "Claudio",
             "Deviljin", "Dragunov", "Eddy", "Eliza", "Feng", "Geese", "Gigas", "Heihachi",
             "Hwoarang", "Jack", "Jin", "Josie", "Julia", "Katarina", "Kazumi", "Kazuya",
             "King", "Kuma", "Lars", "Lei", "Law", "Lee", "Leo", "Lili", "Chloe", "Marduk",
             "Raven", "Miguel", "Negan", "Nina", "Noctis", "Paul", "Shaheen", "Steve",
             "Xiayou", "Yoshimitsu"]




@CLIENT.event
async def on_ready(): #on successful login
    """On successful login, will print to the console"""
    print(f'We have logged in as {CLIENT.user}') #print to the console




@CLIENT.event
async def on_message(message): # on receiving a message
    """Upon seeing a message, checks if it starts with
    the prefix (!), if it does, it will carry out
    that command.
    """

    if message.author == CLIENT.user: #prevents the bot calling itself
        return

    if message.content.startswith("!"): #if prefix used

    # nested within prefix check

        if message.content == "!charlist": #character list command
            await embed_work("charlist", CHAR_LIST, message)

        elif message.content == "!help": #displays the help menu
            await embed_work("help", None, message)

        elif message.content == "!help frame": #frame help menu, very big
            await embed_work("help frame", None, message)

        elif message.content.startswith("!legend"): # for legend of syntax
            await embed_work("legend", None, message)

        elif message.content.startswith("!frame"): # for frame commands
            await check_query(message)







async def check_query(message):
    """Does some of the error checking before fully making
    a request with frame_request()

    Args:
    message: object that has .content, and .channel, which we need

    Type:
    message: class
    """

    message.content = message.content.split()


    if len(message.content) <= 3: #checks if all 3 parameters are supplied
        await message.channel.send("Missing parameters")
        return

    message.content[1] = message.content[1].title()

    if message.content[1] not in CHAR_LIST: # if character not found
        await message.channel.send("""Check the spelling of your character,
do !charlist to see all available characters.""")
        return


    await frame_request(message) # if no errors found, make the request




async def frame_request(message):
    """Makes the request, and checks if the result is valid before
    sending it to embed_work()

    Args:
    message: same message class we're using
    with the other functions, we still need it
    to make the request and pass the channel to embed

    Type:
    message: class
    """

    #makes the request
    #the request cannot be multilined to meet pep-8 otherwise it breaks
    URL = f"https://t7api.herokuapp.com/character/{message.content[1]}?{message.content[2]}={message.content[3]}"
    data = requests.get(URL).json() #parses the json

    if not data: #if data empty, move doesn't exist
        await message.channel.send("Move not found")

    if message.content[2] != "cmd":
        await message.channel.send(URL)

    else:
        await embed_work("frame", (data, URL), message) #if data exists, pass it to embed_work


async def embed_work(mode, data, message):
    """This function does all the work pertaining to embeds, and then sends them.
    Args:
    mode: each command will pass a different mode to the function, letting us know what to do
    data: any data required to send the embed
    message: used to send to the same channel as the command was used, and to read content.

    Type:
    mode: string
    data: dict/list
    message: class
    """

### CHECKING WHAT TO EMBED DEPENDING ON MODE ###

    if mode == "charlist": #if called by charlist

        ### EMBED ALL DATA ###
        embed = discord.Embed(
            title='FrameInstructor Character List',
            description=f"List of characters"
        )
        embed.add_field(name="Character List", value=CHAR_LIST, inline=False)
        ### SEND TO CHANNEL ###
        await message.channel.send(embed=embed)


    elif mode == "help": #if called by !help

        embed = discord.Embed(
            title='FrameInstructor Help Menu',
            description=f"List of commands"
        )

        embed.add_field(name="!help", value="Displays this menu.", inline=False)

        embed.add_field(name="!help frame", value="Displays ALL the options for !frame"
                        , inline=False)

        embed.add_field(name="!legend", value="Sends a link to the official Tekken Zaibatsu Legend"
                        , inline=False)

        embed.add_field(name="!frame", value="Does many things with frame data, check !help"
                        , inline=False)

        embed.add_field(name="Confused?", value="[Link to docs](https://www.github.com/noxlock/FrameInstructor)"
                        , inline=False)

        await message.channel.send(embed=embed)


    elif mode == "legend": #if called by !help

        embed = discord.Embed(
            title='FrameInstructor',
            description="!legend"
        )

        embed.add_field(name="Link to Tekken Zaibatsu's Legend page", value=f"[Tekken Zaibatsu](http://www.tekkenzaibatsu.com/legend.php)", inline=False)

        await message.channel.send(embed=embed)


    elif mode == "help frame": #if called by !help frame
        embed = discord.Embed(
            title='Help Menu For !frame',
            description=f"List of all syntax you can use with !frame"
        )

        embed.add_field(name="cmd {move}", value="Displays a selected move's info",
                        inline=False)

        embed.add_field(name="{plus/minus}OnBlock {True/False}",
                        value="""Pastes a link to all of the character's
                        plus or minus frame on block moves.""", inline=False)

        embed.add_field(name="{plus/minus}OnHit {True/False}",
                        value="The same as {OnBlock} but for frames on hit.", inline=False)

        embed.add_field(name="{plus/minus}OnCounter {True/False}",
                        value="""The same as {OnBlock}
                        but for frames on counter hit.""", inline=False)

        embed.add_field(name="onBlock {min,max}",
                        value="""Pastes a link to all of the character's
                        moves which frames are within the range on block.""", inline=False)

        embed.add_field(name="onHit {min,max}",
                        value="The same as {onHit} but for frame data on hit", inline=False)

        embed.add_field(name="onCounter {min,max}",
                        value="""The same as {onBlock}
                        but for frama data on counter hit""", inline=False)

        embed.add_field(name="hit {h/m/l}",
                        value="""Pastes a link to all of the character's
                        moves that are {high}, {mid}, or {low} hitting.""", inline=False)

        embed.add_field(name="firstHit {h/m/l}", value="""The same as {hit}
                        but only for the first hit of the move.""", inline=False)

        embed.add_field(name="lastHit {h/m/l}", value="""The same as {firsthit}
                        but for the last hit of the move.""", inline=False)

        embed.add_field(name="speed {min,max}", value="""Pastes a link to all of the character's
                        moves which startup frames are between {min,max}.""", inline=False)

        embed.add_field(name="crush {TJ/TC}", value="""Pastes a link to all of the character's
                        moves which are either tech jump or tech crouch.""", inline=False)

        await message.channel.send(embed=embed)

    elif mode == "frame": #if called by !frame/frame_request()
        data, URL = data[0], data[1]

        file = discord.File(f"./Thumbnails/{message.content[1]}.jpg")
        embed = discord.Embed(
            title='FrameInstructor Data',
            description=f"Frame Data for {message.content[1]}, {message.content[3]}",
            colour=discord.Color.red()
        )

        embed.add_field(name="Character", value=message.content[1], inline=True)
        embed.add_field(name="Command", value=data[0]['cmd'], inline=True)
        embed.add_field(name="Type", value=data[0]['hit'], inline=True)
        embed.add_field(name="Damage", value=data[0]['dmg'], inline=True)
        embed.add_field(name="Startup Frames", value=data[0]['speed'], inline=True)
        embed.add_field(name="On Block", value=data[0]['onBlock'], inline=True)
        embed.add_field(name="On Hit", value=data[0]['onHit'], inline=True)
        embed.add_field(name="CH", value=data[0]['onCounter'], inline=True)
        embed.add_field(name="Not what you were looking for?", value=f"[Try this]({URL})", inline=False)
        embed.set_thumbnail(url=f"attachment://{message.content[1]}.jpg")


        await message.channel.send(file=file, embed=embed) #send the embed


CLIENT.run(CLIENT_KEY) #api key
