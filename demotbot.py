import discord
import requests
import random
import math
from bs4 import BeautifulSoup

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

		try:
			randomDemot = random.choice(demotsArray)
			imgUrl = randomDemot['src'].replace('_600.jpg','.jpg')
		except:
			await message.channel.send('nie ma')
			print('code: ' + str(response.status_code))
			print('\ndemotsArray:') #for debugging
			print(demotsArray)
			if isSinglePage == False:
				print('\nhowManyPages: ' + howManyPages + '\nrandomPageNumber: ' + randomPageNumber)
			return

		await message.channel.send(imgUrl)


# DISCORD BOT HERE

KEY = open('./key').read()

demotbot = demotbot()

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

client.run(KEY)