#!/usr/bin/python

# local imports
import credentials

# python modules
import MySQLdb
import urllib
import json

class Item(object):
    def __init__(self, item_id, name, desc, item_group):
        self.item_id = item_id
        self.name = name
        self.desc = desc
        self.item_group = item_group

    def __str__(self):
        return "item_id: " + str(self.item_id) + "\nname: " + str(self.name) + "\ndescription: " + str(self.desc) + "\nitem_group: " + str(self.item_group)

    def save(self):
        """
        Saves this Item to the database.
        """
        
        # Get new database instance
        db = credentials.getDatabase()

        cur = db.cursor()
        query = '''INSERT IGNORE INTO item (id, name, description, item_group)
                VALUES(%s, %s, %s, %s);'''

        data = (self.item_id, self.name, self.desc, self.item_group)
        cur.execute(query, data)

        # commit query
        db.commit()
        db.close()

        return True


def load(item_id):
    '''
    Args:
        item_id: The id of the item to query
    Returns:
        An Item object.
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT * FROM item WHERE id = %s;'''
    cur.execute(query, champion_id)

    i = ""
    for tup in cur:
        i = Item(tup[0], tup[1], tup[2], tup[3])

    # commit query
    db.commit()
    db.close()
    return i

def load_all():
    '''
    Returns:
        A list of all items.
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT * FROM item;'''
    cur.execute(query)

    items = []
    for tup in cur:
        items.append(Item(tup[0], tup[1], tup[2], tup[3]))

    # commit query
    db.commit()
    db.close()
    return items

def fetch_item(item_id):
    '''
    Args:
        item_id: The id of the item to fetch
    Returns:
        An Item object, from Riot Games API.
    '''

    creds = credentials.getCredentials()
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/item/" + str(item_id) + "?api_key=" + str(creds.api_key)
    print("Requesting url: " + str(url))

    response = urllib.urlopen(url);
    data = json.loads(response.read())

    if data is not None:
        if 'id' in data:
            item_id = data['id']
            name = ""
            desc = ""
            item_group = ""

            if 'name' in data:
                name = data['name']

            if 'description' in data:
                desc = data['description']

            if 'group' in data:
                item_group = data['group']

            return Item(item_id, name, desc, item_group)

def fetch_all_items():
    '''
    Returns:
        A list of all items objects, from Riot Games API.
    '''

    creds = credentials.getCredentials()
    url = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/item?api_key=" + str(creds.api_key)
    print("Requesting url: " + str(url))

    response = urllib.urlopen(url);
    data = json.loads(response.read())['data']

    items = []

    for key in data:
        info = data[key]

        if info is not None:
            if 'id' in info:
                item_id = info['id']
                name = ""
                desc = ""
                item_group = ""
                
                if 'name' in info:
                    name = info['name']
                
                if 'description' in info:
                    desc = info['description']

                if 'group' in info:
                    item_group = info['group']

                items.append(Item(item_id, name, desc, item_group))

    return items

# i = fetch_item(3725)
# i.save()

# result = fetch_all_items()
# for i in result:
#     i.save()




