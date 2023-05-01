import socket
from _thread import *
import threading
from sys import platform

thread_num = 0
passed_flag = False

directory = 'distributive-4a'
if(platform.startswith('win32')):
    directory = 'distributive-4a\\'
else:
    directory = 'distributive-4a/'

# Thread to handle each "client_soc" connection
def handler_master(client_soc:socket, client_add, command_list:list[str], thrN:int):
    thrN = thrN + 1
    print(f"[MASTER THREAD] Connection request accepted from {client_add[0]},{client_add[1]}")
    cmd = command_list.pop(0)
    client_soc.send(cmd.encode())
    print(f"[MASTER THREAD] Sent commands of {cmd} to {client_add[0]}, {client_add[1]}")
    client_soc.close()
    print(f"[MASTER THREAD] Closed server-to-client socket on {client_add[0]}, {client_add[1]}")

# Thread to handle each receiving data connection
def handler_receiver(client_soc:socket, client_add, pf:bool):
    print(f"[RECEIVER THREAD] Connection request accepted from {client_add[0]},{client_add[1]}")
    data = client_soc.recv(1000)
    
    while data:
        print(data.decode())
        data = client_soc.recv(1000)
    client_soc.close()
    thread_num = thread_num - 1
    print(f"[RECEIVER THREAD] Closed client-to-server socket on {client_add[0]},{client_add[1]}")


def main_master(port:int):
    print("[MASTER] Thread started!")
    commands = None
    with open(directory+'cmds.txt', 'r') as cmd: 
            commands = cmd.readlines()
            cmd.close()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: 
        server_socket.bind(('', port))
        server_socket.listen()
        print('[MASTER] Master accepting connections...')
        opened_threads = 0
        while(len(commands) != opened_threads):
            client_connected, client_address = server_socket.accept()
            threading.Thread(target=handler_master,args=(client_connected, client_address, commands, thread_num), daemon=True).start() 
            opened_threads = opened_threads + 1

    print('[SERVER] Initialized all master handler threads!')       
    server_socket.close()
    print('[SERVER] Server stopped.')       
    

def main_receiver(port:int):
    print('[RECEIVER] Thread started!')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: 
        server_socket.bind(('', port))
        server_socket.listen()
        print('[RECEIVER] Receiver accepting connections...')
        
        while(thread_num!=0):
            print('Here')
            client_connected, client_address = server_socket.accept()
            threading.Thread(target=handler_receiver,args=(client_connected, client_address), daemon=True).start() 
    
        if(passed_flag):
            print('[RECEIVER] Receiver handler threads completed!')
            server_socket.close()
            print('[RECEIVER] Receiver stopped.')

if __name__ == "__main__":
    port = int(input('Enter port # '))
    threading.Thread(target=main_master, args=[port]).start()
    threading.Thread(target=main_receiver, args=[port+1]).start()