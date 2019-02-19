import telebot
import postgresql as psql
from Conexao import *

con = Conexao('pq://readonly:123@100.100.100.203/poda_teste')
token = '695350005:AAHdicQ1IW-c359VOQFoO_wrKIDHWNV1iFo'
bot = telebot.TeleBot(token)
contador = int(1)

@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, 'Olá, seja bem vindo ao SEMF Bot, Como está você?')
    print(message)
    bot.send_message(message.chat.id, 'Olá Abdias')

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
   
    else:
        bot.send_message(message.chat.id, 'Não compreendi o que dissestes!')

bot.polling()
