#!/usr/bin/env python
# coding: utf-8

import sys
#sys.path.append("D:\\ACREDIUS\\Code\\WebScraping")

import urllib.request
from urllib.error import HTTPError
#error.HTTPError
import bs4 as bs
from ._html import _html

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


from WebScraping.urlsearch.urlsearch import urlSearch
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

from WebScraping.urlsearch.urlsearch import urlSearch
from WebScraping.urlsearch.seleniumSearch import seleniumSearch

from google_trans_new import google_translator
translator = google_translator()

import configparser
import os

config_path = '..\\..\\Config\\config.ini'

class facebookScraper:

    url_search = None
    url_selenium = None
    #chrome browser
    browser = None
    base_url = 'https://www.facebook.com/'
    
    pages = '//*[@id="mount_0_0_bD"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[2]/div[7]/a/div[1]/div[2]/div/div/div/div/span/span'
    
    res = '//*[@id="mount_0_0_bD"]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/h2/span/span/span/a/span[1]'
    
    path_to_chromedriver = None
    
    user_xpath = '//*[@id="email"]' 
    pwd_xpath = '//*[@id="pass"]'
    
    user = 'goneber194@cfcjy.com'
    pwd = '98406161' 
    def __init__(self, usr=None, pwd=None):
        
        if usr==None:
            usr = self.user
        if pwd==None:
            pwd=self.pwd
        #configuration
        config = configparser.ConfigParser() 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_p = os.path.abspath(os.path.join(dir_path,config_path))
        config.read(config_p )
        self.path_to_chromedriver = self.ssh_username = config['SELENIUM']['chrome_drive']
        options = webdriver.ChromeOptions()
        prefs ={"profile.default_content_setting_values.notifications" : 2}
        options.add_experimental_option("prefs",prefs)
        #preferences for disabling credential notif
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        options.add_experimental_option('useAutomationExtension', False)
        self.browser =  webdriver.Chrome(options=options,executable_path = self.path_to_chromedriver)

        self.facebook_login(usr, pwd)
#         self.url_search = urlSearch()
#         self.url_selenium = seleniumSearch()
        pass
    
    def __exit__(self):
        try:
            self.browser.close()
        except Exception as e:
            pass
    def facebook_login(self,user,pwd):
        try:
            self.browser.get(self.base_url)
            
            
            #login & password
            
            user_bar = self.browser.find_element_by_xpath(self.user_xpath)
            user_bar.clear()
            user_bar.send_keys(user)
            
            pwd_bar = self.browser.find_element_by_xpath(self.pwd_xpath)
            pwd_bar.clear()
            pwd_bar.send_keys(pwd)
            pwd_bar.send_keys(Keys.RETURN)
            
        except Exception as e:
            pass
            print('Login Error: ',e)
            
    

    def facebook_url(self, companyName):
        url = None
        
        def clear_text(element):
            length = len(element.get_attribute('value'))
            element.send_keys(length * Keys.BACKSPACE)
        #enter companyName in searchBar and get a result
        wait = WebDriverWait(self.browser, 20)
        
        search = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='global_typeahead']")))
        clear_text(search)
        search.send_keys(companyName)
        search.send_keys(Keys.RETURN)
        time.sleep(15)
        
#         #parsing soup based on a determined class
        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = self.browser.execute_script("return document.body.scrollHeight")

        while True:
        # Scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
            
                break
            
            last_height = new_height
  
        time.sleep(4)
        page = self.browser.page_source      
        pg = bs.BeautifulSoup(page, 'lxml')        
        tag = pg.find_all('a', {'class': "oajrlxb2 gs1a9yip g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 q9uorilb mg4g778l btwxx1t3 pfnyh3mw p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh p8dawk7l oo9gr5id"})        
        
        tag2 = pg.find_all('span', {'class':"a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 nkwizq5d roh60bw9 hop8lmos scwd0bx6 n8tt0mok hyh9befq jwdofwj8 r8blr3vg"})
        i=-1
        while True:
            i = i+1
            if i == len(tag):
                break
            else:
                
                if len(companyName.split()) == 1:
                    if companyName.lower() == tag2[i].text.lower():
                        break
                elif len(companyName.split()) == 2:
                    
                    if companyName.split()[0].lower()== tag2[i].text.split()[0].lower() and companyName.split()[1].lower() in tag2[i].text.lower():
                        break
                else:
                    if companyName.split()[0].lower() in tag2[i].text.lower() and companyName.split()[1].lower() in tag2[i].text.lower() and companyName.split()[2].lower() in tag2[i].text.lower():                        
                        break
                    
        if i < len(tag):
            url = tag[i+1]['href']
            
        return url
            
    def get_facebook_info(self,company_name,url=None):
        if url ==None:
            url = self.facebook_url(company_name)
        print('url',url)
        return self.get_fb_info(url)
        
    def get_fb_info(self,fb_url):
        res = {}
        
        res['fb_followers'] = 0
        res['fb_likers'] = 0
        res['fb_phone'] = None
        if fb_url is not None:
            
            try:
                print(fb_url)
                self.browser.get(fb_url)
                time.sleep(5)
                page= self.browser.page_source
                pg = bs.BeautifulSoup(page, 'lxml')
                tag = pg.find_all('span', {'class': "d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh jq4qci2q a3bd9o3v knj5qynh oo9gr5id"})
                tag1 = (tag[2].text.lstrip().rstrip()).split()
                tag2 = (tag[0].text.lstrip().rstrip()).split()
                res['fb_followers'] = tag1[0]
                res['fb_likers'] = tag2[0]
                res['fb_phone'] = tag[3].text
            except Exception as e:
                                  print (e)
          

        return res
        


