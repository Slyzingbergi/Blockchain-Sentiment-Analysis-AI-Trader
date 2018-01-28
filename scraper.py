from bs4 import BeautifulSoup
import requests
import csv
from textblob import TextBlob

# scan a bunch of news websites for cryptocurrency news

# find mentions of some cryptocurrencies (top 25 CCs right now)
# analyzes sentiments of the mentions
# algorithm determines the value and potentioal of the coin
# currently scrapes the websites:
#	-cryptoanswers
#	-ccn
#	-cnbc
#	-newsbtc
#	-bloomberg
#	-yahoo news
#	-


# contains all the headlines that we will
# analyze the sentiments of
headLines = []

headlinesOfInterest = set()

# some websites think you're ddossing unless you pose as a browser
headers = {'User-Agent':'Mozilla/5.0'}


# scrape a website. 
# tags: list of <html> tags to scrape info from
# speeds things up by not scraping evreyting on the website
# url is the url u want to scrape from
def getStuff (url, tags, pretendToBeMozilla=True):
	if pretendToBeMozilla:
		r = requests.get(url,headers=headers)
	else:
		r = requests.get(url,headers=headers)
	soup = BeautifulSoup(r.text, 'html.parser')

	for tag in tags:
		for text in soup.find_all(tag):
			headLines.append(text.getText())


sentiments = []

with open('keywords', newline='') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	for row in spamreader:

		try:
			# one of these is wrong in the data
			#print(row[5].split("=")[1])
			if row[5].split("=")[1] == "negative":
				sentiments.append((row[2].split("=")[1],False))
			elif row[5].split("=")[1] == "positive":
				sentiments.append((row[2].split("=")[1],True))
			else:
				sentiments.append((row[2].split("=")[1],False))

		except (ValueError, TypeError, IndexError):
			print("wtf")

# getting the data from crypto answers
# text found in <h3> tags

r = requests.get('https://cryptoanswers.net',headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')


# top 25 crypto list
cryptos = [("Bitcoin","BTC"), ("Ethereum","ETH"),\
("Ripple","XRP"), ("Bitcoin Cash","BCH"), ("Cardano","ADA"),\
("Stellar","XML"),("Litecoin","LTC"),("NEM","XEM"),("NEO","NEO"),\
("EOS","EOS"),("IOTA","MIOTA"),("Dash","DASH"),("Monero","XMR"),("TRON","TRX"),\
("VeChain","VEN"),("Bitcoin Gold","BTG"),\
("ICON","ICX"),("Ethereum Classic","ETC"),\
("Qtum","QTUM"),("Lisk","LSK"),("RaiBlocks","XRB"),\
("Populous","PPT"),("OmiseGO","OMG"),\
("Tether","USDT"),("Steem","STEEM")]

# website contains sentiments in <h3> tags
for text in soup.find_all('h3'):
	headLines.append(text.getText())


# need to pretend to be a mozilla browser for this site

r = requests.get('https://www.ccn.com/',headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

for text in soup.find_all("div", {"class": "slide-summary"}):
	headLines.append(text.getText())

for text in soup.find_all("div", {"class": "entry-title"}):
	headLines.append(text.getText())


# here we are going to be getting a bunch of web data
url = 'https://www.bloomberg.com/canada'
getStuff(url,["h1","h2","h3","a"])

url = 'https://ca.finance.yahoo.com/'
tags = ['h3','h2','h1']
getStuff(url,tags)

url = ''
tags = ''
getStuff(url,tags)

r = requests.get('https://www.cnbc.com/wealth/',headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

for text in soup.find_all("p", {"class":"desc"}):
	headLines.append(text.getText())


r = requests.get('https://www.newsbtc.com/',headers=headers)
soup = BeautifulSoup(r.text, 'html.parser')

for text in soup.find_all("p"):
	headLines.append(text.getText())

for text in soup.find_all("h3"):
	headLines.append(text.getText())


for headline in headLines:
	for crypto in cryptos:
		if headline.find(crypto[0]) != -1:
			headlinesOfInterest.add((headline,crypto))

final_sentiments = []

crypto_sentiments = {}

for headline in headlinesOfInterest:
	bl = TextBlob(headline[0])

	key = headline[1][1]

	if key not in crypto_sentiments:
		crypto_sentiments[key] = [bl.polarity * bl.subjectivity,1]
	else:
		crypto_sentiments[headline[1][1]][0] += bl.polarity * bl.subjectivity
		crypto_sentiments[headline[1][1]][1] += 1
	
for sentiment in crypto_sentiments:
	print(sentiment, " = ", crypto_sentiments[sentiment][0] / crypto_sentiments[sentiment][1])