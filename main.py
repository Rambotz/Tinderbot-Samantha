from logging import exception
import profile
from xml.dom import UserDataHandler
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,InvalidElementStateException
import time, random, pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import  json, os, pandas as pd, threading
from faker import Faker
from urllib3 import Retry
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
load_dotenv()
from Bot import Bot


df = pd.read_csv('profile.csv')
selected_cols = ['email','password','profiles','proxies']
mask = df[selected_cols].isnull().any(axis=1)
df.drop(index=df[mask].index, inplace=True)

def work(email,password,proxy):
    try:
        bot = Bot()
        bot.get_driver(profile_name=email,proxy=proxy)
        bot.check_email_login(email,password)
        bot.Swipe(email)
        bot.CloseDriver()
    except: ...

threads = []
for index, row in df.iterrows():

    print(index)
    x = threading.Thread(target=work, args=(row['email'],row['password'],row['proxies']))
    x.start()
    
    threads.append(x)
    # If there are already 10 threads running, wait for one to complete
    if len(threads) == 10:
        for thread in threads:
            thread.join()
        threads = []
    
    if (index+1) %10 == 0:
        
        for thread in threads:
            thread.join()