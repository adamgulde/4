import socket
from _thread import *
import threading
from sys import platform

# Thread to handle each "client_soc" connection
def handler(client_soc:socket, client_add, command_list:list):
    print(f"[SERVER THREAD] Connection request accepted from {client_add[0]},{client_add[1]}")
    client_soc.send(command_list.pop(0).encode())
    client_soc.close()

def main():
    commands = None
    if(platform.startswith('win32')):
        with open('distributive-4a\cmds.txt', 'r') as cmd: 
            commands = cmd.readlines()
            commands.pop(0)
            cmd.close()
        ## create commands list
    else:
        with open('distributive-4a/cmds.txt', 'r') as cmd:
            commands = cmd.readlines()
            commands.pop(0)
            cmd.close()
    
    

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket: 
        server_socket.bind(('', 3131))
        server_socket.listen()
        while(True):
            if(platform.startswith('win32')):
                with open('distributive-4a\cmds.txt', 'r') as cmd: 
                    client_connected, client_address = server_socket.accept()
                    threading.Thread(target=handler,args=(client_connected, client_address, commands), daemon=True).start() 
                    
                    if cmd.readline() == 'stop':
                        print('[SERVER] Server stopped!')
                        break
                ## create commands list
            else:
                with open('distributive-4a/cmds.txt', 'r') as cmd:
                    client_connected, client_address = server_socket.accept()
                    threading.Thread(target=handler,args=(client_connected, client_address, commands), daemon=True).start() 
                    
                    if cmd.readline() == 'stop':
                        print('[SERVER] Server stopped!')
                        break                
    server_socket.close()
if __name__ == "__main__":
    main()