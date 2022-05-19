
import unittest
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import pandas as pd



class TestScrap(unittest.TestCase):

    def setUp(self):
        """Start web driver"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

    def test_login(self):
        try:
            self.driver.get("https://www.facebook.com/login")
            driver.maximize_window()
            time.sleep(2)
            #cliquer sur le bouton des cookies
            cookies = self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div/div/div[3]/button[2]')
            cookies.click()
            time.sleep(3)
            #se connecter avec les identifiants 
            email= self.driver.find_element_by_id('email')
            email.click()
            email.send_keys('lamiabenhamadi@hotmail.fr')
            passw= self.driver.find_element_by_id('pass')
            passw.click()
            passw.send_keys('@ninaaicha123')
            login= self.driver.find_element_by_id('loginbutton').click()
        except NoSuchElementException as ex:
            self.fail(ex.msg)

    def test_scrap(self):
        """Find and click top-right Start your project button"""
        try:
            for i in ["photos_by"]:    
            #get la page 
            self.driver.get("https://www.facebook.com/hashtag/harcelement")
            time.sleep(5)    
            #scroler la page dans une intervall de 0 a 6
            for j in range(0,6):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(10)
            #recuperer tous les liens de la page
             liens = self.driver.find_elements_by_tag_name('a')
             liens = [a.get_attribute('href') for a in liens]
            #prendre que les liens qui commence par photo 
             liens = [a for a in liens if str(a).startswith("https://www.facebook.com/photo")]
             print('on vas integrer ' + str(len(liens)) + 'posts' )
        except NoSuchElementException as ex:
            self.fail(ex.msg)


if __name__ == '__main__':

