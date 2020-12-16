import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

import kd_utilities

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
        driver.switch_to.frame(driver.find_element_by_id('contentframe'))

        #Make sure that the player is loaded
        driver.execute_script(open("CreatePlayer.js").read())
        #Process player
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'kplayer_ifp')))
        except:
            #Despite the create_player script the player still wasn't found
            print("Failed to load player")
            continue

        driver.switch_to.frame(driver.find_element_by_id('kplayer_ifp'))
        
        #Artificial wait for the contents of kplayer_ifp
        sleep(1)

        #May cause an exception
        urls = driver.execute_script(open("VideoUrl.js").read())
        #print(urls)
        if (urls[0] is None):
            print("Failed to find video url")
            continue

        if(urls[1] is not None):
            print("Fount srt")
        database.execute("UPDATE videos SET video_url=?, srt_url=? WHERE page_url=?",(urls[0],urls[1],video[3]))
        database.commit()
    

if __name__ == "__main__":
    database = kd_utilities.open_database()
    driver = kd_utilities.init_driver()

    get_video_urls(database, driver)

    database.commit()
    driver.quit()
