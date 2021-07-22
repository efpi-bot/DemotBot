import discord
import requests
import random
import math
from bs4 import BeautifulSoup

class fandemonium:

	def __init__(self):
		None

	async def run(self, message):

		query = message.content[:-10]
		print(query)
		response = requests.get(f'http://fandemonium.pl/szukaj?q={query}')
		soup = BeautifulSoup(response.content, 'html.parser')

		howManyPages = len(soup.find_all(class_="paging"))
		isPageEmpty = not bool(len(soup.find_all(class_=['fandemot','loaded'])))

		if isPageEmpty == True:

			await message.channel.send('nie ma')
			return

		elif howManyPages != 0:
			randomPageNumber = random.randint(0, howManyPages-1)
			response = requests.get(f'http://fandemonium.pl/szukaj?page={randomPageNumber}&q={query}')
			soup = BeautifulSoup(response.content, 'html.parser')	

		fandemotsArray = soup.find_all(class_=['fandemot','loaded'])

		randomFandemot = random.choice(fandemotsArray)
		imgUrl = randomFandemot['src']

		await message.channel.send(imgUrl)

class miejski:

	def __init__(self):
		None

	async def run(self, message):

		query = message.content[:-8]

		url = f'https://www.miejski.pl/slowo-{query}'
		r_word = requests.get(url)
		definition = ''
		soup = BeautifulSoup(r_word.content, 'html.parser')

		for article in soup.findAll('article'):

			if article.find('p') != None:
				p = article.p.stripped_strings
				definition += '\n'
				
				for string in p:
					definition += string
					definition += ' '

				
			if article.find('blockquote') != None:
				definition += '\n > '
				quote = article.blockquote.stripped_strings

				for string in quote:
					definition += string
					definition += ' '
				definition += '\n '

		if len(definition) > 2000:
			definition = definition[0:2000]

		await message.channel.send(definition)

class komixxy:

	def __init__(self):
		None

	async def run(self, message):

		query = message.content[:-8]
		print(query)
		response = requests.get(f'https://komixxy.pl/szukaj?q={query}')
		soup = BeautifulSoup(response.content, 'html.parser')

		searchResult = soup.find(id = "main_container").contents[25].strip()

		if searchResult == "Nic takiego nie znalazłem":
			await message.channel.send('nie ma')
			return

		howManyResults = int(searchResult.split(' ')[1])
		howManyPages = math.ceil(howManyResults/10)

		if howManyPages != 1:
			randomPageNumber = random.randint(1,int(howManyPages))
			response = requests.get(f'https://komixxy.pl/szukaj/page/{randomPageNumber}?q={query}')
			soup = BeautifulSoup(response.content, 'html.parser')

		komixxyArray = soup.find_all(class_='picwrapper')
		randomKomixx = random.choice(komixxyArray)

		if randomKomixx.img['src'] != '/res/img/blank.gif':
			imgUrl = 'https://komixxy.pl' + randomKomixx.img['src']
		else:
			imgUrl = 'https://komixxy.pl' + randomKomixx.img['data-src']

		imgUrl = imgUrl.replace('_500.jpg','.jpg')

		await message.channel.send(imgUrl)


