import schedule
import time
from mastodon import Mastodon

class Reports():
    """Kicks off a scheduled task to poll the reports and ping the bot if there's new reports"""
    def __init__(self, mastodon: Mastodon, config, bot, chat_id):
        self.mastodon:Mastodon = mastodon
        self.config = config
        self.bot = bot
        self.chat_id = chat_id
        self.seen_reports: set = set()

    
    def check_report_queue(self):
        """Checks report queue and sends a message using a bot"""
        try:
        	reports:dict = self.mastodon.admin_reports()
        	checked_ids = [id['id'] for id in reports]
        	new_ids = set(checked_ids).difference(self.seen_reports)
        	if len(new_ids) > 0:
            	self.bot.send_message(self.chat_id, f'{len(reports)} in the report queue!')
        	else:
            	print("no reports found")
        	self.seen_reports = self.seen_reports.union(new_ids)
		except Exception as e:
			print(e)
		finally:
			pass
        
    def start_monitoring(self):
        """Begin monitoring report queue"""
        schedule.every(1).minutes.do(self.check_report_queue)
        while True:
            schedule.run_pending()
            time.sleep(1)