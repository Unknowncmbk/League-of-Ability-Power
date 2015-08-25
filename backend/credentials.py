import json
import MySQLdb

class Credentials(object):
    def __init__(self, api_key, host, username, password, database):
        self.api_key = api_key
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    def __str__(self):
        return "api_key: " + str(self.api_key) + "\nhost: " + str(self.host) + "\nuser: " + str(self.username) + "\npass: " + str(self.password) + "\ndb: " + str(self.database) 


#read file for database details, riot api key
json_data=open("../credentials.txt").read()
data = json.loads(json_data)

r_creds = data["riot-creds"]
d_creds = data["database-creds"]

creds = Credentials(r_creds["api-key"], d_creds["host"], d_creds["user"], d_creds["password"], d_creds["database"])

def getCredentials():
    """
    Returns:
        The construct credentials object.
    """
    return creds

def getDatabase():
    return MySQLdb.connect(host=creds.host, user=creds.username, passwd=creds.password, db=creds.database)