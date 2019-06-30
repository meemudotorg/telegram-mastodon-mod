#!/usr/bin/env python
# Python mastodon telegram bot for automoderating

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from mastodon import Mastodon, StreamListener

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

class AutomodStreamListener(StreamListener): 
    def on_update(self,status):
        self.bot.send_message(17631065, 'New message?')
        print(status)

    def __init__(self, bot):
        self.bot = bot

def start(update,context):
    """reply to start"""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo msg"""
    update.message.reply_text(update.message.text)

def error(update,context):
    """Log errors"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    mastodon = Mastodon(
        client_id = 'pytooter_clientcred.secret',
        access_token = 'pytooter_usercred.secret',
        api_base_url = 'https://meemu.org'
    )
  
    """Start bot."""
    updater = Updater("644394284:AAG_J2PQ13ATLjIVqsqoN8u1Ei3jxkNhun4", use_context=True)
    dp = updater.dispatcher

    #add handlers for commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    #echo non-commands
    dp.add_handler(MessageHandler(Filters.text, echo))

    dp.add_error_handler(error)
    
    
    updater.start_polling()
    listener = AutomodStreamListener(
        bot = updater.bot
    )
    mastodon.stream_public(listener)
    updater.idle()
   

if __name__ == '__main__':
    main()


