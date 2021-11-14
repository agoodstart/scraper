import sys

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

def get_city_name():
    c = sys.argv[1:]

    if len(c) < 1:
        raise Exception("no arguments passed")

    if len(c) == 1:
        return c[0]
    else:
        return '-'.join(str(s) for s in c)

def get_chrome_driver():
    chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)

    # Use this to bypass recaptcha
    chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    serv = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=serv, options=chrome_options)

if __name__ == "__main__":
    cn = get_city_name()
    d = get_chrome_driver()

    d.get(f'https://www.funda.nl/koop/{cn}')

    i = 0
    linklist = []

    for a in d.find_elements(By.CSS_SELECTOR, 'div.search-content-output ol.search-results div.search-result__header-title-col a:first-child'):
        if i == 10:
            break

        l = a.get_attribute('href')

        linklist.append(l)
        i += 1

    for a in linklist:
        d.get(a)
        try:
            data=WebDriverWait(d, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.object-kenmerken-body dl.object-kenmerken-list dt')))
            for d in data:
                ih = d.get_attribute('innerHTML')
                print(ih)
        except:
            print('Element not found')
            continue
    
    d.close()

    