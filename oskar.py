import sys
import time
import random
import datetime
import telepot
import requests
import configparser
from googletrans import Translator

reload(sys)
sys.setdefaultencoding('utf8')


def handle(msg):

    chat_id = msg['chat']['id']
    userName = msg['chat']['first_name']

    command = msg['text']
    translatedCommand = translator.translate(command)
    sourceLanguage = translatedCommand.src
    operatingLanguage = 'en'

    #response = requests.post(config['Default']['URL'], data=translatedCommand.text)

    print 'got command \"%s\" from user \"%s\"' % (command, userName)
    print 'translated into english: %s' % translatedCommand.text

    greetingMessage = 'Hi ' + userName + ', I am happy to hear from you!'
    startShoppingMessage = 'Then let\'s have a look what Otto can offer for you!'

    for keyword in keywords:
        if keyword in translatedCommand.text:
            bot.sendMessage(chat_id, translator.translate(startShoppingMessage, src=operatingLanguage, dest=sourceLanguage).text)
            break
    else: 
       bot.sendMessage(chat_id, translator.translate(greetingMessage, src=operatingLanguage, dest=sourceLanguage).text)


keywords = ['shop', 'buy']
translator = Translator()

config = configparser.ConfigParser()
config.read('config.ini')

bot = telepot.Bot(config['Bot']['token'])
bot.message_loop(handle)

print 'Listening'

while 1:
    time.sleep(10)