from player import readPlayerList, writePlayerList, proposta, gravaProposta, carregaPropostas, gravaListaRecusados,gravaListaConsideracao,limpaListaConsiderar,readRefusedOffers
from player import enviaMensagemCSV,atualizaProposta
import csv 
import datetime

  #Function responsible for defining the message the user receives when he adds the bot
def start(update, context):
    context.bot.sendMessage(chat_id=update.effective_chat.id, text = "Bem vindo a Liga NFL, para fazer a sua proposta informe o nome do jogaor seguido do valor em milhões. Exemplo: Tom Brady, 5")

#function that converts all the text to Upper Caps
def caps(update, context):
    textCaps = ' ' . join(context.args).upper() 
    context.bot.sendMessage(chat_id = update.effective_chat.id, text = textCaps)


def addPlayer(update, context):

    # player = ' ' . join(context.args)
    # userName = update.message.from_user.name


    context.bot.sendMessage(chat_id =update.effective_chat.id, text = "Jogador Criado!")  


def recebeOferta(receivedMessage, user, userId):
# Verifica se a mensagem esta no formato correto (ok)
# Se existe o jogador (ok)
# Se o horario e valido (ok)
# Se o usuario ainda pode fazer propostas para esse jogador (ok)

    #horario em que mensagens podem ser recebidas
    ini = 9
    fim = 18

    now = int(datetime.datetime.now().hour)
    # print(now)
    if  now >= fim or now <ini:
        reply = 'O horário para negociações ainda não iniciou, elas começam às ' + str(ini) + ' horas e se encerram às ' + str(fim) + ' horas.'
        return reply 

    splitMessage = receivedMessage.split(',')

    # input no formato incorreto
    if len(splitMessage) != 2 :
        reply = "Mensagem no formato errado! Ela deve seguir o padrão do exemplo: JuJu Smith-Schuster, 5"

    else:

        #separa o input
        playerName = (splitMessage[0].lower()).strip()
        
        
        try:
            valorProposta = float(splitMessage[1])

        except:
            reply =  "Mensagem no formato errado! Ela deve seguir o padrão do exemplo: JuJu Smith-Schuster, 5"
            return reply

        #le csv com info dos jogadores
        players = readPlayerList()
        refusedOffers = readRefusedOffers()
        propostas = carregaPropostas()

        #search refused offers
        if any(i for i in refusedOffers if str(userId) == i.userId and i.player == playerName) == True:
            reply = 'Esse jogador encerrou negociações com você!'

            return reply
        
        #search earlier proposals
        if any(i for i in propostas if str(userId) == i.userId and i.player == playerName and float(i.value) >= valorProposta) == True:

            reply = 'Você já fez uma proposta mais alta a esse jogador!'

            return reply

        elif any(i for i in propostas if str(userId) == i.userId and i.player == playerName):

            reply = 'Proposta Atualizada!'
            enviaProposta = proposta (user, userId , playerName ,valorProposta, 0)
            atualizaProposta(enviaProposta)

            return reply
            
        #search players list for playerName input
        index = next((i for i, item in enumerate(players) if item.name.lower() == playerName), None)

        #se nao existir, assign reply 
        if index == None:
            reply = 'Não encontrei nenhum jogador com esse nome!'

        else:

            reply = 'Proposta enviada!'
            enviaProposta = proposta (user, userId , playerName ,valorProposta, 0)
            gravaProposta(enviaProposta)

    return reply

def avaliaPropostas():

    #inicia a variavel
    propostasConsiderar = 0

    #le e escreve o numero de propostas sendo consideradas
    #se o arquivo nao existe cria ele 
    try:
        with open('numeroPropostas.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                if not (row):    
                    continue

                propostasConsiderar = int(row[0])

    except:
         propostasConsiderar = int(4)

    novoNumeroPropostas = propostasConsiderar - 1

    with open('numeroPropostas.csv',  'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([(novoNumeroPropostas )])

    if novoNumeroPropostas <= 0:
        return -1

    #limpa lista de jogadores considerados
    limpaListaConsiderar()

    # jogadores = readPlayerList()
    propostas = carregaPropostas()
    
    #conjunto que vai conter todos os jogadores já avaliados
    jogadorAvaliado = set()

    for p in propostas:
        #avaliamos somente uma vez por jogador
        if p.player not in jogadorAvaliado:
            jogadorAvaliado.add(p.player)
            
            listaPropostas = []
            # procuramos todas as propostas pelo jogador
            for op in propostas:
                if op.player == p.player:
                    listaPropostas.append(op)

            #ordenamos pelo valor da proposta
            listaPropostas.sort(key=lambda x: x.value, reverse=True)

            #reseta o contador
            i = 0
            for x in listaPropostas:
               
                if i  < propostasConsiderar:
                    x.status = 0
                    gravaListaConsideracao(x)
                    
                else:
                    x.status = 1
                    #adiciona na lista negra do jogador
                    gravaListaRecusados(x)

                i = i + 1

    return propostasConsiderar

def replyOffer(update, context):
    receivedMessage = update.message.text
    userName = update.message.from_user.name
    userId = update.effective_chat.id


    reply = recebeOferta(receivedMessage, userName, userId)
    context.bot.sendMessage(chat_id =userId, text = reply) 



# avaliaPropostas()
# print(recebeOferta('Tom Brady,5.5','teste',1280874656))
# readRefusedOffers()