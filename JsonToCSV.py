
import csv
import json
import datetime
import time

now = datetime.datetime.now()

with open("dataComplete.json") as fo:
    data = json.load(fo)

f = csv.writer(open("data.csv", "w+", encoding="utf-8"))

f.writerow(["name", 
            "score", 
            "developer", 
            "publisher", 
            "owners", 
            "players_forever", 
            "players_2weeks", 
            "score_ratio(+to-)", 
            "days_since_sale", 
            "average_days_per_sale", 
            "average_days_per_sale_variance"])

for dataSet in data.values():
    scoreRatio = float(dataSet["positive"]) / max(1.0, float(dataSet["negative"]))
    
    lastSaleEnd = None
    
    daysSinceSale = -1;
    averageDaysPerSale = 0
    
    daysPerSale = []
    
    try:
        previousStartDate = None
        for saleHistory in dataSet["sale_history"]:
            
            #the last sale for number of days since sale
            if (lastSaleEnd == None):
                lastSaleEnd = list(saleHistory.values())[0]
                
                lastSaleEnd = time.mktime(datetime.datetime.strptime(lastSaleEnd, "%Y-%m-%d").timetuple())
                lastSaleEnd = datetime.datetime.utcfromtimestamp(lastSaleEnd)
                
                daysSinceSale = (now - lastSaleEnd).days
                
            startDate = list(saleHistory.keys())[0]
            endDate = list(saleHistory.values())[0]
            
            #the last sale for number of days since sale
            if (lastSaleEnd == None):
                lastSaleEnd = endDate
                
                lastSaleEnd = time.mktime(datetime.datetime.strptime(lastSaleEnd, "%Y-%m-%d").timetuple())
                lastSaleEnd = datetime.datetime.utcfromtimestamp(lastSaleEnd)
                
                daysSinceSale = (now - lastSaleEnd).days
                
            #keep number of days between sales
            if (previousStartDate != None):
                daysPerSale.append((datetime.datetime.utcfromtimestamp(time.mktime(datetime.datetime.strptime(previousStartDate, "%Y-%m-%d").timetuple())) - 
                                   datetime.datetime.utcfromtimestamp(time.mktime(datetime.datetime.strptime(startDate, "%Y-%m-%d").timetuple()))).days)
            previousStartDate = startDate
        
        #sum of days between sales
        for timePerSale in daysPerSale:
            averageDaysPerSale += timePerSale
    except (KeyError):
        pass
      
    #mean of days between sales
    averageDaysPerSale = averageDaysPerSale / max(1, len(daysPerSale))
    
    #variance of days between sales
    daysPerSaleVariance = -1
    for timePerSale in daysPerSale:
        daysPerSaleVariance = (timePerSale - averageDaysPerSale)**2
    daysPerSaleVariance /= max(1, len(daysPerSale))
    
    print (dataSet["name"], startDate, endDate, daysSinceSale, averageDaysPerSale , daysPerSale)
    f.writerow([dataSet["name"],
                dataSet["score_rank"],
                dataSet["developer"],
                dataSet["publisher"],
                dataSet["owners"],
                dataSet["players_forever"],
                dataSet["players_2weeks"],
                "{0:.2f}".format(scoreRatio),
                "{0:.2f}".format(daysSinceSale),
                "{0:.2f}".format(averageDaysPerSale),
                "{0:.2f}".format(daysPerSaleVariance)
                ])