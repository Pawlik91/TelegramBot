import sys
import time
import random
import datetime
import telepot
import requests
import configparser
import bs4
from googletrans import Translator

def youtubeCrawler(searchTerm):
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


def handle(msg):

    chat_id = msg['chat']['id']
    userName = msg['chat']['first_name']

    command = msg['text']
    translatedCommand = translator.translate(command)
    sourceLanguage = translatedCommand.src
    operatingLanguage = 'en'

    #response = requests.post(config['Default']['URL'], data=translatedCommand.text)

    print ('got command \"%s\" from user \"%s\"'.format(command, userName))
    print ('translated into english: %s'.format(translatedCommand.text))

    greetingMessage = 'Hi ' + userName + ', I am happy to hear from you!'
    startShoppingMessage = 'Then let\'s have a look what Otto can offer for you!'

    for keyword in keywords:
        if keyword in translatedCommand.text:
            bot.sendMessage(chat_id, translator.translate(startShoppingMessage, src=operatingLanguage, dest=sourceLanguage).text)
            break
        if 'video' in translatedCommand.text:
            bot.sendMessage(chat_id, str( youtubeCrawler('Otto.de') ))
            break

    else: 
       bot.sendMessage(chat_id, translator.translate(greetingMessage, src=operatingLanguage, dest=sourceLanguage).text)



config = configparser.ConfigParser()
config.read('config.ini')


keywords = ['shop', 'buy']
translator = Translator()    
#youtube = youtube.YouTube(api_key=config['Google']['YouTube'])


bot = telepot.Bot(config['Bot']['token'])
bot.message_loop(handle)


print ('Listening')


while 1:
    time.sleep(10)