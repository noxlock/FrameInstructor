import discord
import requests
import pprint

client = discord.Client()
pp = pprint.PrettyPrinter(indent=4)



# embed.set_footer(text="This is a footer.")
# embed.set_author(name='nox')
# embed.add_field(name="Field 1", value="Field Value", inline=False)
# embed.add_field(name="Field 2", value="Field Value 2", inline=True)



@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client)) #just prints to console when online

@client.event
async def on_message(message): # on message, runs function

	if message.author == client.user: #prevents the bot calling itself
		return

	if message.content.startswith('!help'): #displays the help menu
		embed = discord.Embed(
		title = 'FrameInstructor Help Menu',
		description = f"List of commands"
		)

		embed.add_field(name="!help", value="Displays this menu.", inline=False)
		embed.add_field(name="!frame {character} {command}", value="Displays frame data for the inputted move.", inline=False)
		await message.channel.send(embed=embed)


	if message.content.startswith('!frame'):
		message.content = message.content.strip('!frame')
		r = requests.get(f'https://t7api.herokuapp.com/character/{message.content.strip()}')
		message.content = message.content.replace("?", " ")
		message.content = message.content.replace("=", " ") #various stripping, splitting and replacing to format nicely.
		message.content = message.content.split()
		result = r.json()


		if not result: #if result empty, move doesn't exist
			await message.channel.send("Move not found")

		if 'error' in result: #if error exists, then no valid character
			await message.channel.send("No character found")

		else:
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
			#adds all the data to the embed object.
			await message.channel.send(embed=embed)




client.run('NjIyMjQxNzM0NDAzMDMxMDQw.XXxYhA.ZC1GfQbWhzm4XxtCFql4q-nCU0Q')