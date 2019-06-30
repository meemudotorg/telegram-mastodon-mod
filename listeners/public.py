from mastodon import Mastodon, StreamListener
"""This class provides callbacks for actions taken based on the public mastodon stream, aka the federated timeline"""
class PublicStreamListener(StreamListener): 
    def on_update(self,status):
        """Processes incoming statuses on the fedi TL"""
        self.bot.send_message(self.chat_id, 'New message?')
        print(status)

    def __init__(self, bot, chat_id):
        """Define the telegram bot and the telegram chat id to act on."""
        self.bot = bot
        self.chat_id = chat_id
