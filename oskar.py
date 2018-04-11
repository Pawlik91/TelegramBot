import sys
import time
import random
import datetime
import telepot
#import requests
#import configparser
#from google.cloud import translate
#from google.auth import app_engine

from googletrans import Translator

def handle(msg):

    chat_id = msg['chat']['id']
    userName = msg['chat']['first_name']

    command = msg['text']
    translatedCommand = translator.translate(command)
    print translatedCommand


    print 'got command \"%s\" from user \"%s\"' % (command, userName)
    print 'translated into english: %s' % translatedCommand

    for keyword in keywords:
        if keyword in command:
            bot.sendMessage(chat_id, str('Dann sehen wir mal, was Otto so im Angebot hat!'))
            break
    else: 
       bot.sendMessage(chat_id, str('Hallo ' + userName + ', ich freue mich, von dir zu hoeren!'))


keywords = ['shoppen', 'einkaufen', 'kauf', 'shopping']
translator = Translator()    


bot = telepot.Bot('509164385:AAE0_pOzH6fTPIWO7jc1zm1-08lbKqd55kM')
bot.message_loop(handle)

print 'Listening'

while 1:
    time.sleep(10)