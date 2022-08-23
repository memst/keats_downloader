import time
import sqlite3
import os
from pathlib import Path
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from . import utilities
from . import FFhandler

def list_videos(courses, database, driver):
    wait_element = EC.presence_of_element_located((By.ID, 'page-footer'))
    for course in courses:
        driver.get(course)
        print(course)
        WebDriverWait(driver, 10).until(wait_element)
        video_dicts = driver.execute_script(open("downloader/ListVideos.js").read())
        videos = []

        video_index = 1
        week_of_previous_video = ""
        for video in video_dicts:
            if (video['week'] != week_of_previous_video):
                video_index = 1
                week_of_previous_video = video['week']
            videos.append((video['course_name'], video['course_id'], video['week'], video_index, video['video_name'], video['page_url']))
            video_index += 1

        database.executemany(
            "INSERT INTO videos (course_name, course_id, week, video_in_week, video_name, page_url) VALUES (?, ?, ?, ?, ?, ?) ON CONFLICT(page_url) DO UPDATE SET video_in_week=excluded.video_in_week",
            videos)

def get_video_urls(database, driver):
    for video in database.execute("SELECT course_id, week, video_name, page_url FROM videos WHERE (file_exists = 0 OR file_exists IS NULL)"):
        print(video[0],video[1],video[2])
        driver.get(video[3])

        #Wait and open contentFrame
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'contentframe')))
        except:
            #The only known case of failure is when a video has been removed
            print("Failed to find frame")
            continue
        driver.switch_to.frame(driver.find_element(By.ID,'contentframe'))

        #Make sure that the player is loaded
        driver.execute_script(open("downloader/CreatePlayer.js").read())
        #Process player
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'kplayer')))
        except:
            #Despite the create_player script the player still wasn't found
            print("Failed to load player")
            continue

        driver.switch_to.frame(driver.find_element(By.ID,'kplayer_ifp'))

        #Get video/srt URL
        urls = driver.execute_script(open("downloader/VideoUrl.js").read())
        #print(urls)
        if (urls[0] is None):
            print("Failed to find video url")
            continue

        if(urls[1] is not None):
            print("Fount srt")
        database.execute("UPDATE videos SET video_url=?, srt_url=? WHERE page_url=?",(urls[0],urls[1],video[3]))
        database.commit()

def download_videos(database, online=False, embed_subtitles=False, ffmpeg_verbosity="error"):
    #Get all videos with valid urls
    for course_id, week, video_name, page_url, video_url, srt_url in database.execute("SELECT course_id, week, video_name, page_url, video_url, srt_url FROM videos WHERE video_url IS NOT NULL"):
        paths = utilities.get_paths(page_url, database, online=online)

        #skip if exists
        if os.path.isfile(paths['file_path']):
            continue

        #download
        Path(paths['directory']).mkdir(parents=True, exist_ok=True)

        print(f"Downloading {course_id} {week} {video_name}...")
        #print(f"Launching ffmpeg\nPage URL: {page_url}\nVideo URL: {video_url}\npaths: {paths}\n")
        if online:
            r = requests.get(video_url)
            open(paths['file_path'], "wb").write(r.content)
        elif (embed_subtitles and srt_url is not None):
            FFhandler.execute(['-i', video_url, '-i', srt_url, '-c', 'copy', 
                '-c:s', 'mov_text', '-metadata:s:s:0', 'language=eng', '-disposition:s:s:0', 
                'default', paths['file_path']], name=f"Downloading {course_id} {week} {video_name}")
        else:
            FFhandler.execute(['-i', video_url, '-c', 'copy', paths['file_path']], name=f"Downloading {course_id} {week} {video_name}")

        if ((not embed_subtitles or online) and (srt_url is not None)):
            r = requests.get(srt_url)
            open(paths['srt_path'], "wb").write(r.content)

def check_exists(database):
    database.execute("UPDATE videos SET file_exists = 0")

    for (page_url,) in database.execute("SELECT page_url FROM videos WHERE video_url IS NOT NULL"):
        paths = utilities.get_paths(page_url, database, online=False)

        if os.path.isfile(paths['file_path']):
            database.execute("UPDATE videos SET file_exists = 1 WHERE page_url = ?", (page_url,))