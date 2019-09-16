import csv
import random
import gspread
import datetime
import os
from oauth2client.service_account import ServiceAccountCredentials

#returns an array from a csv file
def writefromCSVFile(stringName):
    returnArray = []
    with open(stringName) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            returnArray.append(row)
    return returnArray

#inverts row and columns
def invertRowandColumn(stringName):
    returnArray = []
    with open(stringName) as csv_file:
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for row in csv_reader:
            returnArray.append(row)

    return(returnArray)

#gets rid of some unimportant data points
def trimData(dataset):
    returnArray = []

    for i in range(len(dataset[0])):
        if((dataset[0][i])[2:len(dataset[0][i]) - 1] != '[deleted]'):
            returnArray.append((dataset[0][i])[2:len(dataset[0][i]) - 1])

    return returnArray

#takes an array and outputs into csvfile
def writeToNewCSVFile(filename, inputArray, orientation):
    with open(filename, mode = 'w') as csv_file:
        thewriter = csv.writer(csv_file, quoting=csv.QUOTE_ALL)
        if(orientation):
            for i in range(len(inputArray)):
                thewriter.writerow([inputArray[i]])
        else:
            thewriter.writerow(inputArray)

def generateSubsetArray(data, amount):
    returnArray = []

    allIndex = list(range(0,len(data)))
    count1 = 0
    count2 = 0

    while(len(returnArray) <= amount):
        randomIndex = random.randint(0,len(allIndex) - 1)
        randomI = allIndex[randomIndex]
        if(data[randomI][0] == '0'):
            if(count1 <= amount / 2):
                count1 += 1
                returnArray.append([data[randomI][0],data[randomI][5]])
        elif(data[randomI][0] == '4'):
            if(count2 <= amount / 2):
                count2 += 1
                returnArray.append([data[randomI][0],data[randomI][5]])
        del allIndex[randomIndex]

    return returnArray

def uploadToGoogleSheets(data_seq_x, data_seq_y, testNumber, sheetName):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    column = 1

    counter = 0
    if(sheetName == 'Bitcoin'):
        counter = 2
    elif(sheetName == 'Donald Trump'):
        counter = 0
    elif(sheetName == 'Golden State Warriors'):
        counter == 1
    worksheet = client.open("Sentiment Analysis Version 1.0 Data").get_worksheet(counter)
    #worksheet = client.open("Sentiment Analysis Version 1.0 Data")(sheetName)

    while(worksheet.cell(column,2).value != ''):
        column += 1

    count = [0,0,0,0]
    for i in range(len(data_seq_y)):
        if(data_seq_y[i] < .45):
            count[0] += 1
        elif(data_seq_y[i] < .55):
            count[1] += 1
        elif(data_seq_y[i] < 1):
            count[2] += 1
        else:
            count[3] += 1


    worksheet.update_acell('B1','Positive')
    worksheet.update_acell('C1','Neutral')
    worksheet.update_acell('D1','Negative')
    worksheet.update_acell('E1','Unlabeled')

    countCategory = [0,0,0,0]

    if(column == 1):
        column += 1

    date = datetime.datetime.today()
    dateString = (str(date.month) + '-' + str(date.day) + '-' + str(date.year))
    worksheet.update_acell('B' + str(column),count[0])
    worksheet.update_acell('C' + str(column),count[1])
    worksheet.update_acell('D' + str(column),count[2])
    worksheet.update_acell('E' + str(column),count[3])
    worksheet.update_acell('A' + str(column),dateString)


    stringDir = 'C:\\Users\\ethan\\Dropbox\\Ethan\'s Programs\\TensorFlow Test\\Machine Learning Testing\\Test Twitter Sentiment Analysis\\All Twitter Data\\'

    data_seq = []

    data_seq.append(data_seq_x)
    data_seq.append(data_seq_y)

    writeToNewCSVFile(stringDir + dateString + "- test number" + str(testNumber), data_seq, False)
    #worksheet.update_cells(cell_list)
    #    cell.value = 'O_o'
