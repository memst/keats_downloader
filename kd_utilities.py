import os

import sqlite3

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver

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

def open_database():
	return sqlite3.connect('example.db')