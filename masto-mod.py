#!/usr/bin/env python
# Python mastodon telegram bot for automoderating
import logging
import yaml
import argparse
import getpass
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from mastodon import Mastodon, StreamListener
from listeners.public import PublicStreamListener
from rules.status import StatusRules
from reports.reports import Reports



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def error(update,context):
    """Log errors"""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def setup(config):
    """One time setup for the bot -- creates the api key and secrets you'll need to hit yr instance"""
    print("Enter your bot's mastodon login:")
    username = input()
    print("Enter your bot's mastodon password")
    password = getpass.getpass()
    print("Creating app on your server....")
    Mastodon.create_app(
        config['server']['app_name'],
        api_base_url = config['server']['url'],
        to_file = 'pytooter_clientcred.secret',
        scopes= ['admin:read', 'read']

    )
    print("app created, logging in...")
    mastodon = Mastodon(
        client_id = 'pytooter_clientcred.secret',
        api_base_url = config['server']['url']
    )
    mastodon.log_in(
        username,
        password,
        to_file = 'pytooter_usercred.secret',
        scopes=['admin:read','read']
    )
    print("Ok thnx, saved credentials!")


def main():
    """Kickoff the bot and run"""
    #parse args
    parser = argparse.ArgumentParser(description="Telegram mastodon mod bot")
    parser.add_argument("--setup", help="Initial setup of the bot, creates the app on the instance and a login token", action="store_true")
    args = parser.parse_args()
   
    #open the settings file
    with open("settings.yml") as settings:
        config = yaml.safe_load(settings)
    
    if args.setup:
        setup(config)
        exit()
    
    #start masotdon.py client
    mastodon = Mastodon(
        client_id = 'pytooter_clientcred.secret',
        access_token = 'pytooter_usercred.secret',
        api_base_url =  config['server']['url']
    )

   # start the telegram bot.
    updater = Updater(config['telegram_api_key'], use_context=True)
    dp = updater.dispatcher

    dp.add_error_handler(error)
    
    updater.start_polling()

    #configure rules.
    rules = StatusRules(config['rules'])

    listener = PublicStreamListener(
        bot = updater.bot,
        chat_id = config['chat_id'],
        rules =  rules
    )

    reports = Reports(
        mastodon = mastodon,
        config = config['reports'],
        bot = updater.bot,
        chat_id = config['chat_id']
    )

    reports.start_monitoring()

    mastodon.stream_public(listener)
    
    updater.idle()
   

if __name__ == '__main__':
    main()


