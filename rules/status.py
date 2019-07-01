class StatusRules:
    """Rules to run on mastodon statuses. Needs to have the proper config in settings.yml"""
    def __init__(self, ruleConfig):
        if ruleConfig is None:
            raise Exception("You must provide screened_text in settings")
        self.screened_text = ruleConfig['screened_text']
        
        for rule in ruleConfig['screened_text']:
            print(rule)

    def has_screened_text(self, status):
        """Does a given status contain phrase from the screened list?"""
        print(status)
        print(any(word in status for word in self.screened_text))
        return any(word in status for word in self.screened_text)
        
    