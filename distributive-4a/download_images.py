from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time as time
import os
directory = ''
def config():
    start_url = input('Where do you want to start? PASS for all users.')
    import time
    driver = webdriver.Chrome()#executable_path="C:/selenium/chromedriver.exe")
    driver.get("")
    input_box = driver.find_element(By.ID, value="identifierId")
    input_box.send_keys("", Keys.ENTER)
    time.sleep(1)
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "password"))
    )
    input_box.send_keys("", Keys.ENTER)
    time.sleep(4)
    return driver, start_url

def get_data(start_url:str):
    users = []
    files = os.listdir(directory)
    for file in files:
        if file.startswith("Users Downloaded at"):
            with open(os.path.join(directory,file), 'r') as f:
                if start_url == 'PASS':
                    users = f.readlines()
                else: 
                    users = f.readlines()                        
                    cut_index = users.index(start_url+"\n")
                    for i in range(cut_index):
                        users.remove(users[0])
    return users


def get_image_urls(d:webdriver, users):
    wait = WebDriverWait(d, 0, poll_frequency=0.01)
    for user in users:
        d.get(user)
        try:
            wait.until(EC.title_contains("|"))
            name = d.find_element_by_xpath('//*[@id="center-top"]/h2').text
            with open(os.path.join(directory,f'{name}_pfp.png'), 'wb') as file:
                file.write(d.find_element_by_xpath('//*[@id="content-left-top"]/div/div/img').screenshot_as_png)
        except TimeoutException:
            pass            
        
        ## //*[@id="content-left-top"]/div/div/img  XPATH FOR PFP
        ## //*[@id="center-top"]/h2                 XPATH FOR NAME
    

if __name__ == "__main__":
    d, start = config()
    u = get_data(start)
    get_image_urls(d, u)
    d.quit()