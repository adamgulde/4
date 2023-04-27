### 
### Important functions: 
###
# import pandas as pd
# def prune(filename):
#     pruned_array = []
#     csv_df = pd.read_csv(filename)
#     for entry in csv_df.itertuples():
#         if entry[2] == 1:
#             pruned_array.append(str(entry[1]).removesuffix('/info').removeprefix('https://bishopmoore.schoology.com/user/'))
#     return pruned_array

### Brute force program to iterate through given Schoology user ids and log
### real users into a csv file.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotInteractableException
import time as time
import socket

def client_initialize():
    print("Data is not stored after code execution.")
    cred = (input("Email: "), input("Password: "))
    return cred

def config(credentials:tuple):
    from sys import platform
    if(platform=='win32'):
        driver = webdriver.Chrome(executable_path='distributive-4a\drivers\chromedriver.exe')
    else:
        driver = webdriver.Chrome(executable_path='distributive-4a\drivers\chromedriver')  
    driver.get("https://bishopmoore.schoology.com/")
    input_box = driver.find_element(By.ID, value="identifierId")
    input_box.send_keys(credentials[0], Keys.ENTER)
    time.sleep(1)
    input_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')) or 
        EC.presence_of_element_located((By.NAME, "password"))
    )
    i = 0
    while driver.current_url != 'https://bishopmoore.schoology.com/home':
        try:  
            input_box.send_keys(credentials[1], Keys.ENTER)
            time.sleep(1)
            i+=1
        except ElementNotInteractableException:
            print(f"An error occured, retrying...({i})")
            time.sleep(3)
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
            print("Unavailable user at: ", user)
    driver.quit()        

def client_main(cred, start_id, end_id):
    input(f"Press ENTER to iterate through {end_id-start_id} users...")
    d = config(cred)
    user_list = create_url_list(start_id, end_id) # can be simplified to just use IDs.. 
    start_time = time.time()
    get_positive_user_id(d, user_list)
    end_time = time.time()
    efficiency = round((end_id-start_id)/(end_time-start_time), 3)
    print(f"Total time iterating: {(int(end_time-start_time))//60}m:{(int(end_time-start_time))%60}s\nTotal URLS iterated: {end_id-start_id}\nAverage runtime efficiency: {efficiency} users/sec")
    return user_exists


def webscrape(ids):
    # id1 = ''
    # id2 = ''
    # next = False
    # for id in ids: ### Parsing string properly
    #     if id != ',':
    #         if not next:
    #             id1 = id1 + id
    #         if next:
    #             id2 = id2 + id
    #     else:
    #         next = True
    # print(id1, id2)
    creds = client_initialize()
    positive_ids = client_main(creds, int(ids[0]), ids[1])
    print("[CLIENT] Finished finding users!\n\n")
    return positive_ids

def sendToServer(positiveIDs:str):
    # file = open('data', 'w')
    # for id in positiveIDs:
    #     file.write(id+'\n')
    # file.close()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    
    client_socket.send(positiveIDs.encode())


def get_command():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    # client_socket.send('0'.encode())
    command = client_socket.recv(20).decode().strip().split(',')
    conv_cmd = int(command[0]), int(command[1])
    print('[CLIENT] Received command!')
    print(conv_cmd)
    client_socket.close()
    return conv_cmd

###
###
###

def main():
    ids = get_command()
    posIDS = webscrape(ids)
    # posIDs = prune('distributive-4a/'+filename)
    sendToServer(posIDS)
    import webbrowser
    webbrowser.open('https://youtu.be/G1IbRujko-A')
    print('\n[CLIENT] Client script completed!') ## this never gets reached but I am so sick of javascript at this point that I do not care

ip, port = input('Enter IPv4 Address of Master: '), int(input('Enter Port # '))
if __name__=="__main__":
    main()
