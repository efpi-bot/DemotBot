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

		howManyResults = ''
		for string in soup.stripped_strings:
			if 'Znalazłem' in string:
				for i in string:
					if str.isdigit(i):
						howManyResults += i

		if howManyResults == '':
			await message.channel.send('nie ma')
			return

		howManyResults = int(howManyResults)
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

	async def run(self, message):

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


# DISCORD BOT HERE

KEY = open('./key').read()

demotbot = demotbot()
komixxy = komixxy()
miejski = miejski()
fandemonium = fandemonium()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().endswith(' demoty'):
        await demotbot.run(message)

    if message.content.lower().endswith(' komixxy'):
        await komixxy.run(message)

    if message.content.lower().endswith(' miejski'):
        await miejski.run(message)

    if message.content.lower().endswith(' fandemoty'):
    	await fandemonium.run(message)

client.run(KEY)
