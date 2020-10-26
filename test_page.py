import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=selenium/chrome_driver")
options.add_argument("disable-web-security")
driver = webdriver.Chrome(executable_path="selenium/chromedriver.exe", chrome_options=options)


driver.get(***REMOVED***)
sleep(10)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'contentframe')))
driver.switch_to.frame(driver.find_element_by_id('contentframe'))
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'kplayer_ifp')))
driver.switch_to.frame(driver.find_element_by_id('kplayer_ifp'))

videoTag = driver.find_element_by_css_selector(".persistentNativePlayer.nativeEmbedPlayerPid")

video_url = videoTag.get_attribute("src")



driver.switch_to.default_content()
element = driver.execute_script(open("video_url.js").read())
sleep(1000)