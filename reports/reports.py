import sched

class ReportsWatcher():
    """Kicks off a scheduled task to poll the reports and ping the bot if there's new reports"""
    def __init__(self, mastodon, config, telegram):
        self.mastodon = mastodon
        self.config = config
        self.telegram = telegram
        s = sched.scheduler()
    def check_report_queue(self):
        pass