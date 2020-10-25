import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=selenium/chrome_driver")
options.add_argument("disable-web-security")
driver = webdriver.Chrome(executable_path="selenium/chromedriver.exe", chrome_options=options)

driver.get("https://google.com")
r = driver.execute_script("return null;")
print(r)