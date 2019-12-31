# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#function to mimic excel right function
def right(s, amount):
    return s[-amount:]

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

os.chdir('/home/pi/Downloads/MarketPdf')

'''
if done by Google Vision
'''

#open ocr file to perform regex
f = open('output0.txt', 'r')
string1 = f.read()
string1 = str(string1)
#count n number of instances and keep last occurrence of "text: ". this is to extract the entire reciept information from the JSON file
s=string1.count('text:')
x = string1.replace('text:', '', s-1)
match = re.search('text:(.*$)', x)
string2 = match.group(1)
#replace the newline char with space. simplify the reg expression process
t = string2.replace('\\', '\n')
t1 = t.replace('\nn', '\n')
data = t1.replace('\n', ' ')
data = data.replace('"', '')

'''
if done by Tesseract
'''
#read text file from tesseract OCR in r
file = open('output.txt', mode='r')
#replace the newline char with space. simplify the reg expression process
data = file.read().replace('\n', ' ')




#Reciept Date
Recieptdate=re.search(r'[0-9][0-9][A-Z]{3}[0-9][0-9][0-9][0-9]', data)
Recieptdate = Recieptdate.group(0)
#split into list from pattern on reciept. every transaction ends in 'N F' or 'T'
data = re.split(' T |N F | NF ', data)
#regex to extract prices and append to list
prices = []
for i in range(len(data)):
    price = right(data[i], 7)
    price = str(price)
    price = price[price.find('$'):]
    price = price.strip()
    price = price.replace(' ', '.')
    price = price.replace('$', '')
    prices.append(price)
    
#remove empty elements from list    
prices = list(filter(None, prices))

############## Item Description ####################

#reducing text to get the first item of reciept 
firstitem = re.sub('[^A-Za-z:\d\s]', '', data[0])
firstitemlist = re.split('Store:[0-9][0-9] ', firstitem)
firstitem = re.sub('[^A-Za-z\s]', '', firstitemlist[1])
firstitem = firstitem.replace('lb', '')
firstitem = firstitem.rstrip()

items = []
#next items
for i in range(len(data)):
    item=re.sub('[^A-Za-z\s]', '', data[i])
    item=re.sub('[a-z]', '', item)
    item=item.lstrip()
    item=item.rstrip()
    items.append(item)

items.pop(len(items)-1)
items.pop(0)
items.insert(0, firstitem)

#Uploading the data to gsheets
os.chdir('/home/pi/Downloads')
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('glowing-thunder-261100-88aeecb27e6e.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("Cardenas_PO_History")
worksheet = wks.get_worksheet(0)

#date column
recieptdatecolumn = []
for i in range(len(prices)):
    if i<len(prices):
        recieptdatecolumn.append(Recieptdate)
    else:
        pass
    
#loop to enter all data    
for date in range(len(recieptdatecolumn)):
    if i<len(recieptdatecolumn):
        next_row = next_available_row(worksheet)
        worksheet.update_acell("A{}".format(next_row), recieptdatecolumn[date])    
        worksheet.update_acell("B{}".format(next_row), items[date])
        worksheet.update_acell("C{}".format(next_row), prices[date])
    else:
        pass
#close ocr file
file.close()
