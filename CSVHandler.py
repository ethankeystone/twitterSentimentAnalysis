import csv
import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

def writeToNewCSVFile(filename, inputArray):
    with open(filename, mode = 'w') as csv_file:
        thewriter = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        print(len(inputArray))
        thewriter.writerow([inputArray])
        thewriter.writerow([inputArray])
