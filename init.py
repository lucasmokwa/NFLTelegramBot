#import libraries
import telegram, logging, player
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue
from botFunctions import  start, replyOffer , addPlayer, avaliaPropostas
from player import enviaMensagemCSV
from datetime import time

#Define execution time
hora = 18
minuto = 1

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#token do NFLManagerBot
token = 'Enter your token'

bot = telegram.Bot(token = token)

updater = Updater(token = token, use_context= True)
dispatcher = updater.dispatcher

print('Bot iniciado!')
#when a start command is received, executes start
startHandler = CommandHandler('start', start)
dispatcher.add_handler(startHandler)

#add a new player to the list
startHandler = CommandHandler('add', addPlayer)
dispatcher.add_handler(startHandler)

#the actual evaluate option
offerHandler = MessageHandler(Filters.text & (~Filters.command), replyOffer)
dispatcher.add_handler(offerHandler)

#funcao que roda a evaluation 
dia = 1

def callback_minute(context: telegram.ext.CallbackContext): 
    #avalia as propostas
    propostasConsiderar = avaliaPropostas()
    print('Avaliando propostas, foram consideradas ' + str(propostasConsiderar) + 'propostas.' )

    if propostasConsiderar == -1:
        return -1

    #envia mensagens de recusa
    enviaMensagemCSV(0, 'listaRecusados.csv', token)
    print('Enviando mensagens recusa')

    #envia mensagens escolhidos
    if (propostasConsiderar == 1):
        enviaMensagemCSV(1, 'listaConsiderados.csv', token)
        print('Enviando mensagens Escolhidos')

    else:
    #envia mensagens de consideracao
        enviaMensagemCSV(1, 'listaConsiderados.csv', token)
        print('Enviando mensagens Consideracao')

#rodar evaluation
t = time(hora + 3, minuto, 00, 000000)
job = updater.job_queue
job.run_daily(callback_minute, t ,days=(0, 1, 2, 3, 4, 5, 6), context=None, name=None)


#Starts running the bot
updater.start_polling()

#makes it so it's stopable
updater.idle()


