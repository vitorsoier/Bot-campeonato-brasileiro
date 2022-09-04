"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import tabulate

from scraping import arquivo
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def tabela (update: Update, context: CallbackContext) -> None:
    serie_a, serie_b = dados()
    update.message.reply_text(serie_a.to_string(formatters={'Text':'{{:<{}s}}'.format(serie_a['time'].str.len().max()).format}, index=False))


def time(update : Update, context: CallbackContext) -> None:
    """"select the team you want to track"""
    


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def dados():

    pagina = arquivo()
    hmlt1, html2 = pagina.obtem_html("https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-a-2022/", 
                                "https://www.cnnbrasil.com.br/esporte/futebol/tabela-brasileirao-serie-b-2022/")

    df1, df2 = pagina.gerando_df(hmlt1, html2)

    serie_a, serie_b = pagina.formater(df1, df2)

    return serie_a, serie_b

def main() -> None:
    """Start the bot."""
    with open ('token.txt', 'r') as credenciais:
        token = credenciais.read()

    updater = Updater(token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("tabela", tabela))

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()
    

if __name__ == '__main__':
    main()