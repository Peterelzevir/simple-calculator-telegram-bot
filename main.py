from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup
import re

updater = Updater(token='5631592767:AAFBFxmY4NgIoZfxn0sV85pwXx54PztsrAQ', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

Current = "0"

def start(update, context):
    global Current
    kb = [[KeyboardButton('c'), KeyboardButton('()'), KeyboardButton('÷'), KeyboardButton('del')],
        [KeyboardButton('7'), KeyboardButton('8'), KeyboardButton('9'), KeyboardButton('×')],
        [KeyboardButton('4'), KeyboardButton('5'), KeyboardButton('6'), KeyboardButton('-')],   
        [KeyboardButton('1'), KeyboardButton('2'), KeyboardButton('3'), KeyboardButton('+')],
        [KeyboardButton(' '), KeyboardButton('0'), KeyboardButton('.'), KeyboardButton('=')]]
    kb_markup = ReplyKeyboardMarkup(kb, True)
    Current = "0"
    context.bot.send_message(chat_id=update.message.chat_id, text="Let's do this!", reply_markup=kb_markup)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def end(update, context):
    updater.stop()

end_handler = CommandHandler('end', end)
dispatcher.add_handler(end_handler)

def display(update, context):
    global Current
    context.bot.send_message(chat_id=update.message.chat_id, text=Current)

def number(update, context):
    global Current
    if len(Current) != 0 and Current[-1] == '0' and (len(Current) == 1 or Current[-2].isdigit() == False):
        Current = Current[0:-1]
    Current += update.message.text

def number_0(update, context):
    global Current
    if (len(Current) != 0 and Current[-1] != '0') or (len(Current) > 1 and Current[-2].isdigit()):
        Current += "0"

def dot(update, context):
    global Current
    for i in range(len(Current) - 1, -1, -1):
        if Current[i].isdigit() == False and Current[i] != '.':
            break
        if Current[i] == '.':
            return
    Current += '.'
        
def operator(update, context):
    global Current
    if len(Current) != 0 and Current[-1].isdigit():
        Current += update.message.text
    elif len(Current) != 0:
        Current = Current[0:-1]
        Current += update.message.text

def delete(update, context):
    global Current
    if len(Current) != 0:
        Current = Current[0:-1]

def equal(update, context):
    global Current
    if len(Current) == 0 or (Current[-1].isdigit() == False and Current[-1] != '.'):
        return
    split_with_operators = re.split("(\×|\÷|\+|\-)", Current)
    split_with_Numbers = re.split("([0-9.]+)", Current)
    ans = float(split_with_operators[0])
    for i in range(1, len(split_with_operators)):
        op = split_with_Numbers[i]
        if op == '+':
            ans += float(split_with_operators[i])
        elif op == '-':
            ans -= float(split_with_operators[i])
        elif op == '×':
            ans *= float(split_with_operators[i])
        elif op == '÷':
            if (float(split_with_operators[i]) == 0):
                return
            ans /= float(split_with_operators[i])
    Current = str(ans)

def parser(update, context):
    switchVar = update.message.text
    if switchVar.isdigit() and int(switchVar) > 0 and int(switchVar) < 10:
        number(update, context)
    elif switchVar.isdigit() and int(switchVar) == 0:
        number_0(update, context)
    elif switchVar == '.':
        dot(update, context)
    elif switchVar == '+' or switchVar == '-' or switchVar == '×' or switchVar == '÷':
        operator(update, context)
    elif switchVar == 'c':
        start(update, context)
    elif switchVar == "del":
        delete(update, context)
    elif switchVar == '=':
        equal(update, context)
    display(update, context)

messageHandler = MessageHandler(Filters.text & (~Filters.command), parser)
dispatcher.add_handler(messageHandler)

updater.start_polling()
