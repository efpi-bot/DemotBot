import discord
import requests
import random
import io
from bs4 import BeautifulSoup

class demotbot:

	def __init__(self):
		None

	async def run(self, message):

		query = message.content.replace('demoty','')
		print(query)
		response = requests.get(f'https://demotywatory.pl/szukaj?q={query}')
		soup = BeautifulSoup(response.content, 'html.parser')
		scriptTags = soup.find_all('script')
		paginatorElement = ''
		for i in scriptTags:
			if 'paginator' in str(i):
				paginatorElement = i
				break

		isSinglePage = False
		try:
			howManyPages = str(paginatorElement).split(',')[1]
		except IndexError:
			isSinglePage = True

		if isSinglePage == False:
			randomPageNumber = random.randint(1,int(howManyPages))
			resonse = requests.get(f'https://demotywatory.pl/szukaj/page/{randomPageNumber}?q={query}')
			soup = BeautifulSoup(response.content, 'html.parser')

		demotsUrlArray = soup.find_all(class_='demot_pic')

		try:
			randomDemot = random.choice(demotsUrlArray)
			imgUrl = randomDemot.a.img['src']
		except:
			await message.channel.send('nie ma')
			return

		imgFileName = imgUrl.split('/')[-1]

		imgResponse = requests.get(imgUrl, stream=True)
		data = io.BytesIO(imgResponse.content)
		await message.channel.send(file=discord.File(data, imgFileName))



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

    if message.content.endswith('demoty'):
    	with message.channel.typing():
        	await demotbot.run(message)

client.run(KEY)