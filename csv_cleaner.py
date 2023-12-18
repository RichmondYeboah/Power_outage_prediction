import matplotlib.pyplot as plt
import pandas as pd
import csv

# checks if the record already exists
def inside(areacode, date_clean, outages):
    with open('Clean.csv', 'r+', newline='') as f:
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

#writes a line into the csv
def write_line(data):
    with open('Clean.csv', 'a', newline='') as f:
        file = csv.writer(f)
        file.writerow(data)



with open('Power_Outages_-_Zipcode2.csv', 'rt') as f:
    line = csv.reader(f)
    for i in line:
        areacode = int(i[1])
        outages = int(i[2])

        # reformatting date into version used by API
        date_raw = i[3]
        buffer = date_raw.split('/')
        buffer2 = buffer[2].split(' ')
        date_clean = "/"+buffer2[0]+"-"+buffer[0]+"-"+buffer[1]+"/"
        

        # was going to add API connection here. thought better of it and made that into the Main.py
        # this only takes the Zipcode file and cleans it a bit.
        # also need to delete the first line of the Zipcode csv file for this to work.
        #I could have coded a workaround but its too early in the morning and its just easier this way
        data_partial = [areacode, date_clean, outages]
        print(data_partial)
        if outages > 4:
            if not inside(areacode, date_clean, outages):
                print("writing data")
                write_line(data_partial)
                
    
print("done")

