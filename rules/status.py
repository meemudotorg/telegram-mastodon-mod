class StatusRules:
    """Rules to run on mastodon statuses. Needs to have the proper config in settings.yml"""
    def __init__(self, ruleConfig):
        if ruleConfig is None:
            raise Exception("You must provide screened_text in settings")
        self.screened_text = ruleConfig['screened_text']
    def has_screened_text(self, status):
        """Does a given status contain phrase from the screened list?"""
        rule_break = list(filter(lambda word: word in self.screened_text, status.split()))
        if(len(rule_break) > 0):
            return rule_break[0]
        return False
        
    