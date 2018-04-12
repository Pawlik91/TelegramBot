import sys
import configparser
import asyncio
import telepot
import requests
import bs4
from googletrans import Translator
from telepot.aio.loop import MessageLoop
from telepot.aio.delegate import per_chat_id, create_open, pave_event_space
import productAPI
import nltk
import random
import NTree

class MessageCounter(telepot.aio.helper.ChatHandler): 

    def __init__(self, *args, **kwargs):
        super(MessageCounter, self).__init__(*args, **kwargs)


    async def on_chat_message(self, msg):
        chat_id = msg['message_id']
        userName = msg['from']['first_name']

        # if(db.userInDB(chat_id) == False):
        #     print('t')

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
                for i in range(0, len(words)):
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
        

        #ToDo: Wenn ein wort in Tree ist -> neue Kategorie 
        stopwords = [ "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the" ]

        corpus=[token for token in words if token not in stopwords]
        # Im Corpus liegen jetzt nur noch Kategorieren, Marken und Produkte        

        categories = []
        # Nach Kategorie im Tree suchen
        for word in corpus:
            if NTree.isPartOfTree(word):
                categories.append(word)

        # Gefundene Kategorien aus Korpus löschen
        corpus=[token for token in words if token not in categories]

        # Übrig sollten nur noch Brands und Produkte sein
        jokes = ["Ich soll einen Witz erzählen? \n Ich kenne keine Witze du Otto!", "Alle Kinder haben eine Devise, nur nicht Otto, der hat ein Motto.", "Schachmatt", "Ey, du Otto!"]
        springSummerTrends = "Spring and summer trends 2018 will be nothing but bright, bold and beautiful. Top Five trends are polka dots, pastels, fringe, asymmetry and checks. Looking forward to seeing you dressed that way!"
        autumnWinterTrends = "How should I now? I am quite intelligent, but no fortune teller. Let\'s wait and see!"

        for keyword in keywords:
            if keyword in corpus:
                result = ( translator.translate(startShoppingMessage, src=operatingLanguage, dest=sourceLanguage).text)
                break
            elif 'video' in corpus:
                result = ( str( self.youtubeCrawler('Otto.de') ))
                break
            elif 'list' in corpus:
                result = productAPI.getAllProducts(brand = "LG", name = "TV", priceFrom = priceFrom, priceTo = priceTo)
                result = result[0].name
                break
            elif 'joke' in corpus:
                result = jokes[random.randrange(0, len(jokes)-1)]
                break
            elif 'trend' in corpus:
                if 'winter' in corpus:
                    result = autumnWinterTrends
                    break
                elif 'autumn' in corpus:
                    result = autumnWinterTrends
                    break
                elif 'spring' in corpus:
                    result = springSummerTrends
                    break
                elif 'summer' in corpus:
                    result = springSummerTrends
                    break
                result = springSummerTrends
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

bot = telepot.aio.DelegatorBot(config['Bot']['token']  , [
    pave_event_space()(
        per_chat_id(), create_open, MessageCounter, timeout=10),
])

NTree.initTree()

loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot).run_forever())
print('Listening ...')

loop.run_forever()