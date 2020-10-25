import sqlite3
import os
import requests

database = sqlite3.connect('example.db')

for video in database.execute("SELECT * FROM Videos WHERE videoUrl IS NOT NULL"):
	path = "online_library/{}/{}/{}.m3u8".format(video[0],video[2],video[3])
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
	except:
		pass
	try:
		os.mkdir("online_library/{}".format(video[0]))
	except:
		pass
	try:
		os.mkdir("online_library/{}/{}".format(video[0],video[2]))
	except:
		pass
	r = requests.get(video[5])
	open(path, "wb").write(r.content)
	if (video[6] is not None):
		r = requests.get(video[6])
		open(srt_path, "wb").write(r.content)
