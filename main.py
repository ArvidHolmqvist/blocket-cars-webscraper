from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import pandas as pd

import random


df = pd.DataFrame(columns=['cost', 'fuel', 'gear', 'range', 'year', 'type', 'wheels', 'hp', 'color', 'URL'])
pd.set_option('display.max_columns', None)

DRIVER_PATH = r'C:\Program Files\Chromedriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)

driver.get('https://www.blocket.se/annonser/hela_sverige/fordon/bilar?cb=3&ccca=1&ccce=1&ccco=1&cchb=1&ccmp=1&ccsc=1&ccsd=1&ccsu=1&cg=1020&f=p&page=1&pl=0&sort=date')
driver.find_element_by_id("accept-ufti").click()

for i in range(0,40):
    page = random.randint(1, 50)

    driver.get('https://www.blocket.se/annonser/hela_sverige/fordon/bilar?cb=3&ccca=1&ccce=1&ccco=1&cchb=1&ccmp=1&ccsc=1&ccsd=1&ccsu=1&cg=1020&f=p&page={}&pl=0&sort=date'.format(page))

    delay = 2 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.enigRj')))
    except TimeoutException:
        print ("Loading took too much time!")
        exit()

    a = driver.find_elements_by_css_selector('.itHtzm')

    url = 'https://www.blocket.se' + a[random.randint(0, 39)].get_attribute('to')

    print(i)

    driver.get(url)

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.gWITvi')))
    except TimeoutException:
        print ("Loading took too much time!")
        exit()


    a = driver.find_element_by_css_selector('.EkzGO').text
    b = driver.find_elements_by_css_selector('.eZCCwh')

    a = a.replace(" ", "")
    a = a.replace("kr", "")

    try:
        carRange = b[2].text.split('-')[1]
    except IndexError:
        carRange = b[2].text
    carRange = carRange.replace(" ", "")

    try:
        hp = b[6].text.split()[0]
    except IndexError:
        hp = b[6].text

    df.loc[i] = [a] + [b[0].text] + [b[1].text] + [carRange] + [b[3].text] + [b[4].text] + [b[5].text] + [hp] + [b[7].text] + [url]

print(df)
df.to_excel(r'data.xlsx', index = False, header=True)