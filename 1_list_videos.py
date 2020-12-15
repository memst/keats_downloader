import os
import sqlite3

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver

with open("courses.txt", "r") as f:
    courses = [line.strip() for line in f.readlines()]

database = sqlite3.connect('example.db')

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("--user-data-dir=" + os.getcwd() + "/selenium/chrome_driver.exe")
options.add_argument("--disable-web-security")
driver = webdriver.Chrome(executable_path="selenium/chromedriver", options=options)

driver.get("https://keats.kcl.ac.uk/")
wait_element = ec.presence_of_element_located((By.ID, 'page-footer'))
WebDriverWait(driver, 10).until(wait_element)

for course in courses:
    driver.get(course)
    print(course)
    WebDriverWait(driver, 10).until(wait_element)
    videoDicts = driver.execute_script(open("list_videos.js").read())
    videos = []

    index = 1
    for i in range(len(videoDicts) - 1):
        videoDicts[i]['name'] = str(index) + "_" + videoDicts[i]['name']

        index = index + 1 if videoDicts[i]['week'] == videoDicts[i+1]['week'] else 1

        videos.append((videoDicts[i]['course'], videoDicts[i]['courseID'], videoDicts[i]['week'], videoDicts[i]['name'],
                       videoDicts[i]['pageUrl']))

    database.executemany(
        "INSERT INTO Videos (course, courseID, week, name, pageUrl) VALUES (?, ?, ?, ?, ?) ON CONFLICT(pageUrl) DO UPDATE SET courseID=courseID",
        videos)

database.commit()
driver.close()
