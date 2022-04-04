from time import sleep
import telebot
import re
import os
from db_levvo import *

token = os.environ['TOKEN_TELEGRAM']
bot = telebot.TeleBot(token)


# verifica se é um e-mail válido ou se foi inserido algum e-mail após o comando /listrar pedidos
def verificaEmail(mensagem):
    try:
        email = mensagem.text.split(' ')[1]
        if email!= None:
            result = re.search(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$', email)
            return result
    except IndexError:
        return False
    else:
        return False

# retorna pedidos com base no e-mail do cliente - recebe como parâmetro a mensagem do telegram
def consultaPedidosEmail(mensagem):
    report = "E-mail não localizado, por favor insira um novo e-mail digitando: /listarpedidos [novo e-mail]"
    if verificaEmail(mensagem):
        email = mensagem.text.split(' ')[1]
        entregas = listaEntregasCliente(email)
        # Caso não localize nenhum cliente retorna o report
        if not entregas:
            return report
        text = ''
        for entrega in entregas:
            text += f'''Nº Entrega: {entrega['N Entrega']}
Descrição: {entrega['Descricao']}
Endereço de Coleta: 
    {entrega['Endereço de Coleta']}
Endereço de Final: 
    {entrega['Endereço de Coleta']}'''
            text+= ' \n\n'
        return text

    return report

@bot.message_handler(commands=["listarpedidos"])
def opcaoListarPedidos(mensagem):
    print(mensagem.text)
    retornoEmail = consultaPedidosEmail(mensagem)
    bot.send_message(mensagem.chat.id, retornoEmail)



####################### Inicia com essa mensagem ###################


def verificar(mensagem):
    return True

@bot.message_handler(func=verificar)
def responder(message):
   keyboard = telebot.types.InlineKeyboardMarkup()
   keyboard.add(
       telebot.types.InlineKeyboardButton(
           'Ir até a Levvo', url='telegram.me/bastosgabriel312'
       )
   )
   keyboard.add(
       telebot.types.InlineKeyboardButton(
           'Fale com um representante', url='telegram.me/bastosgabriel312'
       )   
   )

   bot.send_message(
       message.chat.id,
       ' SEJA BEM VINDO A LEVVO  \n\n' +
       '- Para Listar pedidos envie /listarpedidos [seu e-mail]\n',
       reply_markup=keyboard
   )




bot.polling()