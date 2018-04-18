'''
Converts json to csv time series. Result can be seen in dataTimeseries.csv
'''
import csv
import json
import datetime
import time
from string import digits

now = datetime.datetime.now()

with open("dataComplete1.json") as fo:
    data = json.load(fo)

f = csv.writer(open("data.csv", "w+", encoding="utf-8"))

f.writerow(["month",
            "year",
            "name",
            "developer", 
            "publisher",  
            "days_since_sale", 
            "average_days_per_sale", 
            "average_days_per_sale_variance",
            "months_since_release",
            "sale"])

removedGames = 0

for dataSet in data.values():
    
    lastSaleEnd = None
    
    daysSinceSale = -1
    averageDaysPerSale = -1
    daysPerSaleVariance = -1
    
    daysPerSale = []
    
    try:
        previousStartDate = None
        for saleHistory in dataSet["Sale History"]:
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
    for timePerSale in daysPerSale:
        daysPerSaleVariance = (timePerSale - averageDaysPerSale)**2
    daysPerSaleVariance /= max(1, len(daysPerSale))
    
    #print (dataSet["name"], daysSinceSale, averageDaysPerSale , daysPerSaleVariance)
    
    try:
        releaseDate = datetime.datetime.utcfromtimestamp(time.mktime(datetime.datetime.strptime(dataSet["release_date"].lstrip(digits).lstrip().replace(",", ""), '%b %Y').timetuple()))
    except (KeyError):
        removedGames += 1
        continue;
    except (ValueError):
        removedGames += 1
        continue;
    
    monthsSinceRelease = 0
    for year in range(releaseDate.year, now.year + 1):
        for month in range(1, 13):
            if (month < releaseDate.month and releaseDate.year == year):
                continue;
        
            #stop at current month
            if (now.year == year and now.month == month):
                break;
            
            added = False
            try:
                for saleHistory in dataSet["Sale History"]:
                    startDate = list(saleHistory.keys())[0]
                    utcStartDate = datetime.datetime.utcfromtimestamp(time.mktime(datetime.datetime.strptime(startDate, "%Y-%m-%d").timetuple()))
                    
                    endDate = list(saleHistory.values())[0]
                    utcEndDate = datetime.datetime.utcfromtimestamp(time.mktime(datetime.datetime.strptime(endDate, "%Y-%m-%d").timetuple()))
                    
                    
                    if ((utcStartDate.month <= month and utcStartDate.year == year and
                        month <= utcEndDate.month and utcEndDate.year == year)) or \
                        (utcEndDate.year == utcStartDate.year + 1 and #solves problem case where sale goes into next year
                        ((utcEndDate.month == month and utcEndDate.year == year) or \
                         (utcStartDate.month == month and utcStartDate.year == year))):
                        f.writerow([month,
                                    year,
                                    dataSet["name"],
                                    dataSet["developer"],
                                    dataSet["publisher"],
                                    "{0:.2f}".format(daysSinceSale),
                                    "{0:.2f}".format(averageDaysPerSale),
                                    "{0:.2f}".format(daysPerSaleVariance),
                                    monthsSinceRelease,
                                    1
                                    ])
                        added = True
                        break;
            except (KeyError):
                pass
            if not added:
                f.writerow([
                            month,
                            year,
                            dataSet["name"],
                            dataSet["developer"],
                            dataSet["publisher"],
                            "{0:.2f}".format(daysSinceSale),
                            "{0:.2f}".format(averageDaysPerSale),
                            "{0:.2f}".format(daysPerSaleVariance),
                            monthsSinceRelease,
                            0
                            ])
                
            monthsSinceRelease += 1
            
print ("omitted ", removedGames)