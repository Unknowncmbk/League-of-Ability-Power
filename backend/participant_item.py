#!/usr/bin/python

# local imports
import credentials

# python modules
import MySQLdb
import urllib
import json

class ParticipantItem(object):
    def __init__(self, match_id, participant_id, item, slot, win):
        self.match_id = match_id
        self.participant_id = participant_id
        self.item = item
        self.slot = slot
        self.win = win

    def __str__(self):
        return "match_id: " + str(self.match_id) + "\nparticipant_id: " + str(self.participant_id) + "\nitem: " + str(self.item) + "\nslot: " + str(self.slot) + "\nwin: " + str(self.win)

    def save(self):
        """
        Saves this ParticipantItem to the database.
        """
        
        # Get new database instance
        db = credentials.getDatabase()

        cur = db.cursor()
        query = '''INSERT IGNORE INTO participant_item (match_id, participant_id, item, slot, win)
                VALUES(%s, %s, %s, %s, %s);'''

        data = (self.match_id, self.participant_id, self.item, self.slot, self.win)
        cur.execute(query, data)

        # commit query
        db.commit()
        db.close()

        return True


def load(match_id, participant_id):
    '''
    Args:
        match_id: The id of the match
        participant_id: The id of the participant
    Returns:
        A ParticipantItem object.
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT * FROM participant_item WHERE match_id = %s AND participant_id = %s;'''
    cur.execute(query, match_id, participant_id)

    i = ""
    for tup in cur:
        i = ParticipantItem(tup[0], tup[1], tup[2], tup[3], tup[4])

    # commit query
    db.commit()
    db.close()
    return i

def get_win_rate(item_id, version, region):
    '''
    Args:
        item_id: The id of the item
        version: version of the game
        region: region of the game
    Returns:
        The item's win rate.
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT I.id, I.name, COUNT(*) FROM item I, participant_item PI, game G WHERE PI.match_id=G.id AND I.id=PI.item AND PI.win=1 AND I.id = %s AND G.version = %s  AND region = %s  GROUP BY I.id ORDER BY COUNT(*) DESC;'''

    data = (item_id, version, region)
    cur.execute(query, data)

    item_name = "N/A"
    count = 0

    for tup in cur:
        item_name = str(tup[1])
        count = int(tup[2])

    # build response object
    item = {}
    item['id'] = item_id
    item['name'] = item_name
    item['number'] = count

    # commit query
    db.commit()
    db.close()

    return item

def get_usage_rate(item_id, version, region):
    '''
    Args:
        item_id: The id of the item
        version: version of the game
        region: region of the game
    Returns:
        The item's usage rate.
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT I.id, I.name, COUNT(*) FROM item I, participant_item PI, game G WHERE PI.match_id=G.id AND I.id=PI.item AND I.id = %s AND G.version = %s  AND region = %s  GROUP BY I.id ORDER BY COUNT(*) DESC;'''

    data = (item_id, version, region)
    cur.execute(query, data)

    item_name = "N/A"
    count = 0

    for tup in cur:
        item_name = str(tup[1])
        count = int(tup[2])

    # build response object
    item = {}
    item['id'] = item_id
    item['name'] = item_name
    item['number'] = count

    # commit query
    db.commit()
    db.close()

    return item

def get_all_rates(version, region):
    ap_items = [3157, 3089, 3285, 3135, 3078, 3165, 3116, 3027, 3020, 1058, 3001, 3151, 1026, 3100, 1056, 3174, 3025, 1052, 3092, 2041, 3115, 3158, 3152, 3057, 3040, 3136, 3708, 3724, 3113, 3041, 3108, 3010, 3146, 3114, 3070, 3303, 3003, 3504, 3101, 3098, 3023, 3060, 3716, 3145, 3028, 1027]

    total_records = 60
    response = {}
    items = []

    for item_id in ap_items:
        # {'number': 21, 'id': 3031, 'name': 'Infinity Edge'}
        usage = get_usage_rate(item_id, version, region)

        # {'number': 12, 'id': 3031, 'name': 'Infinity Edge'}
        win = get_win_rate(item_id, version, region)

        # construct item object
        item = {}
        item['id'] = item_id
        item['name'] = usage['name']
        item['usage_number'] = usage['number']
        item['win_number'] = win['number']
        if usage['number'] != 0:
            item['usage_rate'] = round(float(usage['number']) / float(total_records), 2)
        else:
            item['usage_rate'] = 0
        if win['number'] != 0:
            item['win_rate'] = round(float(win['number']) / float(usage['number']), 2)
        else:
            win['number'] = 0 
        items.append(item)

    response['repsonse'] = items
    return response


# print(get_all_rates('5.14.0.329', 'na'))
