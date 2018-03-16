
import urllib.request
import json
import re
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

if __name__ == '__main__':
    #by genre. Change genre to pull from a different genre. Available genres can be found on steamspy.com
    steamspy = urllib.request.urlopen("http://steamspy.com/api.php?request=genre&genre=simulation").read()
    
    steamspyJson = json.loads(steamspy.decode('utf8'))
    
    translation_table = dict.fromkeys(map(ord, "- :!,'/"), None)
    
    #exclude 0
    regex = re.compile(r"[1-9]")
    
    done = 0;
    for gameID in steamspyJson.keys():
        if steamspyJson[gameID]["price"] is not "0":#not a free game
            result = urllib.request.urlopen("http://steamsales.rhekua.com/view.php?steam_type=app&steam_id=" + gameID).read()
            html = result
            parsed_html = BeautifulSoup(html, "lxml")
            
            saleDate = ""
            saleDuration = ""
            
            #create key
            steamspyJson[gameID]['Sale History'] = []
            for word in parsed_html.body.find_all('div', attrs={'class':'tab_desc with_discount'}):
                for word1 in word.find_all('div', attrs=({'class':'genre_release'})):#search for all discount percentages

                    startEndDate = word1.text.split(" ")
                    saleStartDate = re.sub('\s+', '', startEndDate[0])
                    saleEndDate = startEndDate[3]
                    
                    print (str(done) + " " + gameID + " " + saleStartDate + " " + saleEndDate)
                    #append to Sale History key
                    steamspyJson[gameID]['Sale History'].append({saleStartDate: saleEndDate})
            
            done += 1
    #output results to json
    with open('dataSimulation.json', 'w') as outfile:
        json.dump(steamspyJson, outfile)