Adding a readme for my own sanity

4b. (formerly 4d.) interacts with the database as the following:
Step 1: Local computer acts as CLIENT with respect to the database
    client.js
    
    
    
    
    
    
    
    
    
    
    
    
Step 2: Local computer acts as SERVER with respect to the database
    server.js:
        Connect to DB
        Get wix image DL URL
        Create 'data' file, full of wix image DL URl
        Wait for 'response' file to be created (looping)
    download.py
        Read 'data' file
        Use requests module to download image into filename 'img.jpg'
        TODO: send to 4c. AI...
        Receive AI inference name and confidence level
        Create 'response' file.
        Close files and exit
    server.js
        Read 'response' file
        Upload response string to DB
        Exit