class demotbot:

	def __init__(self):
		None

	async def single(self, message):

		query = message.content[:-7]
		print(query)
		response = requests.get(f'https://demotywatory.pl/szukaj?q={query}')
		soup = BeautifulSoup(response.content, 'html.parser')

		searchResultsH2 = soup.find_all('h2')

		try:
			resultH2 = searchResultsH2[2].string
		except:
			await message.channel.send('nie ma')
			return

		howManyResults = ''
		for i in searchResultsH2[2].string:
			if str.isdigit(i):
				howManyResults += i

		howManyResults = int(howManyResults)
		howManyPages = math.ceil(howManyResults/20)

		if howManyPages != 1:
			randomPageNumber = random.randint(1,int(howManyPages))
			response = requests.get(f'https://demotywatory.pl/szukaj/page/{randomPageNumber}?q={query}')
			soup = BeautifulSoup(response.content, 'html.parser')

		demotsArray = soup.find_all(class_='demot')

		randomDemot = random.choice(demotsArray)
		imgUrl = randomDemot['src']
		#imgUrl = randomDemot['src'].replace('_600.jpg','.jpg')

		await message.channel.send(imgUrl)


	async def topInit(self, message):

		query = message.content[:-11]
		print(query)
		response = requests.get(f'https://demotywatory.pl/szukaj/page/1?q={query}')
		soup = BeautifulSoup(response.content, 'html.parser')

		searchResultsH2 = soup.find_all('h2')

		try:
			resultH2 = searchResultsH2[2].string
		except:
			await message.channel.send('nie ma')
			return

		howManyResults = ''
		for i in searchResultsH2[2].string:
			if str.isdigit(i):
				howManyResults += i

		howManyResults = int(howManyResults)
		howManyPages = math.ceil(howManyResults/20)


		demotsArray = soup.find_all(class_ = 'demot')
		demot = demotsArray[0]

		imgUrl = demot['src']

		demotEmbed = discord.Embed(title = query)
		demotEmbed.set_image(url = imgUrl)
		demotEmbed.set_footer(text = f"1/{howManyResults}")
		msgEmbed = await message.channel.send(embed = demotEmbed)
		await msgEmbed.add_reaction("⬅️")
		await msgEmbed.add_reaction("➡️")
		await msgEmbed.add_reaction("🎲")

	async def handleReactions(self, reaction):

		demotEmbed = reaction.message.embeds[0]
		query = demotEmbed.title
		numCurrent = int(demotEmbed.footer.text.split('/')[0])
		numMax = int(demotEmbed.footer.text.split('/')[1])
		howManyPages = math.ceil(numMax/20)
		numDesired = None

		if reaction.emoji == "⬅️":
			numDesired = numCurrent - 1

		elif reaction.emoji == "➡️":
			numDesired = numCurrent + 1

		elif reaction.emoji == "🎲":
			numDesired = random.randint(1, numMax)

		if numDesired == numCurrent:
			numDesired += 1

		if numDesired < 1:
			numDesired = numMax

		elif numDesired > numMax:
			numDesired = 1

		pageDesired = math.ceil(numDesired/20)
		numOnPage = numDesired - (pageDesired - 1)*20


		response = requests.get(f'https://demotywatory.pl/szukaj/page/{pageDesired}?q={query}')
		soup = BeautifulSoup(response.content, 'html.parser')

		demotsArray = soup.find_all(class_ = 'demot')
		demot = demotsArray[numOnPage - 1]
		imgUrl = demot['src']

		demotEmbed.set_image(url = imgUrl)
		demotEmbed.set_footer(text = f"{numDesired}/{numMax}")

		await reaction.message.edit(embed = demotEmbed)


# DISCORD BOT HERE

KEY = open('./key').read()

demotbot = demotbot()
komixxy = komixxy()
miejski = miejski()
fandemonium = fandemonium()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().endswith(' demoty'):
        await demotbot.single(message)

    if message.content.lower().endswith(' demoty all'):
	    await demotbot.topInit(message)

    if message.content.lower().endswith(' komixxy'):
        await komixxy.run(message)

    if message.content.lower().endswith(' miejski'):
        await miejski.run(message)

    if message.content.lower().endswith(' fandemoty'):
    	await fandemonium.run(message)

@client.event
async def on_reaction_add(reaction, user):
    if user == client.user:
        return

    if reaction.emoji in "⬅️➡️🎲" and reaction.me == True:
    	await demotbot.handleReactions(reaction)

@client.event
async def on_reaction_remove(reaction, user):
    if user == client.user:
        return

    if reaction.emoji in "⬅️➡️🎲" and reaction.me == True:
    	await demotbot.handleReactions(reaction)

client.run(KEY)
