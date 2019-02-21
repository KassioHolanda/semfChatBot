import telebot
import postgresql as psql
from Conexao import *

con2 = Conexao('pq://abdiasviana:Voljin!555@localhost/bot_telegram')
con = Conexao('pq://readonly:123@100.100.100.203/poda_teste')
#con = Conexao('pq://abdiasviana:Voljin!555@localhost/poda_teste')
token = '695350005:AAHdicQ1IW-c359VOQFoO_wrKIDHWNV1iFo'
bot = telebot.TeleBot(token)
contador = int(1)

#Comandos de boas vindas.
@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Olá, seja bem vindo ao SEMF Bot. Insira algum dos comandos abaixo para iniciar o atendimento!')
    bot.send_message(message.chat.id, '- Insira seu CPF ou CNPJ para consultar o NÚMERO e o STATUS de suas SOLICITAÇÕES.')
    bot.send_message(message.chat.id, '- Digite /contato para informações sobre Contatos.')
    bot.send_message(message.chat.id, '- Digite /ajuda para receber ajuda sobre os comandos.')
    
    
#Selecionado ajuda do bot para informações.
@bot.message_handler(commands = ['ajuda'])
def send_help(message):
    bot.send_message(message.chat.id, 'AJUDA:')
    bot.send_message(message.chat.id, '- Insira seu CPF ou CNPJ para consultar o NÚMERO e o STATUS de suas SOLICITAÇÕES.')
    bot.send_message(message.chat.id, '- Digite /contato para informações sobre Contatos.')
    bot.send_message(message.chat.id, '- Digite /ajuda para receber ajuda sobre os comandos.')
   
#Selecionado a opção /contato
@bot.message_handler(commands = ['contato'])
def send_contato(message):
    bot.send_message(message.chat.id, 'CONTATOS DA PREFEITURA')
    bot.send_message(message.chat.id, 'Digite /ajuda para receber ajuda sobre os comandos')

@bot.message_handler(func = lambda m: True)
def echo_all(message):
    contador = int(1)
    if len(message.text) == 11:
        numCpf = message.text
        print(message.text)
        sql1 = "select nome from pessoa where cpf = '{0}'".format(numCpf)
        sql2 = "select numerocompleto, status from requerimento r inner join pessoa p on r.pessoa_id = p.id where p.cpf = '{0}'".format(numCpf)
        print(sql1)
        print(sql2)
        rs1 = con.consultar(sql1)
        for linha1 in rs1:
            bot.send_message(message.chat.id, 'Sr(a): {}'.format(linha1[0]))
        bot.send_message(message.chat.id, 'Requerimentos:')
        rs2 = con.consultar(sql2)
        for linha2 in rs2:
            bot.send_message(message.chat.id, '{}: {}'.format(contador, linha2))
            contador += 1
        
        #salvando dados do usuário para envio direto de mensagem.
        chat_id = '{' + str(message.chat.id) + '}'
        user_name = '{' + str(message.chat.username) + '}'
        user_cpf = '{' + str(message.text) + '}'
        sql3 = "insert into usuario values (default, '{0}', '{1}', '{2}')".format(chat_id, user_name, user_cpf)
        print(sql3)
        if con2.manipular(sql3):
            print('Inserido com sucesso')
        else:
            print('Não inserido com sucesso')

       
    elif len(message.text) == 14:
        numCnpj = message.text
        print(message.text)
        sql1 = "select nome from pessoa where cnpj = '{0}'".format(numCnpj)
        sql2 = "select numerocompleto, status from requerimento r inner join pessoa p on r.pessoa_id = p.id where p.cnpj = '{}'".format(numCnpj)
        print(sql1)
        print(sql2)
        rs1 = con.consultar(sql1)
        for linha1 in rs1:
            bot.send_message(message.chat.id, 'Razão Social: {}'.format(linha1[0]))
        bot.send_message(message.chat.id, 'Requerimentos:')
        rs2 = con.consultar(sql2)
        for linha2 in rs2:
            bot.send_message(message.chat.id, '{}: {}'.format(contador, linha2))
            contador += 1
        
        #salvando dados do usuário para envio direto de mensagem.
        chat_id = '{' + str(message.chat.id) + '}'
        user_name = '{' + str(message.chat.username) + '}'
        user_cnpj ='{' + str(message.text) + '}'
        sql3 = "insert into usuario values (default, '{0}', '{1}', '{2}')".format(chat_id, user_name, user_cnpj)
        print(sql3)
        if con2.manipular(sql3):
            print('Inserido com sucesso')
        else:
            print('Não inserido com sucesso')
    
    elif len(message.text) == 6:
        numRequerimento = message.text
        print(message.text)
        sql = "select sr.status from situacaorequerimento sr inner join requerimento r on sr.requerimento_id = r.id where numerocompleto = '{0}'".format(numRequerimento)
        print(sql)
        rs = con.consultar(sql)
        bot.send_message(message.chat.id, 'Número do requerimento solicitado:')
        for linha in rs:
            bot.send_message(message.chat.id, '{}: {}'.format(contador, linha))
            contador += 1

    elif message.text == 'contato' or message.text == 'Contato' or message.text == 'CONTATO':
        send_contato(message)

    elif message.text == 'ajuda' or message.text == 'Ajuda' or message.text == 'AJUDA':
        send_help(message)

    else:
        bot.send_message(message.chat.id, 'Não compreendi o que dissestes!')
        send_help(message)

bot.polling()
