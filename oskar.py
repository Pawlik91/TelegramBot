import sys
import time
import random
import datetime
import telepot
import requests
import configparser
import bs4
from googletrans import Translator

class MessageCounter(telepot.aio.helper.ChatHandler): 

    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)


    async def on_chat_message(self, msg):
        chat_id = msg['message_id']
        userName = msg['from']['first_name']

        command = msg['text']
        translatedCommand = translator.translate(command)
        sourceLanguage = translatedCommand.src
        operatingLanguage = 'en'

        #response = requests.post(config['Default']['URL'], data=translatedCommand.text)

        print ('got command \"{}\" from user \"{}\"'.format(command, userName))
        print ('translated into english: {}'.format(translatedCommand.text))

        greetingMessage = 'Hi ' + userName + ', I am happy to hear from you!'
        startShoppingMessage = 'Then let\'s have a look what Otto can offer for you!'


        words = translatedCommand.text.split(' ')
        wordCombinationList = [['between', 'and'], ['-'], ['from', 'to'], ['budget', 'is']]

        range = []

        for wordCombination in wordCombinationList:
            if all(word in words for word in wordCombination):
                for i in range(0, len(words))
                    if ("-" == words[i]):
                        range.append(words[i-1])      
                        range.append(words[i+1])
                        break
                    elif("budget" == words[i] ) and ("is" == words[i+1]):
                        range.append(words[i+2])
                        break
                    elif ( wordCombination[0] == words[i]) or (wordCombination[1] == words[i] ):
                        range.append(words[i+1])
                        break
        

        if (len(range)>1):
            priceFrom = range[0]
            priceTo = range[1]
        elif (len(range)==1):
            priceTo = range[0]
        

        for keyword in keywords:
            if keyword in translatedCommand.text:
                result = ( translator.translate(startShoppingMessage, src=operatingLanguage, dest=sourceLanguage).text)
                break
            elif 'video' in translatedCommand.text:
                result = ( str( self.youtubeCrawler('Otto.de') ))
                break
            elif 'list' in translatedCommand.text:
                result = productAPI.getAllProducts(brand = "LG", name = "TV", priceFrom = '30000', priceTo = '50000')
                result = result[0].name
                break
        else: 
            result = (translator.translate(greetingMessage, src=operatingLanguage, dest=sourceLanguage).text)

        await self.sender.sendMessage( str( result ) ) 


    def youtubeCrawler(self, searchTerm):
        text = requests.get('https://www.youtube.com/results?search_query='+searchTerm).text
        soup = bs4.BeautifulSoup(text, "html.parser")

        div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class'] ]
        # for d in div:
        d = div[0]
        img0 = d.find_all('img')[0]
        a0 = d.find_all('a')[0]
        imgL = img0['src'] if not img0.has_attr('data-thumb') else img0['data-thumb']
        a0 = [ x for x in d.find_all('a') if x.has_attr('title')][0]
        return (a0['title'] + '\n http://www.youtube.com/' + a0['href'] ) 





config = configparser.ConfigParser()
config.read('config.ini')


keywords = ['shop', 'buy']
translator = Translator()    
#youtube = youtube.YouTube(api_key=config['Google']['YouTube'])


bot = telepot.aio.DelegatorBot(config['Bot']['token']  , [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()