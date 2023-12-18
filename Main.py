import urllib.parse
import urllib.request
import json
import csv
import time
import matplotlib.pyplot as plt
import pandas as pd

#constants
API_KEY="NCF8XJDWE767RMKB22MN36U9Q"
UNIT_GROUP="us"

# this interfaces with the API to retrieve data
def getWeatherForecast(loc, date):
         requestUrl = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/" + urllib.parse.quote_plus(loc)
         requestUrl = requestUrl+date+"?key="+API_KEY+"&unitGroup="+UNIT_GROUP+"&include=days";
         
         #print('Weather requestUrl={requestUrl}'.format(requestUrl=requestUrl))
         try:
                 req = urllib.request.urlopen(requestUrl)
         except:
                 print("Could not read from:"+requestUrl);
                 return []
                
         rawForecastData = req.read()
         req.close()
         return json.loads(rawForecastData)

# this checks to see if this entry already exists in the csv file
def inside(areacode, date_clean, outages):
    with open('Clean_Full.csv', 'r+', newline='') as f:
        line = csv.reader(f)

        try:   
            for i in line:
                if str(areacode) == str(i[0]) and str(date_clean) == str(i[1]) and str(outages) == str(i[2]):
                    print("found record")
                    return True
        except:
            print("csv is empty")
            return False
    print("record not found")
    return False

# function to write a line into the csv
def write_line(data):
    with open('Clean_Full.csv', 'a', newline='') as f:
        file = csv.writer(f)
        file.writerow(data)


with open('Clean.csv', 'rt') as f:
    line = csv.reader(f)
    for i in line:
        # for ease of use
        areacode = i[0]
        date = i[1]
        outages = i[2]

        # if not in the csv -> retrieve data and write line into csv
        if not inside(areacode, date, outages):
            location= "Maryland," + str(areacode)    
            weatherForecast = getWeatherForecast(location, date)
            
            print('Weather forecast for {location}'.format(location=weatherForecast['resolvedAddress']))
            days = weatherForecast['days']
            for day in days:
                data = [i[0], i[1], i[2], day["tempmax"], day["tempmin"], day["description"], day["conditions"], day["windspeed"], day["windgust"], day["snowdepth"], day["precip"]]
                write_line(data)
                print("wrote data")
                #print('{datetime} tempmax:{tempmax} tempmin:{tempmin} description:{description} conditions:{conditions} windspeed:{windspeed} windgust:{windgust} snowdepth:{snowdepth} precip:{precip}'.format(datetime=day['datetime'], tempmax=day["tempmax"], tempmin=day["tempmin"], description=day["description"], conditions=day["conditions"], windspeed=day["windspeed"], windgust=day["windgust"], snowdepth=day["snowdepth"], precip=day["precip"]))

print("done")










