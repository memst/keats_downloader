import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

database = sqlite3.connect('example.db')

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=selenium/chrome_driver")
options.add_argument("disable-web-security")
driver = webdriver.Chrome(executable_path="selenium/chromedriver.exe", chrome_options=options)

driver.get("https://keats.kcl.ac.uk/")
wait_element = EC.presence_of_element_located((By.ID, 'page-footer'))
WebDriverWait(driver, 10).until(wait_element)

for video in database.execute("SELECT * FROM Videos WHERE (file_exists = 0 OR file_exists IS NULL)"):
    print(video[1],video[2],video[3])
    driver.get(video[4])

    #Wait and open contentFrame
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'contentframe')))
    except:
        #The only known case of failure is when a video has been removed
        print("Failed to find frame")
        continue
    driver.switch_to.frame(driver.find_element_by_id('contentframe'))

    #Make sure that the player is loaded
    driver.execute_script(open("create_player.js").read())
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

    urls = driver.execute_script(open("video_url.js").read())
    #print(urls)
    if (urls[0] is None):
        print("Failed to find video url")
        continue

    if(urls[1] is not None):
        print("Fount srt")
    database.execute("UPDATE Videos SET videoUrl=?, srtUrl=? WHERE pageUrl=?",(urls[0],urls[1],video[4]))
    database.commit()
    

database.commit()
driver.quit()