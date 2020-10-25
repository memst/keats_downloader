import sqlite3
import os
import ffmpeg
import requests
#library/couse/week/name.mp4

database = sqlite3.connect('example.db')

for video in database.execute("SELECT * FROM Videos WHERE videoUrl IS NOT NULL"):
	path = "library/{}/{}/{}.mp4".format(video[0],video[2],video[3])
	srt_path = "library/{}/{}/{}.srt".format(video[0],video[2],video[3])
	#skip if exists
	if os.path.isfile(path):
		continue

	#no url
	if (video[4] is None):
		continue

	#download
	try:
		os.mkdir("library")
	except:
		pass
	try:
		os.mkdir("library/{}".format(video[0]))
	except:
		pass
	try:
		os.mkdir("library/{}/{}".format(video[0],video[2]))
	except:
		pass
	ffmpeg.input(video[5]).output(path).run()
	if (video[6] is not None):
		r = requests.get(video[6])
		open(srt_path, "wb").write(r.content)
