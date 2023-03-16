import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException,InvalidElementStateException
import time, random, pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import  json, os
from selenium.common.exceptions import *
from faker import Faker
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from addproxy import get_proxy_extension
from dotenv import load_dotenv
load_dotenv()



class Bot:
    def __init__(self):
        self.all_response_text = []
        self.email = os.getenv('EMAIL').replace('@gmail.com','')+'+'+str(random.randint(10000,99999))+'@gmail.com'
        self.password = os.getenv('PASSWORD')
        self.number = 0
        
    def get_driver(self,profile_name='Default',profileDict = 'Profiles',latitude='', longitude='',proxy='') :
        options = webdriver.ChromeOptions()
        profile_name = str(profile_name)
        self.profile = profile_name
        options.add_argument(f"--user-data-dir={profileDict}") 
        options.add_argument("--disable-popup-blocking")
        options.add_argument(f'--profile-directory={profile_name}')
        if proxy:
            if '@' in str(proxy):
                parts = proxy.split('@')

                user = parts[1].split(':')[0]
                pwd = parts[1].split(':')[1]

                host = parts[0].split(':')[0]
                port = parts[0].split(':')[1]
            print('user='+str(user)+'pass='+str(pwd)+'host='+str(host)+'port='+str(port))
            extension = get_proxy_extension(PROXY_HOST=str(host), PROXY_PORT=str(port), PROXY_USER=str(user), PROXY_PASS=str(pwd) , profile_name=profile_name)
            options.add_argument(f'--load-extension={extension}')
        # create a dictionary to specify the latitude and longitude
        if latitude and longitude:
            location = {"latitude": latitude, "longitude": longitude, "accuracy": 100}
            # add the location dictionary to the ChromeOptions object
            options.add_argument('--enable-geolocation')
            options.add_argument('--use-fake-ui-for-media-stream')
            options.add_argument('--enable-precise-memory-info')


        # options.headless = True
        self.driver = uc.Chrome(use_subprocess=True,options=options)
        self.driver.maximize_window()
        
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())
        
        # profile = webdriver.FirefoxProfile('Profiles_FF')
        # self.driver = webdriver.Firefox(profile)
        # self.driver.maximize_window()
        
        if latitude and longitude:
            self.driver.execute_cdp_cmd('Emulation.setGeolocationOverride', location)
        
    def find_element(self, element, locator, locator_type=By.XPATH,
            page=None, timeout=10,
            condition_func=EC.presence_of_element_located,
            condition_other_args=tuple()):
        """Find an element, then return it or None.
        If timeout is less than or requal zero, then just find.
        If it is more than zero, then wait for the element present.
        """
        try:
            if timeout > 0:
                wait_obj = WebDriverWait(self.driver, timeout)
                ele = wait_obj.until(
                         EC.presence_of_element_located(
                             (locator_type, locator)))
                # ele = wait_obj.until(
                #         condition_func((locator_type, locator),
                #             *condition_other_args))
            else:
                ele = self.driver.find_element(by=locator_type,
                        value=locator)
            if page:
                print(
                        f'Found the element "{element}" in the page "{page}"')
            else:
                print(f'Found the element: {element}')
            return ele
        except (NoSuchElementException, TimeoutException) as e:
            if page:
                print(f'Cannot find the element "{element}"'
                        f' in the page "{page}"')
            else:
                print(f'Cannot find the element: {element}')
                
    def click_element(self, element, locator, locator_type=By.XPATH,
            timeout=10):
        """Find an element, then click and return it, or return None"""
        ele = self.find_element(element, locator, locator_type, timeout=timeout)
        if ele:
            ele.click()
            print(f'Clicked the element: {element}')
            return ele

    def input_text(self, text, element, locator, locator_type=By.XPATH,
            timeout=10, hide_keyboard=True):
        """Find an element, then input text and return it, or return None"""
        
        ele = self.find_element(element, locator, locator_type=locator_type,
                timeout=timeout)
        if ele:
            time.sleep(1)
            ele.clear()
            ele.send_keys(text)
            print(f'Inputed "{text}" for the element: {element}')
            return ele    
    
    def change_window(self,index=0):
        AllWindow = self.driver.window_handles
        if index:
            self.driver.switch_to.window(AllWindow[index])
            return
            
        CurrentWindow = self.driver.current_window_handle
        for window in AllWindow:
            if window != CurrentWindow:
                self.driver.switch_to.window(window)
                break
        
    def check_email_login(self,email,password):
        for _ in range(3):
            self.driver.get('https://myaccount.google.com/')
            
            check_account = self.find_element('check account','/html/body/header/div[1]/div[5]/ul/li[2]/a',timeout=5)
            if check_account : 
                if check_account.text == 'Go to Google Account': 
                    check_account.click()
                    self.login_gmail(email,password)
            else : 
                ...
    
    def login_gmail(self,email,password):
        
        self.random_sleep(5,10)
        self.input_text(email,'Input Field','//*[@id="identifierId"]')
        self.click_element('Next btn','//*[@id="identifierNext"]/div/button')
        self.random_sleep(3,7)
        # breakpoint()
        self.input_text(password,'Input Field','//*[@id="password"]/div[1]/div/div[1]/input')
        self.click_element('Next btn','//*[@id="passwordNext"]/div/button')
        self.random_sleep(5,10)
        
    def random_sleep(self,x1=1,x2=5):
        rr = random.randint(x1,x2)
        print(f'time sleep : {rr}')
        time.sleep(rr)
        
    def CloseDriver(self):
        breakpoint()
        try:self.driver.quit()
        except : ...
        
    def set_custom_location(self, latitude, longitude, accuracy="100%"):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "accuracy": int(accuracy.split('%')[0])
        }
        location = {'latitude': latitude, 'longitude': longitude, 'accuracy': 100}
        self.driver.execute_cdp_cmd('Emulation.setGeolocationOverride', location)
        
    def change_framework(self,element):
        self.driver.switch_to.frame(element)
    
    def is_bann(self):
        try:
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
            bann_xpath = '//*[text()="You Have Been Banned From Tinder"]'
            bann = self.driver.find_element(By.XPATH,bann_xpath)
            if bann:return True
        except NoSuchElementException:
            pass
        except TimeoutException:
            pass
        except:... 
        
    def user_login(self):
        breakpoint()
        fr1 = self.find_element('Google login framework','/html/body/div[2]/main/div/div/div[1]/div/div/div[3]/span/div/div/div/div/iframe')
        self.change_framework(fr1)
        self.click_element('google login','/html/body/div/div/div[2]')
        self.random_sleep()
        
        if self.is_bann():
            self.CloseDriver()
            
        try:
            handles = self.driver.window_handles
            self.driver.switch_to.window(handles[-1])
            self.click_element('Google account','/html/body/div/div[1]/div/div/main/div/div/div[1]/div[1]/div[1]')
            self.click_element('Confirm btn','/html/body/div/div[1]/div/div/main/div[3]/div[1]',timeout=3)
        except : ...
        
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[-1])
        number_ele = self.find_element('Mobile number','/html/body/div[2]/main/div/div[1]/div/div[1]/h3')
        if number_ele:
            if number_ele.text == "Enter your mobile number":
                self.number = int(input('Please create an account and come back again\nPress Enter to continue with others :'))
                self.CloseDriver()
                return
                # self.number = int(input('Please Enter mobile number (it must be only number) :'))
            
        body_ele = self.find_element('Google login framework','body',By.TAG_NAME)
        self.change_framework(body_ele)
        self.random_sleep()
        
    def close_popups(self):
        self.click_element('allow geo location','/html/body/div[2]/main/div/div/div/div[3]/button[1]',timeout=0)
        self.click_element('Notification for matching','/html/body/div[2]/main/div/div/div/div[3]/button[1]',timeout=0)
        self.click_element('add to home( no intrested btn)','/html/body/div[2]/main/div/div[2]/button[1]', timeout=0)
        self.click_element('No thanks (buy a primium)','/html/body/div[2]/main/div/div[3]/button[2]',timeout=0)
        
        
        
    def Swipe(self):

        print('work is starting from here')     
        if not "tinder" in self.driver.current_url:
            self.driver.get("https://tinder.com/?lang=en")
            time.sleep(1.5)
        else:
            print("User is not logged in yet.\n")
            return False
        
        
        if self.click_element('Login btn','/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]',timeout=5):
            self.user_login()
        else:
            print('User is alredy logged in')
        breakpoint()
        like_ration = int(os.getenv('LIKE_RATION'))
        
        for _ in range(50):
            self.random_sleep(1,4)
            self.close_popups()
            random_number = random.randint(1, 10)
            breakpoint()
            if random_number <= like_ration:
                self.click_element('Like btn','/html/body/div[1]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div/div[4]/button')
                try:
           
                    action = ActionChains(self.browser)
                    action.send_keys(Keys.ARROW_RIGHT).perform()

                except (TimeoutException, ElementClickInterceptedException):
                    self._get_home_page()
            else:
                try:
           
                    action = ActionChains(self.browser)
                    action.send_keys(Keys.ARROW_LEFT).perform()

                except (TimeoutException, ElementClickInterceptedException):
                    self._get_home_page()
        