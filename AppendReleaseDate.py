'''
Created on Feb 24, 2018
http://store.steampowered.com/api/appdetails?appids=
@author: Andy
'''
import json
import urllib.request
import time

with open("dataSports.json") as fo:
    data2 = json.load(fo)

keysToDel = []

for key in data2.keys():
    result = urllib.request.urlopen("http://store.steampowered.com/api/appdetails?appids=" + key).read()
    resultJson = json.loads(result.decode('utf8'))
    
    try:
        data2[key]["release_date"] = resultJson[key]["data"]["release_date"]["date"]
    except (KeyError):
        keysToDel.append(key)
    time.sleep (2);
        
#for keyDel in keysToDel:
#    del data2[keyDel]
    
with open("dataSports1.json", "w") as fo:
    json.dump(data2, fo)