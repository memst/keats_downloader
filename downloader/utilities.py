import os

import sqlite3

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver

MAX_NAME_LENGTH = 40

def init_driver():
    options = webdriver.ChromeOptions()
    options.headless = False
    options.add_argument("--user-data-dir=" + os.getcwd() + "/selenium/chrome_driver")
    options.add_argument("--disable-web-security")
    driver = webdriver.Chrome(executable_path="selenium/chromedriver.exe", options=options)

    driver.get("https://keats.kcl.ac.uk/")
    wait_element = EC.presence_of_element_located((By.ID, 'page-footer'))
    WebDriverWait(driver, 10).until(wait_element)

    return driver

def open_database(filename):
    return sqlite3.connect(filename)

def create_database(filename):
    statement = "CREATE TABLE \"videos\" ( `course_name` TEXT NOT NULL, `course_id` TEXT NOT NULL, `week` TEXT NOT NULL, 'video_in_week' INTEGER DEFAULT NULL, `video_name` TEXT NOT NULL, `page_url` TEXT NOT NULL UNIQUE, `video_url` TEXT, `srt_url` TEXT, `file_exists` INTEGER DEFAULT 0, PRIMARY KEY(`page_url`) )"

    database = sqlite3.connect(filename)
    database.execute(statement)
    database.commit()


def get_paths(page_url, database, online=False):
    base_folder = None
    extension = None
    if online:
        base_folder="online_library"
        extension="m3u8"
    else:
        base_folder="library"
        extension="mp4"

    course_id, week, video_in_week, video_name = database.execute("SELECT course_id, week, video_in_week, video_name FROM videos WHERE page_url = ?", (page_url,)).fetchone()

    directory = "{}/{}/{}".format(base_folder, course_id, week)
    file_name = "{:02}_{}.{}".format(video_in_week, video_name[0:MAX_NAME_LENGTH], extension)
    file_directory = "{}/{}".format(directory, file_name)
    srt_name = "{:02}_{}.srt".format(video_in_week, video_name[0:MAX_NAME_LENGTH])
    srt_path = "{}/{}".format(directory, srt_name)

    return {
        'directory': directory,
        'file_name': file_name,
        'file_path': file_directory,
        'srt_name': srt_name,
        'srt_path': srt_path
    }
