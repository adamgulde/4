import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('10.13.0.16', 3131))
server_socket.listen() 
URL = None

with open('cmds.txt', 'r') as cmd:
    commands = cmd.readlines()
    commands.pop(0)
    ## create commands[] list
    URL = commands.pop(0)
    cmd.close()

while(True):
    with open('cmds.txt', 'r') as cmd:
        client_connected, client_address = server_socket.accept()
        print(f"[SERVER] Connection request accepted from {client_address[0]},{client_address[1]}")
        if cmd.readline() != 'stop':

            ## implement threading                
            client_connected.send(commands[0].encode())

        else: 
            client_connected.send(URL.encode())
            print('[SERVER] Server stopped!')
            break

server_socket.close()