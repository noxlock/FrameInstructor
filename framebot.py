""" A Discord bot that utilizes fANZYo's T7 API
to send back frame data as a Discord embed message
"""

import discord
import requests


CLIENT = discord.Client()
CHAR_LIST = ["Akuma", "Alisa", "Anna", "Armor King", "Asuka", "Bob", "Bryan", "Claudio",
             "Devil Jin", "Dragunov", "Eddy", "Eliza", "Feng", "Geese", "Gigas", "Heihachi",
             "Hwoarang", "Jack", "Jin", "Josie", "Julia", "Katarina", "Kazumi", "Kazuya",
             "King", "Kuma", "Lars", "Lei", "Law", "Lee", "Leo", "Lili", "Chloe", "Marduk",
             "Raven", "Miguel", "Negan", "Nina", "Noctis", "Paul", "Shaheen", "Steve",
             "Xiayou", "Yoshimitsu"]




@CLIENT.event
async def on_ready():
    """On successful login, will print to the console"""
    print('We have logged in as {0.user}'.format(CLIENT)) #just prints to console when online

@CLIENT.event
async def on_message(message): # on message, runs function
    """Upon seeing a message, does numerous checks to identify the command,
    and performs error handling before
    sending the data to message.channel.send() and finally returning
    """

    if message.author == CLIENT.user: #prevents the bot calling itself
        return


    if message.content.startswith("!"): #if prefix used

        if message.content == "!charlist": #character list command
            embed = discord.Embed(
                title='FrameInstructor Character List',
                description=f"List of characters"
            )
            embed.add_field(name="Character List", value=CHAR_LIST, inline=False)
            await message.channel.send(embed=embed)




        elif message.content == "!help": #displays the help menu
            embed = discord.Embed(
                title='FrameInstructor Help Menu',
                description=f"List of commands"
            )

            embed.add_field(name="!help", value="Displays this menu.", inline=False)

            embed.add_field(name="!help frame", value="Displays ALL the options for !frame"
                            , inline=False)

            await message.channel.send(embed=embed)


        elif message.content == "!help frame": #frame help menu, very big
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



        elif message.content.startswith("!frame"): # for frame commands
            message.content = message.content.split()
            message.content[1] = message.content[1].title()


            if message.content[1] not in CHAR_LIST: # if character not found
                await message.channel.send("""Check the spelling of your character,
                                            do !charlist to see all available characters.""")


            if len(message.content) < 3: #checks if all 3 parameters are supplied
                await message.channel.send("Missing parameters")


            else: #if all 3 supplied then:
                r_json = requests.get(f""""https://t7api.herokuapp.com/character/
                {message.content[1]}?{message.content[2]}={message.content[3]}""")

                result = r_json.json()

                #move on to error checking


                if not result: #if result empty, move doesn't exist
                    await message.channel.send("Move not found")


                #append to embed object, and send.


                else:
                    file = discord.File(f"./Thumbnails/{message.content[1]}.jpg")
                    embed = discord.Embed(
                        title='FrameInstructor Data',
                        description=f"Frame Data for {message.content[1]}, {message.content[3]}",
                        colour=discord.Color.red()
                    )

                    embed.add_field(name="Character", value=message.content[0], inline=True)
                    embed.add_field(name="Command", value=result[0]['cmd'], inline=True)
                    embed.add_field(name="Type", value=result[0]['hit'], inline=True)
                    embed.add_field(name="Damage", value=result[0]['dmg'], inline=True)
                    embed.add_field(name="Startup Frames", value=result[0]['speed'], inline=True)
                    embed.add_field(name="On Block", value=result[0]['onBlock'], inline=True)
                    embed.add_field(name="On Hit", value=result[0]['onHit'], inline=True)
                    embed.add_field(name="CH", value=result[0]['onCounter'], inline=True)
                    embed.set_thumbnail(url=f"attachment://{message.content[1]}.jpg")
                    #adds all the data to the embed object.

                    await message.channel.send(file=file, embed=embed) #send the embed


CLIENT.run('NjIyMjQxNzM0NDAzMDMxMDQw.XXxYhA.ZC1GfQbWhzm4XxtCFql4q-nCU0Q') #api key
