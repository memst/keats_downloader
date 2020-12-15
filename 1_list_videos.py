import os
import sqlite3

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver

import kd_utilities


def list_videos(coruses, database, driver):
    wait_element = EC.presence_of_element_located((By.ID, 'page-footer'))
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




if __name__ == "__main__":
    with open("courses.txt", "r") as f:
        courses = [line.strip() for line in f.readlines()]

    database = kd_utilities.open_database()
    driver = kd_utilities.init_driver()

    list_videos(courses, database, driver)

    database.commit()
    driver.quit()