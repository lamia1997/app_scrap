#!/usr/bin/env python
# coding: utf-8

# ## importer les packages necessaire 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup 
import pandas as pd
import requests
import os
import pymongo
import time

images=[]
Comment=[]
Post=[]
# ## Connexion

PATH = 'chromedriver.exe'
options=webdriver.ChromeOptions()
prefs={'profile.default_content_setting_values.notifications': 2}
options.add_experimental_option('prefs',prefs)
driver = webdriver.Chrome(PATH,options=options)
#appel a la page principal de facebook
driver.get("https://www.facebook.com/login")
time.sleep(3)

#agrandir la fenetre
driver.maximize_window()
time.sleep(2)
#cliquer sur le bouton des cookies
cookies = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]')
cookies.click()
time.sleep(3)
#se connecter avec les identifiants 
email=driver.find_element_by_id('email')
email.click()
email.send_keys('lamiabenhamadi@hotmail.fr')
passw=driver.find_element_by_id('pass')
passw.click()
passw.send_keys('@ninaaicha123')
login=driver.find_element_by_id('loginbutton').click()
for i in ["photos_by"]:    
    #get la page 
    driver.get("https://www.facebook.com/hashtag/harcelement")
    time.sleep(5)    
    #scroler la page dans une intervall de 0 a 6
    for j in range(0,6):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
    #recuperer tous les liens de la page
    liens = driver.find_elements_by_tag_name('a')
    liens = [a.get_attribute('href') for a in liens]
    #prendre que les liens qui commence par photo 
    liens = [a for a in liens if str(a).startswith("https://www.facebook.com/photo")]
    print('on vas integrer ' + str(len(liens)) + 'posts' )

#parcourir tous les liens des photos
for lien in liens:
    driver.get(lien)
    time.sleep(2)
    comments=driver.find_elements_by_css_selector("[class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql']") or driver.find_elements_by_css_selector("[class='ee']") or driver.find_elements_by_css_selector("[class='eg']")
    for comment in comments:
        comment=comment.text
        Comment.append(comment)
        imag = driver.find_elements_by_tag_name("img")
        images.append(imag[1].get_attribute("src"))
        try:
            post = driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[1]/div[1]/div[2]')          
            Post.append(post.text)
        except:
            txt='None'
            Post.append(txt)
                

data = pd.DataFrame({'Post': Post ,'Comment': Comment,'images': images})
data.dropna()
data["Post"] = data["Post"].astype(str)
data["Post"] = data["Post"].str.replace("%", "")
data["Post"] = data["Post"].str.replace(",", ".")
data["Post"] = data["Post"].str.replace("@", "")
data["Post"] = data["Post"].str.replace("\n", ".")
data["Post"] = data["Post"].str.replace("#", "")
#supprimer les ligne ou il ya pas de post
data.drop( data[(data["Post"].str.contains('None'))
data["Comment"] = data["Comment"].str.replace("?", "")
data["Comment"] = data["Comment"].str.replace("\n", "")
data["Comment"] = data["Comment"].str.replace("!", "")
#table enfant
Enfant = data[data['Post'].str.contains('enfant')]
#l'insertion dans mongodb
client = pymongo.MongoClient("mongodb://localhost:27017")
data = data.to_dict(orient ="records")
Enfant = Enfant.to_dict(orient ="records")
db = client["kaisens"]
db2 = client["Enfantdb"]
db.kaisens.insert_many(data)
db2.Enfantdb.insert_many(data)




