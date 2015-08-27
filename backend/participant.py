#!/usr/bin/python

# local imports
import credentials
from participant_stat import ParticipantStat
from participant_item import ParticipantItem

# python modules
import MySQLdb
import urllib
import json

class Participant(object):
    def __init__(self, match_id, participant_id, champion_id, team_id, win, lane, inventory, stat):
        self.match_id = match_id
        self.participant_id = participant_id
        self.champion_id = champion_id
        self.team_id = team_id
        self.win = win
        self.lane = lane
        self.inventory = inventory
        self.stat = stat

    def __str__(self):
        return "match_id: " + str(self.match_id) + "\nparticipant_id: " + str(self.participant_id) + "\nchampion_id: " + str(self.champion_id) + "\nteam_id: " + str(self.team_id) + "\nwin: " + str(self.win) + "\nlane: " + str(self.lane)

    def save(self):
        """
        Saves this Participant to the database.
        """
        
        # Get new database instance
        db = credentials.getDatabase()

        cur = db.cursor()
        query = '''INSERT IGNORE INTO participant (match_id, participant_id, champion_id, team_id, win, lane)
                VALUES(%s, %s, %s, %s, %s, %s);'''

        data = (self.match_id, self.participant_id, self.champion_id, self.team_id, self.win, self.lane)
        cur.execute(query, data)

        # commit query
        db.commit()
        db.close()

        self.save_inventory()
        self.save_stats()

        return True

    def save_inventory(self):
        for item in self.inventory:
            item.save()

    def save_stats(self):
        stats = self.stat
        stats.save()


def load(match_id, participant_id):
    '''
    Args:
        match_id: The id of the match
        participant_id: The id of the participant
    Returns:
        An Participant object.
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT * FROM participant WHERE match_id = %s AND participant_id = %s;'''
    cur.execute(query, match_id, participant_id)

    p = ""
    for tup in cur:
        p = Participant(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])

    # commit query
    db.commit()
    db.close()
    return p