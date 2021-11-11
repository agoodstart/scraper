# Importing modules
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def get_chrome_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    serv = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=serv, options=chrome_options)

chrome_driver = get_chrome_driver()
chrome_driver.get("https://www.funda.nl/koop/amsterdam/")
# driver.get('https://www.funda.nl/')