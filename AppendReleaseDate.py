'''
Appends release date to json file that contains games. Should be used if creating time series. 
http://store.steampowered.com/api/appdetails?appids=
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
    time.sleep (2);#steam has limit on number of requests within period of time
with open("dataSports1.json", "w") as fo:
    json.dump(data2, fo)