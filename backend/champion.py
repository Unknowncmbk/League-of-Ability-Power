#!/usr/bin/python

import MySQLdb
import credentials
import urllib
import json

class Champion(object):
    def __init__(self, champion_id, name, title):
    	self.champion_id = champion_id
    	self.name = name
    	self.title = title

    def __str__(self):
        return "champion_id: " + str(self.champion_id) + ", name: " + str(self.name) + ", title: " + str(self.title)

    def save(self):
        """
        Saves this Champion to the database.
        """
        
        # Get new database instance
        db = credentials.getDatabase()

        cur = db.cursor()
        query = '''INSERT IGNORE INTO champion (id, name, title)
                VALUES(%s, %s, %s);'''

        data = (self.champion_id, self.name, self.title)
        cur.execute(query, data)

        # commit query
        db.commit()
        db.close()

        return True


def load(champion_id):
    '''
    Args:
        champion_id: The id of the champion to query
    Returns:
        A champion object.
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT * FROM champion WHERE id = %s;'''
    cur.execute(query, champion_id)

    c = ""
    for tup in cur:
        c = Champion(tup[0], tup[1], tup[2])

    # commit query
    db.commit()
    db.close()
    return c

def load_all():
    '''
    Returns:
        A list of all champions.
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT * FROM champion;'''
    cur.execute(query)

    champs = []
    for tup in cur:
        champs.append(Champion(tup[0], tup[1], tup[2]))

    # commit query
    db.commit()
    db.close()
    return champs

def fetch_champion(champion_id):
    '''
    Args:
        champion_id: The id of the champion to fetch
    Returns:
        A champion object, from Riot Games API.
    '''

    creds = credentials.getCredentials()
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + str(champion_id) + "?api_key=" + str(creds.api_key)
    print("Requesting url: " + str(url))

    response = urllib.urlopen(url);
    data = json.loads(response.read())

    if data is not None:
    	if 'id' in data:
    		champion_id = data['id']
    		name = ""
    		title = ""

    		if 'name' in data:
    			name = data['name']

    		if 'title' in data:
    			title = data['title']

    		return Champion(champion_id, name, title)

def fetch_all_champions():
	'''
	Returns:
		A list of all champion objects, from Riot Games API.
	'''

	creds = credentials.getCredentials()
	url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion?api_key=" + str(creds.api_key)
	print("Requesting url: " + str(url))

	response = urllib.urlopen(url);
	data = json.loads(response.read())['data']

	champs = []

	for key in data:
		info = data[key]

		if info is not None:
			if 'id' in info:
				champion_id = info['id']
				name = ""
				title = ""

				if 'name' in info:
					name = info['name']

				if 'title' in info:
					title = info['title']

				champs.append(Champion(champion_id, name, title))

	return champs

# # to populate the database
# result = fetch_all_champions()
# for c in result:
# 	c.save()




