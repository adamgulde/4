import socket
import time
import os
import prune

def webscrape(ids):
    import find_users
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
    init_vals = find_users.client_initialize(int(id1), int(id2))
    f = find_users.client_main(init_vals[0], init_vals[1], init_vals[2])
    print("[CLIENT] Finished finding users!\n\n")
    return f

# def send_data(f):
#     datasent = 0
#     DATA_INCREMENT = 100
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect(('10.13.0.16', 3131))

#     data_to_upload = open(f, 'rb')
#     total_data = os.stat(f).st_size
#     print(f'[CLIENT] Data size: {total_data}')
    
#     client_socket.send(int.to_bytes(total_data))
#     print('[CLIENT] Sent data size!')
    
#     data_chunk = data_to_upload.read(DATA_INCREMENT)
#     while datasent < total_data:
#         client_socket.send(data_chunk)
#         data_chunk = data_to_upload.read(DATA_INCREMENT)
#         datasent += DATA_INCREMENT

#     print('[CLIENT] Data transmitted!')
    
#     data_to_upload.close()
#     ### Wait for confirmation...
#     while client_socket.recv(1) != '1':
#         print('\n[CLIENT] Client waiting for new command...')
#         time.sleep(1)
        
def sendToData(positiveIDs):
    file = open('data', 'w')
    for id in positiveIDs:
        file.write(id+'\n')
    file.close()


def get_command():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('10.13.0.16', 3131))
    # client_socket.send('0'.encode())
    command = client_socket.recv(20).decode()
    print('[CLIENT] Received command!')
    return command

def main():
    # upload_2_DB()
    ids = get_command()
    filename = webscrape(ids)
    posIDs = prune.prune('distributive (4a)/'+filename)
    sendToData(posIDs)
    print('\n[CLIENT] Client script completed!')

if __name__=="__main__":
    ## main()
    filename = 'Pinged Schoology Profiles at 84082862 to 84082870.csv'
    posIDs = prune.prune('distributive (4a)/'+filename)
    sendToData(posIDs)
    print('\n[CLIENT] Client script completed!')