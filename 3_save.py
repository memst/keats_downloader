import sqlite3
import os
from pathlib import Path
import requests
import ffmpeg

import kd_utilities

ONLINE = False

def download_videos(database, online=False):
    #Get all videos with valid urls
    for page_url, video_url, srt_url in database.execute("SELECT page_url, video_url, srt_url FROM videos WHERE video_url IS NOT NULL"):
        paths = kd_utilities.get_paths(page_url, database, online=online)

        #skip if exists
        if os.path.isfile(paths['file_path']):
            continue

        #download
        Path(paths['directory']).mkdir(parents=True, exist_ok=True)

        if online:
            r = requests.get(video_url)
            open(paths['file_path'], "wb").write(r.content)
        else:
            ffmpeg.input(video_url).output(paths['file_path'],codec="copy").run()

        if (srt_url is not None):
            r = requests.get(srt_url)
            open(paths['srt_path'], "wb").write(r.content)



if __name__ == "__main__":
    database = kd_utilities.open_database()

    download_videos(database, online=ONLINE)