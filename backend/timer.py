#!/usr/bin/python

import json
import os

# local imports
import match

# python modules
import json
import os
import time
from threading import Thread

class RepeatingTask(Thread):
    def __init__(self, interval, data):
        self.stopped = False
        self.interval = interval
        self.data = data
        Thread.__init__(self)

    def run(self):
        while not self.stopped and len(self.data) > 0:
            self.onInterval()
            time.sleep(self.interval)

    def onInterval(self):

        try:
            # pop the next tuple
            tup = self.data.pop()
            if tup is not None:
                region = tup[0].lower()
                match_id = tup[1]

                # print message
                print("Requesting region " + str(region) + " for match " + str(match_id))

                m = match.fetch_match(match_id, region)
                # save the match to db
                m.save()

                # save the participants
                for p in m.participants:
                    p.save()
        except Exception as e:
            print(e)


def read_data():
	"""
	Returns: A set of tuples (region, match_id) in which we should read from Riot.
	"""

	matches = []

	# walk the directory
	for root, dirs, files in os.walk("./AP_ITEM_DATASET/"):

		# for each file
		for f in files:

			# if data file and ranked_solo match
			if f.endswith(".json") and "RANKED_SOLO" in str(root):

				# read file
				file_name = str(root) + "/" + str(f)
				json_data = open(file_name).read()
				data = json.loads(json_data)

				# for each match in this file
				for match_id in data:

					# isolate region
					parts = f.split(".")

					# tuple of (region_name, match_id)
					tup = (parts[0], match_id)

					# add to total matches we have to find
					matches.append(tup)

	return matches

matches = read_data()
if matches is not None:
	if len(matches) > 0:

		# Schedule a repeating task to handle off thread instructions
		task = RepeatingTask(2, matches)
		task.start()