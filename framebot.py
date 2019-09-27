import discord
import requests
import pprint

client = discord.Client()
pp = pprint.PrettyPrinter(indent=4)
charlist = ["Akuma", "Alisa", "Anna", "Armor King", "Asuka", "Bob", "Bryan", "Claudio", "Devil Jin", "Dragunov", "Eddy", "Eliza", "Feng", "Geese", "Gigas", "Heihachi", "Hwoarang", "Jack", "Jin", "Josie", "Julia", "Katarina", "Kazumi", "Kazuya", "King", "Kuma", "Lars", "Lei", "Law", "Lee", "Leo", "Lili", "Chloe", "Marduk", "Raven", "Miguel", "Negan", "Nina", "Noctis", "Paul", "Shaheen", "Steve", "Xiayou", "Yoshimitsu"]




@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client)) #just prints to console when online

@client.event
async def on_message(message): # on message, runs function

	if message.author == client.user: #prevents the bot calling itself
		return


	if message.content.startswith("!"):

		if message.content == "!charlist":
			embed = discord.Embed(
			title = 'FrameInstructor Character List',
			description = f"List of characters"
			)
			embed.add_field(name="Character List", value=charlist, inline=False)
			await message.channel.send(embed=embed)




		elif message.content == "!help": #displays the help menu
			embed = discord.Embed(
			title = 'FrameInstructor Help Menu',
			description = f"List of commands"
			)

			embed.add_field(name="!help", value="Displays this menu.", inline=False)
			embed.add_field(name="!help frame", value="Displays ALL the options for !frame", inline=False)
			await message.channel.send(embed=embed)


		elif message.content == "!help frame": #frame help menu, very big
			embed = discord.Embed(
			title = 'Help Menu For !frame',
			description = f"List of all syntax you can use with !frame"
			)

			embed.add_field(name="cmd {move}", value="Displays a selected move's info", inline=False)
			embed.add_field(name="{plus/minus}OnBlock {True/False}", value="Pastes a link to all of the character's plus or minus frame on block moves.", inline=False)
			embed.add_field(name="{plus/minus}OnHit {True/False}", value="The same as {OnBlock} but for frames on hit.", inline=False)
			embed.add_field(name="{plus/minus}OnCounter {True/False}", value="The same as {OnBlock} but for frames on counter hit.", inline=False)
			embed.add_field(name="onBlock {min,max}", value="Pastes a link to all of the character's moves which frames are within the range on block.", inline=False)
			embed.add_field(name="onHit {min,max}", value="The same as {onHit} but for frame data on hit", inline=False)
			embed.add_field(name="onCounter {min,max}", value="The same as {onBlock} but for frama data on counter hit", inline=False)
			embed.add_field(name="hit {h/m/l}", value="Pastes a link to all of the character's moves that are {high}, {mid}, or {low} hitting.", inline=False)
			embed.add_field(name="firstHit {h/m/l}", value="The same as {hit} but only for the first hit of the move.", inline=False)
			embed.add_field(name="lastHit {h/m/l}", value="The same as {firsthit} but for the last hit of the move.", inline=False)
			embed.add_field(name="speed {min,max}", value="Pastes a link to all of the character's moves which startup frames are between {min,max}.", inline=False)
			embed.add_field(name="crush {TJ/TC}", value="The same as {firsthit} but for the last hit of the move.", inline=False)
			await message.channel.send(embed=embed)



		elif message.content.startswith("!frame"):
			message.content = message.content.split()
			message.content[1] = message.content[1].title()


			if message.content[1] not in charlist:
				await message.channel.send("Check the spelling of your character, do !charlist to see all available characters.")


			if len(message.content) < 3: #checks if all 3 parameters are supplied
				await message.channel.send("Missing parameters")


			else: #if all 3 supplied then:
				r = requests.get(f'https://t7api.herokuapp.com/character/{message.content[1]}?{message.content[2]}={message.content[3]}')		
				result = r.json()

				#move on to error checking


				if not result: #if result empty, move doesn't exist
					await message.channel.send("Move not found")


				#append to embed object, and send.


				else:
					file = discord.File(f"./Thumbnails/{message.content[1]}.jpg")
					embed = discord.Embed(
					title = 'FrameInstructor Data',
					description = f"Frame Data for {message.content[1]}, {message.content[3]}", #frame data for character, cmd
					colour = discord.Color.red()
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
					await message.channel.send(file=file, embed=embed)




client.run('NjIyMjQxNzM0NDAzMDMxMDQw.XXxYhA.ZC1GfQbWhzm4XxtCFql4q-nCU0Q')