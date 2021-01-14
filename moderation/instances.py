from mastodon import Mastodon
import sys
import sqlite3
import time
import schedule

class Instances():
    """If we're lucky someday mastodon will let us do this thru the API."""
    def __init__(self, mastodon: Mastodon, config, bot, chat_id):
        self.mastodon:Mastodon = mastodon
        self.config = config
        self.bot = bot
        self.chat_id = chat_id
       
        pass
    def list_blocked_instances(self):
        pass
    def block_instance(self):
        pass
    def fetch_instances(self):
        instances = self.mastodon.instance_peers()
        return instances
    def init_sqllite_db(self):
        connection = sqlite3.connect("instances.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE instance (instanceUrl TEXT)")
        connection.close()

    def instance_digest(self):
        connection = sqlite3.connect("instances.db")
        try:
            print("Searching for new instances...")
            rows = set(self.__fetch_from_db())
            print(len(rows))
            rows = [x[0] for x in rows]
            instance_list = set(self.fetch_instances())
            print(len(instance_list))
            if len(rows) < 1:
                print("No instances saved...dumping initial list and moving on")
                self.__insert_new_instances(instance_list)
                return
            diff = [x for x in instance_list if x not in rows]
            print(len(diff))
            if len(diff) > 0:
                msg = " ".join(diff)
                print("found new instances..")
                self.__insert_new_instances(instance_list)
                self.bot.send_message(self.chat_id, f'NEW INSTANCES FOUND: {msg}')
            else:
                print("no new instances found")
        except sqlite3.ProgrammingError as e:
            print(e)
        finally:
            connection.close()
            print("done")
       
    
    def start_monitoring(self):
   
        schedule.every(1).minutes.do(self.instance_digest)
        while True:
            schedule.run_pending()
            time.sleep(1)
        
    def __fetch_from_db(self):
        connection = sqlite3.connect("instances.db")
        cursor =connection.cursor()
        rows = cursor.execute("SELECT instanceUrl FROM instance").fetchall()
        cursor.close()
        connection.close()
        return rows

    def  __insert_new_instances(self, urls):
        connection = sqlite3.connect("instances.db")
        cursor = connection.cursor()
        statement = "INSERT INTO instance (instanceUrl) VALUES (?);"
        for item in urls:
            cursor.execute(statement,(item,))
        connection.commit()
        cursor.close()
        connection.cose()