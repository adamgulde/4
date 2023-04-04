### Brute force program to iterate through given Schoology user ids and log
### real users into a csv file. Prune.py then cleans csvs and download_images.py
### finds pfps and downloads them.

### I have edited out sensitive information prior to uploading to github, 
### namely my email and password required to run the webscraper. 
### Perhaps in the future an official authenticator should be used, 
### instead of writing in my information in the script. 

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time as time

def config():
    if not True: #add input asking if it should be ran in background
        op = webdriver.ChromeOptions()
        op.add_argument('headless')
        driver = webdriver.Chrome(options=op)
    else: driver = webdriver.Chrome()#executable_path="C:/selenium/chromedriver.exe")
    driver.get("https://bishopmoore.schoology.com/")
    input_box = driver.find_element(By.ID, value="identifierId")
    input_box.send_keys("#####", Keys.ENTER)
    time.sleep(1)
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    input_box.send_keys("#####", Keys.ENTER)
    time.sleep(4)
    return driver

user_list = []
def create_url_list(start_id:int, end_id:int):
    for id in range(end_id - start_id):
        base = f"https://bishopmoore.schoology.com/user/{start_id + id}/info"
        user_list.append(base)
    return user_list

user_exists = []
def get_positive_user_id(driver :webdriver, url_list :list):
    wait = WebDriverWait(driver, 0, poll_frequency=0.01)
    for user in url_list:
        driver.get(user)
        try:
            wait.until(EC.title_contains("|"))
            user_exists.append(1) 
        except TimeoutException:
            user_exists.append(0)
            print("Unavailable user at: ", user)
        # try:
        #     element = WebDriverWait(driver, 0, poll_frequency=0.1).until(
        #         EC.presence_of_element_located((By.CLASS_NAME, "profile-picture"))
        #     )
        #     user_exists.append(1) 
        # except:
        #     print("Unavailable user at: ", user)
        #     # error_type = driver.find_element(By.XPATH, "//*[@id='error-page']/h2")
        #     user_exists.append(0)
    driver.quit()        


def consolidate_data(start_id:int, end_id:int):
    data_df = pd.Series(user_exists, user_list)
    data_df.to_csv(f"Pinged Schoology Profiles at {start_id} to {end_id}.csv")


def main():
    start_id = int(input("Start user ID (INCLUSIVE): "))
    end_id = int(input("End user ID (EXCLUSIVE): "))
    input(f"Press ENTER to iterate through {end_id-start_id} users...")
    d = config()
    user_list = create_url_list(start_id, end_id)
    start_time = time.time()
    get_positive_user_id(d, user_list)
    end_time = time.time()
    efficiency = round((end_id-start_id)/(end_time-start_time), 3)
    print(f"Total time iterating: {(int(end_time-start_time))//60}m:{(int(end_time-start_time))%60}s\nTotal URLS iterated: {end_id-start_id}\nAverage runtime efficiency: {efficiency} users/sec")
    consolidate_data(start_id, end_id)

if __name__=="__main__":
    main()