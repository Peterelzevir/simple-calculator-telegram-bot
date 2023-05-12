from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup

#kilid e bot ro midim be code
updater = Updater(token='5631592767:AAFBFxmY4NgIoZfxn0sV85pwXx54PztsrAQ', use_context=True)
#hame event haro bas bedim be in ke handle kone
dispatcher = updater.dispatcher

#??
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#hame tabe ha ba event haye moxtalef, update va context migiran.
def start(update, context):
    kb = [[KeyboardButton('/command1')],
          [KeyboardButton('/command2')]]
    kb_markup = ReplyKeyboardMarkup(kb)
    context.bot.send_message(chat_id=update.message.chat_id,
                     text="Hiiii",
                     reply_markup=kb_markup)

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

#bara command start tabe start ro tarif mikonim, va event esh ro midim be dispatcher
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#bara command caps tabe caps tarif mikonim va event esh ro midim be dispatcher
caps_handler = CommandHandler('caps', caps)
dispatcher.add_handler(caps_handler)

#bara massage ha menhaye command ha tabe echo ro tarif mikonim va midim be dispatcher
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title=query.upper(),
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)

#baraye inline tabe inline tarif mikonim midim be dispatcher
inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

#bot shuru be kar mikone
updater.start_polling()
