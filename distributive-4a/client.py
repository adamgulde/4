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
import os
import socket

def client_initialize(s_id, e_id):
    print("Data is not stored after code execution.")
    cred = (input("Email: "), input("Password: "))
    return cred, s_id, e_id

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
    input_box = WebDriverWait(driver, 10).until(
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
            ## user_exists.append(0)
            print("Unavailable user at: ", user)
    driver.quit()        

# def consolidate_data(start_id:int, end_id:int):
#     data_df = pd.Series(user_exists, user_list)
#     filename = f"Pinged Schoology Profiles at {start_id} to {end_id}.csv"
#     data_df.to_csv('distributive-4a/'+filename)
#     return filename

def client_main(cred, start_id, end_id):
    input(f"Press ENTER to iterate through {end_id-start_id} users...")
    d = config(cred)
    user_list = create_url_list(start_id, end_id)
    start_time = time.time()
    get_positive_user_id(d, user_list)
    end_time = time.time()
    efficiency = round((end_id-start_id)/(end_time-start_time), 3)
    print(f"Total time iterating: {(int(end_time-start_time))//60}m:{(int(end_time-start_time))%60}s\nTotal URLS iterated: {end_id-start_id}\nAverage runtime efficiency: {efficiency} users/sec")
    return user_exists


def webscrape(ids):
    id1 = ''
    id2 = ''
    next = False
    for id in ids: ### Parsing string properly
        if id != ',':
            if not next:
                id1 = id1 + id
            if next:
                id2 = id2 + id
        else:
            next = True
    print(id1, id2)
    init_vals = client_initialize(int(id1), int(id2))
    positive_ids = client_main(init_vals[0], init_vals[1], init_vals[2])
    print("[CLIENT] Finished finding users!\n\n")
    return positive_ids
ip = 'localhost'

def sendToServer(positiveIDs):
    # file = open('data', 'w')
    # for id in positiveIDs:
    #     file.write(id+'\n')
    # file.close()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, 3131))
    # client_socket.send('0'.encode())
    client_socket.sendmsg(positiveIDs)

def get_command():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = input('Enter IPv4 Address of Master: ')
    client_socket.connect((ip, 3131))
    # client_socket.send('0'.encode())
    command = client_socket.recv(20).decode()
    print('[CLIENT] Received command!')
    return command

###
###
###

def main():
    ids = get_command()
    posIDS = webscrape(ids)
    # posIDs = prune('distributive-4a/'+filename)
    sendToServer(posIDS)
    os.remove('distributive-4a\Pinged Schoology Profiles at 84083000 to 84084000.csv')
    import webbrowser
    webbrowser.open('https://youtu.be/G1IbRujko-A')
    os.system('node distributive-4a/uploader.js')
    print('\n[CLIENT] Client script completed!') ## this never gets reached but I am so sick of javascript at this point that I do not care

if __name__=="__main__":
    main()
