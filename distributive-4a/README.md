Added readme for my own sanity...

4a is supposed to do quite a few things, starting at server.py

    server.py
        Create socket server, accepting connections on localhost
        From commands.txt file, it reads 'start' then begins iterating through the commands to distribute
        Creates worker threads and accepts 1 connection per thread
        Sends command URL to worker connection
    client.py
        Create client socket, connect to server socket
        Receive command URL
        Begin webscraping -> find_users.py
    find_users.py (consolidated into client.py)
        Initialize webscraping client with user credentials
        TODO: create user credentials list (SENSITIVE DATA)...
        Begin webscraping with client_main function
        Create user ID list
        Webscraping loop, appending 0 and 1 to nonexisting and existing users, respectively 
        Create Pinged Profiles csv file
        Return csv file
        Close find_users.py
    client.py
        Prune csv file from client.py...
        export remaining (positive) ids into 'data'...
        Funny gandalf video
        run uploader.js...
    uploader.js
        For each entry in 'data', upload to database
        TODO: Close... (never reached)
    client.py
        TODO: Close... (never reached)
    server.py
        TODO: close connection... close thread...
        TODO: Query when database is full... how???
    Crash client.py
    Crash server.py










[OTHER]:
Run this in terminal: 

xattr -d com.apple.quarantine chromedriver

May need to update chromedriver: 
download is available at https://chromedriver.chromium.org/downloads

May need to update chrome: 
Chrome settings => About Chrome => should automatically update

Server will continue to accept connections as long as the 
first line of cmds.txt does not read "stop" (no quotes)