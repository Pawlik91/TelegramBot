import sys
import time
import random
import datetime
import telepot

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    print 'got command : %s' % command

    if command == 'Ich will shoppen!':
        bot.sendMessage(chat_id, str('Dann sehen wir mal, was Otto so im Angebot hat!'))


bot = teleport.Bot('509164385:AAE0_pOzH6fTPIWO7jc1zm1-08lbKqd55kM')
bot.message_loop(handle)