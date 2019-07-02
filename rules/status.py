import re

class StatusRules:
    """Rules to run on mastodon statuses. Needs to have the proper config in settings.yml"""
    def __init__(self, rule_config):
        if rule_config is None:
            raise Exception("You must provide rules in settings")
        self.rule_config = rule_config
        print(rule_config)
    def has_screened_text(self, status):
        """Does a given status match a pattern from the rules list?"""
        for rule in self.rule_config:
            pattern = rule['regex']
            print(pattern)
            result = re.search(pattern, status)
            if result:
                print(result)
                return rule['name']
        return False
        
