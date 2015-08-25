#!/usr/bin/python

# local imports
import credentials

# python modules
import MySQLdb
import urllib
import json

class ParticipantStat(object):
    def __init__(self, match_id, participant_id):
        self.match_id = match_id
        self.participant_id = participant_id
        self.kills = 0
        self.deaths = 0
        self.assists = 0
        self.magic_damage = 0
        self.magic_damage_champs = 0
        self.magic_damage_taken = 0
        self.champ_level = 0
        self.gold_earned = 0
        self.win = 0

    def __setKDA__(self, kills, deaths, assists):
        self.kills = kills
        self.deaths = deaths
        self.assists = assists

    def __setDamage__(self, magic_damage, magic_damage_champs, magic_damage_taken):
        self.magic_damage = magic_damage
        self.magic_damage_champs = magic_damage_champs
        self.magic_damage_taken = magic_damage_taken

    def __setOther__(self, champ_level, gold_earned, win):
        self.champ_level = champ_level
        self.gold_earned = gold_earned
        self.win = win

    def __str__(self):
        return "match_id: " + str(self.match_id) + "\nparticipant_id: " + str(self.participant_id)

    def save(self):
        """
        Saves this ParticipantStat to the database.
        """
        
        # Get new database instance
        db = credentials.getDatabase()

        cur = db.cursor()
        query = '''INSERT IGNORE INTO participant_stat (match_id, participant_id, kills, deaths, assists, magic_damage, magic_damage_champs, magic_damage_taken, champ_level, gold_earned, win)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);'''

        data = (self.match_id, self.participant_id, self.kills, self.deaths, self.assists, self.magic_damage, self.magic_damage_champs, self.magic_damage_taken, self.champ_level, self.gold_earned, self.win)
        cur.execute(query, data)

        # commit query
        db.commit()
        db.close()

        return True


def load(match_id, participant_id):
    '''
    Args:
        item_id: The id of the item to query
        match_id: The id of the match
        participant_id: The id of the participant
    Returns:
        A ParticipantStat object.
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT * FROM participant_stat WHERE match_id = %s AND participant_id = %s;'''
    cur.execute(query, match_id, participant_id)

    pa = ""
    for tup in cur:
        pa = ParticipantStat(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7], tup[8], tup[9], tup[10])

    # commit query
    db.commit()
    db.close()
    return pa

