import requests
from os import remove
  

IMG_NAME = 'img.jpg'
url = open("database-4b\data", "r").read()
  
data = requests.get(url).content
  
f = open(IMG_NAME,'wb')
  
f.write(data)
f.close()
  
### Run through AI here



confidence_lvl = 31
detected_face = "Test Adam"

### END AI BLOCK

## remove(IMG_NAME) ## deletes downloaded file

## Creates response file for uploading response to DB
f = open("database-4b\\response", "w")
f.write(f"This looks like {detected_face}, with a confidence level of {confidence_lvl}%")
f.close()