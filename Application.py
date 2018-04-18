'''
Uses list of games on steamspy (by genre) and isthereanydeal.com to find sale history for each game. Not used as there is a limit on the sale history time period that can be scraped.
Creates json file containing data from each game in genre. 
'''
import codecs
import urllib.request
import json
import time
import re
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
    
ROMAN_NUMERAL_TABLE = [
    ("M", 1000), ("CM", 900), ("D", 500),
    ("CD", 400), ("C", 100),  ("XC", 90),
    ("L", 50),   ("XL", 40),  ("X", 10),
    ("IX", 9),   ("V", 5),    ("IV", 4),
    ("I", 1)
]

#used to convert integer to roman numerals. isthereanydeal.com uses roman numerals for numbers that are non-zero
def convert_to_roman(number):
    """ Convert an integer to Roman
    >>> print(convert_to_roman(45))
    XLV """
    roman_numerals = []
    for numeral, value in ROMAN_NUMERAL_TABLE:
        count = number // value
        number -= count * value
        roman_numerals.append(numeral * count)

    return ''.join(roman_numerals)

def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def repl(match):
    return convert_to_roman(int(match.group(0)))

if __name__ == '__main__':
    #by genre
    steamspy = urllib.request.urlopen("http://steamspy.com/api.php?request=genre&genre=Sports").read()
    
    steamspyJson = json.loads(steamspy.decode('utf8'))
    
    translation_table = dict.fromkeys(map(ord, "- :!,'/"), None)
    
    #exclude 0
    regex = re.compile(r"[1-9]")
    
    done = 0;
    for gameID in steamspyJson.keys():
        gameName = steamspyJson[gameID]["name"]
        gameName = gameName.translate(translation_table)
        gameName = regex.sub(repl, gameName)
        if steamspyJson[gameID]["price"] is not "0" and gameName != "":#not a free game
            print (gameName + ":")
            result = urllib.request.urlopen("https://isthereanydeal.com/game/" + gameName + "/history/?shop%5B%5D=steam&generate=Select+Stores").read()
            html = result
            parsed_html = BeautifulSoup(html, "lxml")
            
            saleDate = ""
            saleDuration = ""
            
            #create key
            steamspyJson[gameID]['Sale History'] = []
            for word in parsed_html.body.find_all('div', attrs={'class':'game log'}):
                for word1 in word.find_all('span', attrs=('lgCut')):#search for all discount percentages
                    if "-0%" not in word1 and word.text != "":#only discounted rows
                        
                        #find correct location in data
                        occurrences = findOccurrences(word.text, "-")
                        
                        #split with spaces
                        filteredData = word.text[occurrences[-2] - 4:].split(" ")#-4 index to include year
                        
                        saleDate = "".join(filteredData[:1])
                        saleDuration = "".join(filteredData[2:])
                        
                        print (gameName + " " + saleDate + " " + saleDuration)
                        #append to Sale History key
                        steamspyJson[gameID]['Sale History'].append({saleDate: saleDuration})
            
            done += 1
    #output results to json
    with open('data.json', 'w') as outfile:
        json.dump(steamspyJson, outfile)