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
print("done")

for video in database.execute("SELECT * FROM Videos WHERE (file_exists = 0 OR file_exists IS NULL)"):
	try:
		print(video[1],video[2],video[3])
		driver.get(video[4])
		
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'contentframe')))
		driver.switch_to.frame(driver.find_element_by_id('contentframe'))
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'kplayer_ifp')))
		driver.switch_to.default_content()
		sleep(1)
	except:
		print("Failed to find frame")
		continue
	#still using JS for some reason. Could quite easily change this to be pure selenium, but me lazy.
	urls = driver.execute_script(open("video_url.js").read())
	#print(urls)
	if(urls[1] is not None):
		print("Fount srt")
	database.execute("UPDATE Videos SET videoUrl=?, srtUrl=? WHERE pageUrl=?",(urls[0],urls[1],video[4]))
	database.commit()
	

database.commit()
driver.close()