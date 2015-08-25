#!/usr/bin/python

# local imports
import credentials

# python modules
import MySQLdb
import urllib
import json

class ParticipantItem(object):
    def __init__(self, match_id, participant_id, item0, item1, item2, item3, item4, item5, item6, win):
        self.match_id = match_id
        self.participant_id = participant_id
        self.item0 = item0
        self.item1 = item1
        self.item2 = item2
        self.item3 = item3
        self.item4 = item4
        self.item5 = item5
        self.item6 = item6
        self.items = [item0, item1, item2, item3, item4, item5, item6]
        self.win = win

    def __str__(self):
        return "match_id: " + str(self.match_id) + "\nparticipant_id: " + str(self.participant_id) + "\nitems: " + str(self.items) + "\nwin: " + str(self.win)

    def save(self):
        """
        Saves this ParticipantItem to the database.
        """
        
        # Get new database instance
        db = credentials.getDatabase()

        cur = db.cursor()
        query = '''INSERT IGNORE INTO participant_item (match_id, participant_id, item0, item1, item2, item3, item4, item5, item6, win)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

        data = (self.match_id, self.participant_id, self.item0, self.item1, self.item2, self.item3, self.item4, self.item5, self.item6, self.win)
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
        i = ParticipantItem(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9])

    # commit query
    db.commit()
    db.close()
    return i



