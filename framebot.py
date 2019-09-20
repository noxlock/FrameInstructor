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




	if message.content.startswith('!charlist'):
		embed = discord.Embed(
		title = 'FrameInstructor Character List',
		description = f"List of characters"
		)
		embed.add_field(name="Character List", value=charlist, inline=False)
		await message.channel.send(embed=embed)




	if message.content.startswith('!help'): #displays the help menu
		embed = discord.Embed(
		title = 'FrameInstructor Help Menu',
		description = f"List of commands"
		)

		embed.add_field(name="!help", value="Displays this menu.", inline=False)
		embed.add_field(name="!help frame", value="Displays ALL the options for !frame", inline=False)
		await message.channel.send(embed=embed)


	if message.content == "!help frame": #frame help menu, very big
		embed = discord.Embed(
		title = '!frame Help Menu',
		description = f"List of all syntax you can use with !frame"
		)

		embed.add_field(name="cmd {move}", value="Displays a selected move's info", inline=False)
		embed.add_field(name="plusOnBlock {True/False}", value="Pastes a link to all of the character's plus frame on block moves. This is done because there is a lot.", inline=False)
		embed.add_field(name="plusOnHit {True/False}", value="Pastes a link to all of the character's plus frame on hit moves. This is done because there is a lot.", inline=False)
		



	if message.content.startswith('!frame'):
		message.content = message.content.strip('!frame')
		message.content = message.content.split()
		message.content[0] = message.content[0].title()


		if message.content[0] not in charlist:
			await message.channel.send("Check the spelling of your character, do !charlist to see all available characters.")


		if len(message.content) < 3: #checks if all 3 parameters are supplied
			await message.channel.send("Missing parameters")


		else: #if all 3 supplied then:
			r = requests.get(f'https://t7api.herokuapp.com/character/{message.content[0]}?{message.content[1]}={message.content[2]}')		
			result = r.json()

			#move on to error checking


			if not result: #if result empty, move doesn't exist
				await message.channel.send("Move not found")


			#append to embed object, and send.


			else:
				file = discord.File(f"./Thumbnails/{message.content[0]}.jpg")
				embed = discord.Embed(
				title = 'FrameInstructor Data',
				description = f"Frame Data for {message.content[0]}, {message.content[2]}", #frame data for character, cmd
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
				embed.set_thumbnail(url=f"attachment://{message.content[0]}.jpg")
				#adds all the data to the embed object.
				await message.channel.send(file=file, embed=embed)




client.run('NjIyMjQxNzM0NDAzMDMxMDQw.XXxYhA.ZC1GfQbWhzm4XxtCFql4q-nCU0Q')