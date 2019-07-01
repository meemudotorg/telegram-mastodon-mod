#!/usr/bin/env python
# Python mastodon telegram bot for automoderating
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from mastodon import Mastodon, StreamListener
from listeners.public import PublicStreamListener
from rules.status import StatusRules
import yaml


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update,context):
    """reply to start"""
    update.message.reply_text('ok!')

def error(update,context):
    """Log errors"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def setup():
    print("Enter your mastodon login name")
    print("Enter your mastodon password")
    print("Creating app on your server....")
    print("Ok thnx, saved credentials!")

def main():
    #open the settings file
    with open("settings.yml") as settings:
        config = yaml.safe_load(settings)

    #start masotdon.py client
    mastodon = Mastodon(
        client_id = 'pytooter_clientcred.secret',
        access_token = 'pytooter_usercred.secret',
        api_base_url =  config['server']['url']
    )

   # start the telegram bot.
    updater = Updater(config['telegram_api_key'], use_context=True)
    dp = updater.dispatcher

    #add handlers for commands
    dp.add_handler(CommandHandler("start", start))

    dp.add_error_handler(error)
    
    updater.start_polling()

    rules = StatusRules(config['rules'])

    listener = PublicStreamListener(
        bot = updater.bot,
        chat_id = config['chat_id'],
        rules =  rules
    )

    mastodon.stream_public(listener)
    updater.idle()
   

if __name__ == '__main__':
    main()


