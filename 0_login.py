from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=selenium/chrome_driver")
driver = webdriver.Chrome(executable_path="selenium/chromedriver.exe", chrome_options=options)

driver.get("https://keats.kcl.ac.uk/")