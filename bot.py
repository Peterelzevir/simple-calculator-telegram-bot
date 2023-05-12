import os

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from calculator import Calculator

def start(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a calculator bot. Send me a math expression and I'll calculate it for you.")

def help(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Send me a math expression and I'll calculate it for you.")

def calculate(update, context):

    expression = update.message.text

    try:

        result = Calculator.calculate(expression)

        context.bot.send_message(chat_id=update.effective_chat.id, text=result)

    except:

        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't calculate that expression.")

def main():

    token = os.environ.get('BOT_TOKEN')

    updater = Updater(token, use_context=True)

    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)

    help_handler = CommandHandler('help', help)

    calculate_handler = MessageHandler(Filters.text & ~Filters.command, calculate)

    dispatcher.add_handler(start_handler)

    dispatcher.add_handler(help_handler)

    dispatcher.add_handler(calculate_handler)

    port = int(os.environ.get('PORT', 5000))

    updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)

    updater.bot.setWebhook("https://your-app-name.herokuapp.com/" + token)

    updater.idle()

if __name__ == '__main__':

    main()

