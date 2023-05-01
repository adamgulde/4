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

user_exists = []
def get_positive_user_id(start_id:int, end_id:int, driver :webdriver):
    wait = WebDriverWait(driver, 0, poll_frequency=0.01)
    for user in range(start_id, end_id+1):
        driver.get("https://bishopmoore.schoology.com/user/"+str(user)+"/info")
        try:
            wait.until(EC.title_contains("|"))
            user_exists.append(user) 
        except TimeoutException:
            print("Unavailable user at: ", user)
    driver.quit()        

def client_main(cred, start_id, end_id):
    input(f"Press ENTER to iterate through {end_id-start_id} users...")
    d = config(cred)
    start_time = time.time()
    get_positive_user_id(start_id, end_id, d)
    end_time = time.time()
    efficiency = round((end_id-start_id)/(end_time-start_time), 3)
    print(f"Total time iterating: {(int(end_time-start_time))//60}m:{(int(end_time-start_time))%60}s\nTotal URLS iterated: {end_id-start_id}\nAverage runtime efficiency: {efficiency} users/sec")
    return user_exists


def webscrape(ids):
    creds = client_initialize()
    positive_ids = client_main(creds, int(ids[0]), ids[1])
    print("[CLIENT] Finished finding users!")
    return positive_ids

def sendToServer(positiveIDs:str):
    print(positiveIDs)
    strIDs = ' '.join(str(id) for id in positiveIDs)
    print(strIDs)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port+1))
    client_socket.send(strIDs.encode())
    print('[CLIENT] Sent positive ID data!')


def get_command():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))
    command = client_socket.recv(20).decode().strip().split(',')
    conv_cmd = int(command[0]), int(command[1])
    print('[CLIENT] Received command!')
    print(conv_cmd)
    client_socket.close()
    return conv_cmd


def main():
    ids = get_command()
    # posIDS = webscrape(ids)
    # sendToServer(posIDS)
    sendToServer(ids)
    import webbrowser
    webbrowser.open('https://youtu.be/BBGEG21CGo0')
    print('[CLIENT] Client script completed!') 

ip, port = input('Enter IPv4 Address of Master: '), int(input('Enter Port # '))
if __name__=="__main__":
    main()
