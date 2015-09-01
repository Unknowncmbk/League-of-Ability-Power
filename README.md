## Introduction to Two Shot
Two Shot compares statistical data from League of Legends over two different patches in order to see trends of play styles from one patch to another. In specific, we're interested in looking at the Ability Power Itemization changes that modified the game from patch 5.11 to 5.14. In this project, we will aggregate win rates/use rates of items from both patches and analyze the ban rates of specific champions in order to see who benefitted the most from the AP Itemization changes.

## Background
This project was a submission in Riot Games API challenge 2.0. More information on Riot's API challenge and past winners can be found [here](https://developer.riotgames.com/docs/api-challenge).

## Requirements
This program was written and tested on MacOS 10.9.5, and further tested on CentOS 6.6.
- [MySQL](http://dev.mysql.com/doc/mysql-repo-excerpt/5.6/en/linux-installation-yum-repo.html)
- [Python](https://www.digitalocean.com/community/tutorials/how-to-set-up-python-2-7-6-and-3-3-3-on-centos-6-4) with MySQL module.
- [Flask](http://flask.pocoo.org/docs/0.10/installation/)

This software also assumes you already have installed and setup MySQL with a database, installed and ran Flask, and install Python with the MySQL-Python extension from pip. (pip install Python-MySQL).

## Instructions
To populate match data, if you don't have any:
- Transfer the repository contents to a location in which you want to run the program's set up.
- Edit credentials.txt with MySQL database connection details and your API key from Riot Games.
- Copy/paste queries from ./backend/schema/database-schema.txt into MySQL in order to populate tables.
- Edit timer.py REQUESTS_PER_INTERVAL field to include how many max requests you want to send to Riot.
- Run champion.py's fetch_all_champions() to populate champion records (Thresh, Akali, etc) and run item.py's fetch_all_items() to grab info on each item.
- Optional: You can uncomment the counter in the method read_data() to limit how many matches you want to pull. For example, if you're interested in only generating 5 matches from each file.

## Snapshots
TBA

## Improvements
TBA

## Disclaimer
This project or its contributors are no way affilated with Riot Games.

## License
A copy of the TwoShot's license can be found [here](https://github.com/Unknowncmbk/Two-Shot/blob/master/LICENSE).
