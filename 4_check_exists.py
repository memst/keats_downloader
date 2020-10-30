import os
import sqlite3

MAX_NAME_LENGTH = 40

database = sqlite3.connect('example.db')

database.execute("UPDATE Videos SET file_exists = 0")

for video in database.execute("SELECT * FROM Videos WHERE videoUrl IS NOT NULL"):
	dirs = []
	for i in range(4):
		dirs.append(video[i].strip()[0:MAX_NAME_LENGTH])

	directory = "library/{}/{}".format(dirs[0],dirs[2])
	path = "{}/{}.mp4".format(directory,dirs[3])
	if os.path.isfile(path):
		database.execute("UPDATE Videos SET file_exists = 1 WHERE pageUrl = ?", (video[4],))

database.commit()