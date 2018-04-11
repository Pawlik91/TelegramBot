import sys
import time
import random
import datetime
import telepot
import telegram

def handle(msg):
    chat_id = msg['chat']['id']
    userName = msg['chat']['first_name']

    #user = telegram.user()
    command = msg['text']

    print 'got command : %s' % command
    print 'from user: ' + userName

    if 'shoppen' in command:
        bot.sendMessage(chat_id, str('Dann sehen wir mal, was Otto so im Angebot hat!'))
    else: 
       bot.sendMessage(chat_id, str('Hallo ' + userName + ', ich freue mich, von dir zu hoeren!'))


bot = telepot.Bot('509164385:AAE0_pOzH6fTPIWO7jc1zm1-08lbKqd55kM')
bot.message_loop(handle)

print 'Listening'

while 1:
    time.sleep(10)