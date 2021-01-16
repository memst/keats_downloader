import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from downloader import utilities
from downloader import settings
from downloader import scripts

def login():
	options = webdriver.ChromeOptions()
	options.add_argument("user-data-dir=selenium/chrome_driver")
	driver = webdriver.Chrome(executable_path="selenium/chromedriver.exe", chrome_options=options)

	driver.get("https://keats.kcl.ac.uk/")

	WebDriverWait(driver, 9999).until(EC.url_matches("https://keats.kcl.ac.uk/"))

	driver.quit()

if not os.path.isfile(settings.settings['database_file']):
	utilities.create_database(settings.settings['database_file'])

if not settings.settings['logged_in']:
	login()

driver = utilities.init_driver()
database = utilities.open_database(settings.settings['database_file'])

with open("courses.txt", "r") as f:
    courses = [line.strip() for line in f.readlines()]

try:
	scripts.list_videos(courses, database, driver)
	scripts.check_exists(database)
	scripts.get_video_urls(database, driver)
finally:
	driver.quit()

scripts.download_videos(database)
scripts.check_exists(database)
