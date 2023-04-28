import socket
from _thread import *
import threading
from sys import platform

directory = 'distributive-4a'
if(platform.startswith('win32')):
    directory = 'distributive-4a\\'
else:
    directory = 'distributive-4a/'

# Thread to handle each "client_soc" connection
def handler_master(client_soc:socket, client_add, command_list:list[str]):
    print(f"[MASTER THREAD] Connection request accepted from {client_add[0]},{client_add[1]}")
    cmd = command_list.pop(0)
    client_soc.send(cmd.encode())
    print(f"[MASTER THREAD] Sent commands of {cmd} to {client_add[0]}, {client_add[1]}")
    client_soc.close()
    print(f"[MASTER THREAD] Closed server-to-client socket on {client_add[0]}, {client_add[1]}")

# Thread to handle each receiving data connection
def handler_receiver(client_soc:socket, client_add):
    print(f"[RECEIVER THREAD] Connection request accepted from {client_add[0]},{client_add[1]}")
    data = client_soc.recv(1000)
    
    while data:
        print(data.decode())
        data = client_soc.recv(1000)
    client_soc.close()
    print(f"[RECEIVER THREAD] Closed client-to-server socket on {client_add[0]},{client_add[1]}")


def main_master(port:int):
    print("[MASTER] Thread started!")
    commands = None
    with open(directory+'cmds.txt', 'r') as cmd: 
            commands = cmd.readlines()
            commands.pop(0)
            cmd.close()
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: 
        server_socket.bind(('', port))
        server_socket.listen()
        print('[MASTER] Master accepting connections...')
        while(True):
            with open(directory+'cmds.txt', 'r') as cmd: 
                client_connected, client_address = server_socket.accept()
                threading.Thread(target=handler_master,args=(client_connected, client_address, commands), daemon=True).start() 
                
                if cmd.readline() == 'stop':
                    print('[SERVER] Server stopped!')
                    break            
    server_socket.close()

def main_receiver(port:int):
    print('[RECEIVER] Thread started!')
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: 
        server_socket.bind(('', port))
        server_socket.listen()
        print('[RECEIVER] Receiver accepting connections...')
        
        ### OS conditional
        
        client_connected, client_address = server_socket.accept()
        threading.Thread(target=handler_receiver,args=(client_connected, client_address), daemon=True).start() 
        
        ### end OS conditional 
    server_socket.close()

if __name__ == "__main__":
    port = int(input('Enter port # '))
    # main_master()
    threading.Thread(target=main_master, args=[port]).start()
    threading.Thread(target=main_receiver, args=[port+1]).start()