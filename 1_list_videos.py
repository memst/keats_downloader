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
        video_dicts = driver.execute_script(open("ListVideos.js").read())
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




if __name__ == "__main__":
    with open("courses.txt", "r") as f:
        courses = [line.strip() for line in f.readlines()]

    database = kd_utilities.open_database()
    driver = kd_utilities.init_driver()

    list_videos(courses, database, driver)

    database.commit()
    driver.quit()