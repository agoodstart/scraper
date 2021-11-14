import sys
import json

# Importing selenium drivers
from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException, NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#Webdriver manager saves the chromedriver in cache so you don't have to download it manually
from webdriver_manager.chrome import ChromeDriverManager

# reads out arguments as city names if there is a space in the name(like "den haag") it will join the string with hyphen 
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

    #makes sure it is possible to run headless
    chrome_options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')

    serv = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=serv, options=chrome_options)

# checks if city name is present, page will return "/zoeksuggestie otherwise"
def check_city_name(cd, cn):
    # gets the city based on 
    cd.get(f'https://www.funda.nl/koop/{cn}/')

    try:
        WebDriverWait(cd, 5).until(EC.presence_of_element_located((By.ID, 'content')))
    except TimeoutException:
        print("page timed out")
    
    if "zoeksuggestie" in cd.current_url:
        sys.exit("City name not found")

# due to recaptcha, there is no easy fix to bypass recaptcha. Instead, get all the urls, and store them in a list
def get_house_links(cd, i = 0, urllist = []):
    for a in cd.find_elements(By.CSS_SELECTOR, 'div.search-content-output ol.search-results div.search-result__header-title-col a:first-child'):
        if i == 10:
            break

        l = a.get_attribute('href')

        urllist.append(l)
        i += 1
    
    return urllist

# navigation will trigger recaptcha. instead, reload with each url in the urllist
def get_house_infos(cd, urllist, houselist = []):
    for a in urllist:
        house = {
            'link': a,
        }
        cd.get(a)
        try:
            WebDriverWait(cd, 5).until(EC.presence_of_element_located((By.ID, 'content')))
            data=cd.find_element(By.XPATH, '//dt[contains(text(),"Ligging tuin")]/following-sibling::dd/span')

            ih = data.get_attribute('innerHTML')
            house['Ligging tuin'] = ih
            print(ih)
        except NoSuchElementException:
            house['Ligging tuin'] = 'Optie niet beschikbaar'
        except TimeoutException:
            print("page timed out")
            house['Ligging tuin'] = 'Geen informatie gevonden'
        except:
            house['Ligging tuin'] = ''
        houselist.append(house)

    return houselist

if __name__ == "__main__":
    cn = get_city_name()
    cd = get_chrome_driver()

    check_city_name(cd, cn)

    urllist = get_house_links(cd)

    houselist = get_house_infos(cd, urllist)
    cd.close()

    # print the results to a json file
    with open('houses.json', 'w') as f:
        json.dump(houselist, f, sort_keys=True, indent=4)