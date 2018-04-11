import sys
import time
import random
import datetime
import telepot
import requests
import configparser
from google.cloud import translate
from google.auth import app_engine
    import googleapiclient.discovery

def handle(msg):
    config = configparser.ConfigParser()
    config.read('config.ini')
    googleCredentials = config['Google']['Credentials']

    chat_id = msg['chat']['id']
    userName = msg['chat']['first_name']

    command = msg['text']

    translate_client = translate.Client()
    result = translate_client.detect_language(command)


    print 'Text: %s' % command
    print 'Confidence: %s' % result['confidence'] 
    print 'Language: %s' % result['language']

    bot.sendMessage(chat_id, 'Language: %s' % result['language'] )
    bot.sendMessage(chat_id, 'Confidence: %s' % result['confidence'] )

    #user = telegram.user()

    print 'got command : %s' % command
    print 'from user: ' + userName

    if 'shoppen' in command:
        bot.sendMessage(chat_id, str('Dann sehen wir mal, was Otto so im Angebot hat!'))
    else: 
       bot.sendMessage(chat_id, str('Hallo ' + userName + ', ich freue mich, von dir zu hoeren!'))


bot = telepot.Bot('573809489:AAHAwbrgWU6wePwXOq1aGqd5Ot5xHE1276M')
bot.message_loop(handle)

print 'Listening'

while 1:
    time.sleep(10)