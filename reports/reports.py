import schedule
import time
from mastodon import Mastodon

class Reports():
    """Kicks off a scheduled task to poll the reports and ping the bot if there's new reports"""
    def __init__(self, mastodon: Mastodon, config, bot, chat_id):
        self.mastodon = mastodon
        self.config = config
        self.bot = bot
        self.chat_id = chat_id
        self.seen_reports = set()

    
    def check_report_queue(self):
        reports = self.mastodon.admin_reports()
        print(reports)
        self.bot.send_message(self.chat_id, f'{len(reports)} in the report queue!')
        
    def start_monitoring(self):
         schedule.every().minute.do(self.check_report_queue)
         
         while True:
            schedule.run_pending()
            time.sleep(1)