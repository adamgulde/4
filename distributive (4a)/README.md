Added readme for my own sanity...

4a is supposed to do quite a few things, starting at server.py

    server.py
        Create socket server, accepting connections on localhost
        From commands.txt file, it reads 'start' then begins iterating through the commands to distribute
        Creates worker threads and accepts 1 connection per thread
        Sends command URL to worker connection
        TODO: close connection... close thread...
        TODO: Query when database is full... how???
    client.py
        Create client socket, connect to server socket
        Receive command URL        
        










[OTHER]:
Run this in terminal: 

xattr -d com.apple.quarantine chromedriver

May need to update chromedriver: 
download is available at https://chromedriver.chromium.org/downloads

Server will continue to accept connections as long as the 
first line of cmds.txt does not read "stop" (no quotes)