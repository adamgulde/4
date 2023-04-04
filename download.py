import requests
from os import remove
  

IMG_NAME = 'img.jpg'
url = open("data", "r").read()
  
# This statement requests the resource at
# the given link, extracts its contents
# and saves it in a variable
data = requests.get(url).content
  
# Opening a new file named img with extension .jpg
# This file would store the data of the image file
f = open(IMG_NAME,'wb')
  
# Storing the image data inside the data variable to the file
f.write(data)
f.close()
  
### Run through AI here



confidence_lvl = 31
detected_face = "Test Adam"

### AI BLOCK
remove(IMG_NAME)

f = open("response", "w")
f.write(f"This looks like {detected_face}, with a confidence level of {confidence_lvl}%")
f.close()