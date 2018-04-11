import sys
import time
import random
import datetime
import telepot
import requests
import configparser
from googletrans import Translator


def handle(msg):

    chat_id = msg['chat']['id']
    userName = msg['chat']['first_name']

    command = msg['text']
    translatedCommand = translator.translate(command).text

    response = requests.post(config['Default']['URL'], data=translatedCommand)

    print 'got command \"%s\" from user \"%s\"' % (command, userName)
    print 'translated into english: %s' % translatedCommand

    for keyword in keywords:
        if keyword in translatedCommand:
            bot.sendMessage(chat_id, str('Dann sehen wir mal, was Otto so im Angebot hat!'))
            break
    else: 
       bot.sendMessage(chat_id, str('Hallo ' + userName + ', ich freue mich, von dir zu hoeren!'))


keywords = ['shop', 'buy']
translator = Translator()    

config = configparser.ConfigParser()
config.read('config.ini')

bot = telepot.Bot(config['Bot']['token'])
bot.message_loop(handle)

print 'Listening'

while 1:
    time.sleep(10)