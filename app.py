from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json


DRIVER_PATH = './chromedriver'
BASE_URL = 'https://loltracker.com/'

driver = webdriver.Chrome(DRIVER_PATH)
driver.get(BASE_URL)

# driver.maximize_window()

articles = driver.find_element(By.CLASS_NAME, 'view-all-blogs')
articles.find_element(By.TAG_NAME, 'a').click()

selections = driver.find_elements(By.CLASS_NAME, 'eb-post-listing__item')
data = {}
cpt = 0

for element in selections:
    data_temp = {}
    try:
        data_temp['title'] = element.text.split('\n')[0]
    except:
        data_temp['title'] = None
    try:
        data_temp['date'] = element.text.split('\n')[1]
    except:
        data_temp['date'] = None
    try:
        data_temp['author'] = element.text.split('\n')[2]
    except:
        data_temp['author'] = None
    try:
        data_temp['desc'] = element.text.split('\n')[3]
    except:
        data_temp['desc'] = None
    try:
        data_temp['keys'] = '-'.join(element.text.split('\n')[5:])
    except:
        data_temp['keys'] = None
    try:
        data_temp['img'] = element.find_element(
            By.CLASS_NAME, 'eb-post-thumb.is-left').find_element(By.TAG_NAME, 'img').get_attribute('src')
    except:
        data_temp['img']

    data[cpt] = data_temp
    cpt += 1

with open("loltracker.json", "wb") as f:
    f.write(str(data).encode("UTF-8"))

driver.close()
