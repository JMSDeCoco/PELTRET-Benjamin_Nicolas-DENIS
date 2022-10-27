from pickle import TRUE
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
import json
from utiles import DataBase
import sqlalchemy as db
import pandas as pd

DRIVER_PATH = './chromedriver'
BASE_URL = 'https://loltracker.com/'

# creation de la database
driver = webdriver.Chrome(DRIVER_PATH)
base = DataBase('LeagueTrack')

try:
    base.truncate_table('Tracker')
except:
    pass

try:
    # creation de la table
    base.create_table('Tracker', tracker_id=db.String, tracker_title=db.String, tracker_date=db.String,
                      tracker_author=db.String, tracker_content=db.String, tracker_cat=db.String, tracker_img=db.String)
except:
    print(False)


def collect_data(page: int):
    # connection a la page
    driver.get(BASE_URL)
    # deplacement sur la page
    articles = driver.find_element(By.CLASS_NAME, 'view-all-blogs')
    articles.find_element(By.TAG_NAME, 'a').click()
    driver.maximize_window()
    newUrl = driver.current_url
    data = []
    list_url = [newUrl + f'?start={n*50}' for n in range(page)]
    for url in list_url:
        driver.get(url)
        # get element de la page
        selections = driver.find_elements(
            By.CLASS_NAME, 'eb-post-listing__item')
        # get les elements de la page pour les stocker dans un json
        for element in selections:
            id_select = element.get_attribute('data-id')

            data_temp = {}
            try:
                data_temp['id'] = id_select
            except:
                data_temp['id'] = None

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
                data_temp['img'] = None

            data.append(data_temp)
            # Ajout dans la bdd
            if len(pd.DataFrame(base.select_table('Tracker')).columns) == 0:
                base.add_row('Tracker', tracker_id=str(id_select), tracker_title=data_temp['title'], tracker_date=data_temp['date'], tracker_author=data_temp[
                             'author'], tracker_content=data_temp['desc'], tracker_cat=data_temp['keys'], tracker_img=data_temp['img'])
            else:
                base.add_row('Tracker', tracker_id=str(id_select), tracker_title=data_temp['title'], tracker_date=data_temp['date'], tracker_author=data_temp[
                             'author'], tracker_content=data_temp['desc'], tracker_cat=data_temp['keys'], tracker_img=data_temp['img'])
    return data


def createJson(n):
    # creation du JSON
    with open("loltracker.json", "wb") as f:
        f.write(str(collect_data(n)).encode("UTF-8"))


# permets de lancer le script
if (len(sys.argv) == 1):
    createJson(4)
else:
    createJson(int(sys.argv[1]))

time.sleep(2)
driver.close()
