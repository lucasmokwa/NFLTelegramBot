import csv
import requests

def botSendText(mensagem, chatId, token):
    
    
    send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + str(chatId) + '&parse_mode=Markdown&text=' + mensagem

    response = requests.get(send_text)

    return response.json()


class player:
    def __init__(self, name, team,taken, value):
        self.name = name
        self.taken = taken
        self.team = team
        self.value = value

def readPlayerList():
    playerList = []

    with open('players.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not (row):    
                continue
            playerList.append(player(row[0], row[1], int(row[2]), float(row[3])))

    return playerList


def writePlayerList(playerList):
    
    with open('players.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for player in playerList:
            writer.writerow([player.name.lower(), player.team, player.taken, player.value])

    return 1

class proposta:
    def __init__(self, user, userId, player, value, status):
        self.user = user
        self.userId = userId
        self.player = player
        self.value = value
        self.status = status

def gravaProposta(proposta):
    fields = [proposta.user, proposta.userId, proposta.player, proposta.value , proposta.status]

    try:
        with open('proposta.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
    except:
        with open('proposta.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
    return 1

def atualizaProposta(propostaRecebida):

    fields = [propostaRecebida.user, propostaRecebida.userId, propostaRecebida.player, propostaRecebida.value , propostaRecebida.status]
    propostas = []

    with open('proposta.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not (row):    
                continue
            propostas.append(proposta(row[0], row[1], row[2], row[3],row[4]))
    
    for row in propostas:
        if row.userId == fields[1] and row.player == fields[2]:
            row.value = fields[3]
    
    with open('proposta.csv', 'w' , newline= '') as csvfile:
        writer = csv.writer(csvfile)
        
        for row in propostas:
            writer.writerow([row.user,row.userId,row.player,row.value,row.status])

    return 1


def gravaListaRecusados(proposta):
    fields = [proposta.user, proposta.userId, proposta.player, proposta.value , proposta.status]

    try:
        with open('listaRecusados.csv',  'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
    except:
        with open('listaRecusados.csv',  'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)

    return 1

def gravaListaConsideracao(proposta):
    fields = [proposta.user, proposta.userId,  proposta.player,proposta.value ,  proposta.status]
 
    try:
        with open('listaConsiderados.csv',  'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
    except:
        with open('listaConsiderados.csv',  'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)

    return 1

def carregaPropostas():
    propostas = []

    try:
        with open('proposta.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                if not (row):    
                    continue
                propostas.append(proposta(row[0], row[1], row[2], row[3],row[4]))
    except:
        print('erro')
       
    return propostas

def enviaMensagem(mensagem, player, userId , token):
    if (mensagem == 0):
        texto = 'A sua proposta pelo jogador ' + player + ' foi recusada pelo baixo valor, e seu agente encerrou as negociações. '
    elif(mensagem == 1):
        texto = 'A sua proposta pelo jogador ' + player + ' ainda está sob consideração.'

    botSendText(texto , userId , token)  
    
    return 1

def enviaMensagemCSV(mensagem, inputCsv, token):

    with open(inputCsv, 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not (row):    
                continue
            enviaMensagem(mensagem, row[2], row[1], token)
            
    return 1


def limpaProposta():

    propostas = []

    with open('listaConsiderados.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not (row):    
                continue
            propostas.append(proposta(row[0], row[1], row[2], row[3],row[4]))


    with open('proposta.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            for row in propostas:
                writer.writerow(row[0],row[1],row[2],row[3],row[4])
    return 1


def limpaListaConsiderar():

    with open('listaConsiderados.csv', 'w', newline= '') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow('')

    return 1
    

def readRefusedOffers():
    propostas = []

    with open('listaRecusados.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)

        for row in reader:
            if not (row):    
                continue
            propostas.append(proposta(row[0], row[1], row[2], row[3],row[4]))

    return propostas

# teste =  proposta(',','','','','')
# gravaListaRecusados(teste)
# print (teste.user)

# enviaMensagem(0, 'topeira', 1280874656 , '1173516505:AAHky7naNkUzRQDGnvsZK_UzknSiKC6rKQQ')


