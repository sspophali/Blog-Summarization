# -*- coding: utf-8 -*-
"""
Created on Thu May  9 01:40:11 2019
Title : Script for Extracting summary using selenium
author: Sameer & Sagar
"""

import pandas as pd
import numpy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import MySQLdb
import os

# Database connection
db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     passwd="Data@123",  # your password
                     db="blogs_dataset")        # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
cur = db.cursor()

#chrome_options = Options()  
#chrome_options.add_argument("--headless")   
#capa = DesiredCapabilities.CHROME
#capa["pageLoadStrategy"] = "none"
os.environ['MOZ_HEADLESS'] = '1'

blog_dataset = pd.read_csv('C:\Sameer\Data Science\Aegis\Capstone\Data\Blogs\Clean\DataSet\Algorithms.csv')
blog_dataset = blog_dataset[(blog_dataset['site']=='medium.com') & (blog_dataset.no_of_lines >=201) & (blog_dataset.no_of_lines <=300)]
blog_dataset['summarized']='NaN'
blog_dataset=blog_dataset[0:2]
try:            
               
    #wait = WebDriverWait(driver, 10)#10 seconds wait.increase if your net is slow    
    #wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_doc79r')))
    for ind in blog_dataset.index:
        print('\nWorking for blog: '+blog_dataset['title'][ind]+"...")
        #driver = webdriver.Chrome('C://Users//Sameer//Desktop//chromedriver_win32//chromedriver.exe',desired_capabilities=capa,options=chrome_options)
        driver = webdriver.Firefox(executable_path='C://Users//Sameer//Desktop//Firefox//geckodriver.exe')
        driver.get('http://textsummarization.net/text-summarizer') 
        #wait = WebDriverWait(driver, 15)#10 seconds wait.increase if your net is slow 
        time.sleep(6)   #depend on internet speed adjust this value
        text=blog_dataset['text'][ind]
        urlBox = driver.find_element_by_id('text')
        urlBox.send_keys(text)
        sentNum = driver.find_element_by_id('sentnum')
        sentNum.clear()
        sentNum.send_keys(int(round((blog_dataset['no_of_lines'][ind])/5)))
        sentNum.send_keys(Keys.ENTER)
        time.sleep(3)   #
        source=driver.page_source
        soup=BeautifulSoup(source,'html.parser')
        summary=soup.find_all('div',attrs={'class':'span5'}) 
        res=[]
        for r in summary:
            res.append(r.find('p').text)
        if len(res) !=1 :    
            summary_text=res[1].replace('\n',"")
        else:
            summary_text=res[0].replace('\n',"")
        blog_dataset['summarized'][ind]=summary_text.encode('ascii','ignore').decode('ascii')
        try:
            cur.execute("""INSERT INTO blog_text VALUES (%s,%s)""",(blog_dataset['uuid'][ind],summary_text.encode('ascii','ignore').decode('ascii')))
            db.commit()
        except:
            db.rollback()
        
        driver.close()
except:
    print("Error in Connection")