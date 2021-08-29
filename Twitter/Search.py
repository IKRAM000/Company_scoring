#!/usr/bin/env python
# coding: utf-8



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import configparser
import os
import pandas as pd


config_path = '..\\..\\Config\\config.ini'




class seleniumSearch:
    
    browser = None
    path_to_chromedriver = 'C:\\Program Files\\Google\\chromedriver_win32\\chromedriver.exe'
    def __init__(self):
        
        '''
        #read config
        config = configparser.ConfigParser() 
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_p = os.path.abspath(os.path.join(dir_path,config_path))
        config.read(config_p )
        self.path_to_chromedriver = self.ssh_username = config['SELENIUM']['chrome_drive']
        '''
        #open a browser
        options = webdriver.ChromeOptions() 
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.browser =  webdriver.Chrome(options=options,executable_path = self.path_to_chromedriver)
        pass
        
    def __exit__(self):
        self.closebrowser()
        
    def reopenbrowser(self):
        try:
            self.closebrowser()
            self.browser =  webdriver.Chrome(executable_path = self.path_to_chromedriver)
            retry = 0
        except Exception as e:
            print('reopenbrowser Error: ',e)
        pass
    
    def closebrowser(self):
        if self.browser is not None:
            try:
                self.browser.close()
            except Exception as e:
                pass
            
    def googlesearch(self,key):
        #assert self.browser == None, 'Could not found an open browser!'
   
        res = None
        try:
            self.browser.delete_all_cookies()

            self.browser.get("https://www.google.com")
            search_bar = self.browser.find_element_by_name("q")
            search_bar.clear()
            search_bar.send_keys(key)
            search_bar.send_keys(Keys.RETURN)
            result = self.browser.find_element_by_tag_name('h3')
            result.click()
            wait = 0
            #res = self.browser.find_element_by_xpath('//*[@id="rso"]/div[1]/div/div/div[1]/a/h3')
            while 'https://www.google.com/search' in self.browser.current_url and wait <200:
                time.sleep(0.1)
                wait += 1 
                
            if 'https://www.google.com/search' in self.browser.current_url:
                res = None
            else:
                res = self.browser.current_url
        except Exception as e:
            print('googlesearch Error: ',e)
            res = None
        return res
    
    def duckduckgosearch(self,key):
        #assert self.browser == None, 'Could not found an open browser!'
   
        res = None
        try:

            self.browser.get('https://duckduckgo.com')
            time.sleep(2)
            search_form = self.browser.find_element_by_id('search_form_input_homepage')
            search_form.send_keys(key)
            search_form.submit()
            results = self.browser.find_elements_by_class_name('result__a')
            time.sleep(10)
            res = results[0].get_attribute("href")
        except Exception as e:
            print('duckduckgosearch Error: ',e)
            res = None
        return res
     
    def search(self,key,retry=0):
        
       #assert self.browser == None, 'Could not found an open browser!'
        retry = retry
        res = None
        try:
         
            res = self.googlesearch(key)
            
            #if googlesearch if giving None --> try duckduckgo
            if res == None:
                res = self.duckduckgosearch(key)

            #get only the username from the url
            try:
                 c=res.split('?')[0]
            except :
                 pass
            try:
                n=c.split('/')
                username=n[-1]
            except :
                pass    
            #split the user and the key
            try:
                user_splitted=username.split('_')
            except :
                user_splitted=username  
            try:
                keyy=key[10:]
                key_splitted=keyy.split()
            except :
                key_splitted=keyy        
            #check if the company username is correct
            score=0
            for i in user_splitted:
                for j in key_splitted:
                    if i.upper() in j.upper():
                        score+=1      
                        continue
                        
            for i in key_splitted:
                for j in user_splitted :
                    if i.upper() in j.upper():
                        score+=1
                        continue 
            if score < 1 :
                res = None                  
        except Exception as e:
            print('search Error: ',e)
            res = None
        return res
    
    def getMonyhouse_url(self,company_name):
        url = ' https://www.moneyhouse.ch/en/company/ + '
        res = self.search(url+company_name)
        
        if res is None:
            print('return no url!')
            return None
        #validate result
        # fr/: the url must contains a
          
        if 'moneyhouse.ch/' in res and len(res)> len(url):
            return res
            '''tokens = company_name.lower().split(' ')
            for token in tokens:
                if token != None and (token not in res):
                    res = None
                    break'''
        else:
            print(res) 
            res = None
        return res 

    def getCrunchbase_url(self,company_name):
        url = ' https://www.crunchbase.com/organization/ + '
        res = self.search(url+company_name)
        
        if res is None:
            return None
        
         #validate result
        # fr/: the url must contains crunchbase prefix
            
        if 'crunchbase.com/' in res and len(res)> len(url):
            return res
            '''
            tokens = company_name.lower().split(' ')
            for  token in tokens:
                if token != None and (token  not in res):
                    res = None
                    break'''
        else:
            res = None
        return res 
    
    def getLinkedin_url(self,company_name):
        url = 'https://www.linkedin.com/company/ + '
        res = self.search(url+company_name)
        
        if res is None:
            return None
        
               #validate result
        # fr/: the url must contains crunchbase prefix
          
        if 'https://www.linkedin.com/company/' in res and len(res)> len(url):
            return res 
        
            #tokens = company_name.lower().split(' ')
            """for token in tokens:
                if token != None and (token  not in res):
                    res = None
                    break""" 
        else:
            res = None
        
        return res 
        
    def getTwitter_url(self,company_name):
        url = 'twitter + '
        res = self.search(url+company_name)
        print(res)
        if res is None:
            return None
        
               #validate result
        # fr/: the url must contains crunchbase prefix
       
        if 'twitter.com' in res :
            return res 
        
            #tokens = company_name.lower().split(' ')
            """for token in tokens:
                if token != None and (token  not in res):
                    res = None
                    break""" 
        else:
            res = None
        
        return res 

    def get_urls(self,company_name):
        res = {}
        '''
        res['company_name'] = company_name
        res['moneyhouse_url'] = self.getMonyhouse_url(company_name)
        res['crunchbase_url'] = self.getCrunchbase_url(company_name)
        res['linkedin_url'] = self.getLinkedin_url(company_name)
        '''
        return self.getTwitter_url(company_name)
       
#impoting the execl file
df = pd.read_excel ('1.xlsx')


#Searching for the companies url
urls=[]
for i in range(len(df['company_name'])) :
    try:
        s=seleniumSearch()
        urls.append(s.get_urls(df['company_name'][i]))
        df['Twitter_url'][i]=urls[i]
        df.to_excel("outputt.xlsx")
    except:
        pass






