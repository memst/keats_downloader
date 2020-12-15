import os
import sqlite3

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver

with open("courses.txt", "r") as f:
    courses = [line.strip() for line in f.readlines()]

database = sqlite3.connect('example.db')

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--user-data-dir=" + os.getcwd() + "/selenium/chrome_driver")
options.add_argument("--disable-web-security")
driver = webdriver.Chrome(executable_path="selenium/chromedriver.exe", options=options)

driver.get("https://keats.kcl.ac.uk/")
wait_element = EC.presence_of_element_located((By.ID, 'page-footer'))
WebDriverWait(driver, 10).until(wait_element)

for course in courses:
    driver.get(course)
    print(course)
    WebDriverWait(driver, 10).until(wait_element)
    videoDicts = driver.execute_script(open("list_videos.js").read())
    videos = []

    videoIndex = 1
    weekOfPreviousVideo = ""
    for video in videoDicts:
    	if (video['week'] != weekOfPreviousVideo):
    		videoIndex = 1
    		weekOfPreviousVideo = video['week']
    	video['name'] = "{:02}_{}".format(videoIndex, video['name'])
    	videos.append((video['course'], video['courseID'], video['week'], video['name'], video['pageUrl']))
    	videoIndex += 1

    database.executemany(
        "INSERT INTO Videos (course, courseID, week, name, pageUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(pageUrl) DO UPDATE SET courseID=courseID",
        videos)

database.commit()
driver.quit()
