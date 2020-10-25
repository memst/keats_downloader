import sqlite3
import os
import ffmpeg
import requests
#library/couse/week/name.mp4
path_base="library/{}/{}/{}.mp4"

database = sqlite3.connect('example.db')
VIDEO = ***REMOVED***
for video in database.execute("SELECT * FROM Videos WHERE pageUrl=?",(VIDEO,)):
	path = "online_library/{}/{}/{}.mp4".format(video[0],video[2],video[3])
	srt_path = "online_library/{}/{}/{}.srt".format(video[0],video[2],video[3])
	#skip if exists
	if os.path.isfile(path):
		continue

	#no url
	if (video[4] is None):
		continue

	#download
	try:
		os.mkdir("online_library")
		os.mkdir("online_library/{}".format(video[0]))
		os.mkdir("online_library/{}/{}".format(video[0],video[2]))
	except:
		pass
	wget
	if (video[6] is not None):
		r = requests.get(video[6])
		open(srt_path, "wb").write(r.content)
