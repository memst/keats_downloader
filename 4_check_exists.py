import os
import sqlite3

import kd_utilities

MAX_NAME_LENGTH = 40

def check_exists(database):
	database.execute("UPDATE Videos SET file_exists = 0")

	for video in database.execute("SELECT * FROM Videos WHERE videoUrl IS NOT NULL"):
	    dirs = []
	    for i in range(4):
	        dirs.append((video[i][0:MAX_NAME_LENGTH]).strip())

	    directory = "library/{}/{}".format(dirs[0],dirs[2])
	    path = "{}/{}.mp4".format(directory,dirs[3])
	    if os.path.isfile(path):
	        database.execute("UPDATE Videos SET file_exists = 1 WHERE pageUrl = ?", (video[4],))

if __name__ == "__main__":
    database = kd_utilities.open_database()

    check_exists(database)

    database.commit()