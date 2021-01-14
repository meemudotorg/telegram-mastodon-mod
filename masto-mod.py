#!/usr/bin/env python
# Python mastodon telegram bot for automoderating
import logging
import yaml
import argparse
import getpass
import signal
from concurrent.futures import ThreadPoolExecutor
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from mastodon import Mastodon, StreamListener
from listeners.public import PublicStreamListener
from rules.status import StatusRules
from reports.reports import Reports
from moderation.instances import Instances



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
    setup_db(mastodon,config)
    print("Ok thnx, saved credentials!")

def setup_db(mastodon: Mastodon, config):
    instances = Instances(mastodon, config, None, None)
    instances.init_sqllite_db()
    print("done...!")

def goodbye(bot, chat_id):
    bot.send_message(chat_id, "SIGHUP/SIGTERM... Goodbye!")



def main():
    """Kickoff the bot and run"""
    #parse args
    parser = argparse.ArgumentParser(description="Telegram mastodon mod bot")
    parser.add_argument("--setup", help="Initial setup of the bot, creates the app on the instance and a login token", action="store_true")
    parser.add_argument("--setup_db", help="Reinitialize, or initial set up of, instances database", action="store_true")
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
    if args.setup_db:
        setup_db(Mastodon, config)
        exit()
    
   # start the telegram bot.
    updater = Updater(config['telegram_api_key'], use_context=True)
    dp = updater.dispatcher

    dp.add_error_handler(error)
    
    updater.start_polling()

    #configure rules.
    rules = StatusRules(config['rules'])
    chat_id = config['chat_id']
    listener = PublicStreamListener(
        bot = updater.bot,
        chat_id = chat_id,
        rules =  rules
    )

    reports = Reports(
        mastodon = mastodon,
        config = config['reports'],
        bot = updater.bot,
        chat_id = chat_id
    )
    instances = Instances(
        mastodon = mastodon,
        config = config,
        bot = updater.bot,
        chat_id = chat_id
    )
    caller = goodbye(updater.bot,chat_id)
    signal.signal(signal.SIGHUP, caller)
    signal.signal(signal.SIGTERM, caller)
   
    updater.bot.send_message(chat_id, "HI! I'm online!")

    #start the listening features on different threads

    with ThreadPoolExecutor(max_workers=3) as e:
        e.submit(reports.start_monitoring)
        e.submit(instances.start_monitoring)
        e.submit(mastodon.stream_public, listener)
       
    
    updater.idle()
   

if __name__ == '__main__':
    main()


