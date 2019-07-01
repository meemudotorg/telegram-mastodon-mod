from mastodon import Mastodon, StreamListener
from rules.status import StatusRules
"""This class provides callbacks for actions taken based on the public mastodon stream, aka the federated timeline"""
class PublicStreamListener(StreamListener): 
    def on_update(self,status):
        """Processes incoming statuses on the fedi TL"""
        if self.rules.has_screened_text(status.content):
            self.bot.send_message(self.chat_id, f'Message contains {status.content}')
        self.bot.send_message(self.chat_id, 'New message?')
        #print(status)

    def __init__(self, bot, chat_id, rules):
        """Define the telegram bot and the telegram chat id to act on."""
        self.bot = bot
        self.chat_id = chat_id
        self.rules = rules
        
