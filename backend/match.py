#!/usr/bin/python

# local imports
import credentials
from participant import Participant
from participant_stat import ParticipantStat
from participant_item import ParticipantItem

# python modules
import MySQLdb
import urllib
import json

class Match(object):
    def __init__(self, match_id, version, duration, region, participants, banned_champs):
        self.match_id = match_id
        self.version = str(version)
        self.duration = duration
        self.region = str(region)
        self.participants = participants
        self.banned_champs = banned_champs

    def __str__(self):
        return "match_id: " + str(self.match_id) + "\nversion: " + str(self.version) + "\nduration: " + str(self.duration) + "\nregion: " + str(self.region) + "\nparticipants: " + str(self.participants)

    def save(self):
        """
        Saves this Match to the database.
        """
        
        # Get new database instance
        db = credentials.getDatabase()

        cur = db.cursor()
        query = '''INSERT IGNORE INTO game_match (id, version, duration, region)
                VALUES(%s, %s, %s, %s);'''

        data = (self.match_id, self.version, self.duration, self.region)
        cur.execute(query, data)

        # commit query
        db.commit()
        db.close()

        for champ_id in self.banned_champs:
            self.save_banned_champ(champ_id)

        return True

    def save_banned_champ(self, champ_id):
        """
        Saves a champ_id to the database as a banned champion.
        """
        
        # Get new database instance
        db = credentials.getDatabase()

        cur = db.cursor()
        query = '''INSERT IGNORE INTO banned_champion (match_id, champion_id)
                VALUES(%s, %s);'''

        data = (self.match_id, champ_id)
        cur.execute(query, data)

        # commit query
        db.commit()
        db.close()

        return True


def load(match_id):
    '''
    Args:
        match_id: The id of the match
    Returns:
        A Match object
    '''
    # Get new database instance
    db = credentials.getDatabase()

    cur = db.cursor()
    query = '''SELECT * FROM match WHERE id = %s;'''
    cur.execute(query, match_id)

    m = ""
    for tup in cur:
        m = Match(tup[0], tup[1], tup[2], tup[3])

    # commit query
    db.commit()
    db.close()
    return m

def fetch_match(match_id, region):
    '''
    Args:
        match_id: The id of the match to fetch
        region: The region of the match
    Returns:
        A Match object, from Riot Games API.
    '''

    creds = credentials.getCredentials()
    url = 'https://na.api.pvp.net/api/lol/' + region + '/v2.2/match/' + str(match_id) + '?api_key=' + str(creds.api_key)
    print("Requesting url: " + str(url))

    response = urllib.urlopen(url);
    data = json.loads(response.read())

    for key in data:
        if key == 'matchVersion':
            version = data[key]

        elif key == 'matchDuration':
            duration = data[key]

        elif key == 'teams':
            teams = data[key]

            banned_champs = []

            for t in teams:
                bans = t['bans']

                for b in bans:
                    champion_id = b['championId']
                    banned_champs.append(champion_id)

        elif key == 'participants':
            participants = data[key]

            list_participants = []

            # for each participant
            for p in participants:
                #print(p)

                for key in p:

                    if key == 'participantId':
                        participant_id = p[key]

                    elif key == 'championId':
                        champion_id = p[key]

                    elif key == 'teamId':
                        team_id = p[key]

                    elif key == 'timeline':
                        lane = p[key]['lane']

                    elif key == 'stats':
                        stats = p[key]

                        # item info
                        item0 = stats['item0']
                        item1 = stats['item1']
                        item2 = stats['item2']
                        item3 = stats['item3']
                        item4 = stats['item4']
                        item5 = stats['item5']
                        item6 = stats['item6']

                        kills = stats['kills']
                        deaths = stats['deaths']
                        assists = stats['assists']

                        magic_damage = stats['magicDamageDealt']
                        magic_damage_champs = stats['magicDamageDealtToChampions']
                        magic_damage_taken = stats['magicDamageTaken']

                        champ_level = stats['champLevel']
                        gold_earned = stats['goldEarned']
                        win = stats['winner']

                # construct items of participant
                items = ParticipantItem(match_id, participant_id, item0, item1, item2, item3, item4, item5, item6, win)

                # construct stats of participant
                stat = ParticipantStat(match_id, participant_id)
                stat.__setKDA__(kills, deaths, assists)
                stat.__setDamage__(magic_damage, magic_damage_champs, magic_damage_taken)
                stat.__setOther__(champ_level, gold_earned, win)

                # construct participant object
                participant = Participant(match_id, participant_id, champion_id, team_id, win, lane, items, stat)

                list_participants.append(participant)

    return Match(match_id, version, duration, region, list_participants, banned_champs)

# match = fetch_match(1852538938, 'na')

# # save the match to db
# match.save()

# # save the participants
# for p in match.participants:
#     p.save()


