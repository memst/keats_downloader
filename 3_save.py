import sqlite3
import os
from pathlib import Path
import requests
import ffmpeg

ONLINE = False
MAX_NAME_LENGTH = 40
database = sqlite3.connect('example.db')

def save(online=True):
	base_folder = None
	extension = None
	if online:
		base_folder="online_library"
		extension="m3u8"
	else:
		base_folder="library"
		extension="mp4"

	#Get all videos with valid urls
	for video in database.execute("SELECT * FROM Videos WHERE videoUrl IS NOT NULL"):
		dirs = []
		for i in range(4):
			dirs.append(video[i].strip()[0:MAX_NAME_LENGTH])

		directory = "{}/{}/{}".format(base_folder,dirs[0],dirs[2])
		path = "{}/{}.{}".format(directory,dirs[3],extension)
		srt_path = "{}/{}.srt".format(directory,dirs[3])

		#skip if exists
		if os.path.isfile(path):
			continue
		print(video[1],video[2],video[3])
		#download
		Path(directory).mkdir(parents=True, exist_ok=True)

		if online:
			r = requests.get(video[5])
			open(path, "wb").write(r.content)
		else:
			ffmpeg.input(video[5]).output(path,codec="copy").run()

		if (video[6] is not None):
			r = requests.get(video[6])
			open(srt_path, "wb").write(r.content)

save(online=ONLINE)
