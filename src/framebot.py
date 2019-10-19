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

        reply = Embedder(message)

        if message.content == "!help": #displays the help menu
            await reply.help()

        elif message.content == "!help frame": #frame help menu, very big
            await reply.help_frame()

        elif message.content == "!charlist": #character list command
            await reply.charlist(CHAR_LIST)

        elif message.content == "!legend": # for legend of syntax
            await reply.legend()

        elif message.content.startswith("!frame"): # for frame commands
            await check_query(reply)







async def check_query(reply):
    """Does some of the error checking before fully making
    a request with frame_request()

    Parameters
    ----------
    message: class
        class that has .content, and .channel, which we need

    Returns
    -------

    """

    reply.message.content = reply.message.content.split()


    if len(reply.message.content) <= 3: #checks if all 3 parameters are supplied
        await reply.message.channel.send("Missing parameters")
        return

    reply.message.content[1] = reply.message.content[1].title()

    if reply.message.content[1] not in CHAR_LIST: # if character not found
        await reply.message.channel.send("""Check the spelling of your character,
do !charlist to see all available characters.""")
        return


    await frame_request(reply) # if no errors found, make the request




async def frame_request(reply):
    """Makes the request, and checks if the result is valid before
    sending it to embed_work()

    Parameters
    ----------
    message: class
        same message class we're using
        with the other functions, we still need it
        to make the request and pass the channel to embed

    Returns
    -------
    """

    #makes the request
    #the request cannot be multilined to meet pep-8 otherwise it breaks
    URL = f"https://t7api.herokuapp.com/character/{reply.message.content[1]}?{reply.message.content[2]}={reply.message.content[3]}"
    data = requests.get(URL).json() #parses the json

    if not data: #if data empty, move doesn't exist
        await reply.message.channel.send("Move not found")

    if reply.message.content[2] != "cmd":
        await reply.message.channel.send(URL)

    else:
        await reply.frame((data, URL)) #if data exists, pass it to embed_work


class Embedder:
    """Class that handles all the code 
    regarding embeds
    """

    def __init__(self, message):
        """Initializes the class with the 
        message class

        Parameters
        ----------
        data: list/tuple
            anything extra needed to complete
            the embed
        message: class
            contains the message content and channel
        """

        self.message = message


    async def help(self):
        """Embeds and sends the result
        of the !help command

        Parameters
        ----------
        self: class
            contains the message content and channel
        """

        embed = discord.Embed(
            title='FrameInstructor Help Menu',
            description=f"List of commands"
        )

        embed.add_field(name="!help", value="Displays this menu.", inline=False)

        embed.add_field(name="!help frame", value="Displays ALL the options for !frame"
                        , inline=False)

        embed.add_field(name="!legend", value="Sends a link to the official Tekken Zaibatsu Legend"
                        , inline=False)

        embed.add_field(name="!charlist", value="Displays a list of all possible characters to be used with other commands"
                        , inline=False)

        embed.add_field(name="!frame", value="Does many things with frame data, check !help frame"
                        , inline=False)

        embed.add_field(name="Confused?", value="[Link to docs](https://www.github.com/noxlock/FrameInstructor)"
                        , inline=False)

        await self.message.channel.send(embed=embed)


    async def help_frame(self):
        """Embeds and sends the result
        of the !help frame command

        Parameters
        ----------
        self: class
            contains the message content and channel
        """

        embed = discord.Embed(
            title='Help Menu For !frame',
            description="Menu follows the convention of !frame {character} {parameter} {condition}"
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

        embed.add_field(name="Confused?", value="[Link to docs](https://www.github.com/noxlock/FrameInstructor)"
                        , inline=False)

        await self.message.channel.send(embed=embed)


    async def charlist(self, data):
        """Embeds and sends the charlist

        Parameters
        ----------
        data: list
            the list of characters
        self: class
            contains the message content and channel
        """

        ### EMBED ALL DATA ###
        embed = discord.Embed(
            title='FrameInstructor Character List',
            description=f"List of characters"
        )
        embed.add_field(name="Character List", value=CHAR_LIST, inline=False)
        ### SEND TO CHANNEL ###
        await self.message.channel.send(embed=embed)


    async def legend(self):
        """Embeds and sends a 
        hyperlink to the legend

        Parameters
        ----------
        self: class
            contains the message content and channel
        """

        embed = discord.Embed(
            title='FrameInstructor',
            description="!legend"
        )

        embed.add_field(name="Link to Tekken Zaibatsu's Legend page", value=f"[Tekken Zaibatsu](http://www.tekkenzaibatsu.com/legend.php)", inline=False)

        await self.message.channel.send(embed=embed)


    async def frame(self, data):
        """Embeds the result of frame_request()
        and sends it.

        Parameters
        ----------
        data: tuple
            the request result and URL of the endpoint
        self: class
            contains the message content and channel
        """

        data, URL = data[0], data[1]

        file = discord.File(f"./Thumbnails/{self.message.content[1]}.jpg")
        embed = discord.Embed(
            title='FrameInstructor Data Result',
            description=f"Frame Data for {self.message.content[1]}, {self.message.content[3]}",
            colour=discord.Color.red()
        )

        embed.add_field(name="Character", value=self.message.content[1], inline=True)
        embed.add_field(name="Command", value=data[0]['cmd'], inline=True)
        embed.add_field(name="Type", value=data[0]['hit'], inline=True)
        embed.add_field(name="Damage", value=data[0]['dmg'], inline=True)
        embed.add_field(name="Startup Frames", value=data[0]['speed'], inline=True)
        embed.add_field(name="On Block", value=data[0]['onBlock'], inline=True)
        embed.add_field(name="On Hit", value=data[0]['onHit'], inline=True)
        embed.add_field(name="CH", value=data[0]['onCounter'], inline=True)
        embed.add_field(name="Not what you were looking for?", value=f"[Try this]({URL})", inline=False)
        embed.set_thumbnail(url=f"attachment://{self.message.content[1]}.jpg")


        await self.message.channel.send(file=file, embed=embed) #send the embed


CLIENT.run(CLIENT_KEY) #api key

