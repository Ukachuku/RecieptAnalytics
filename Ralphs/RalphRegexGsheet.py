# -*- coding: utf-8 -*-
"""
Created on Tue Dec 24 16:34:36 2019

@author: Enrique
"""

import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from itertools import chain

#function to mimic excel right function
def right(s, amount):
    return s[-amount:]

#function to find next available row in google sheet
def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

os.chdir('//home//pi//Downloads//MarketPdf')

#read text file from tesseract OCR in r
file = open('output.txt', mode='r')
#replace the newline char with space. simplify the reg expression process
#data = file.read().replace('\n', ' ')
data = file.read()
data = re.sub('\n', ' ', data)
#should not be any commas in reciept regardless of store. this will fix any ocr errors that misplaced period for a comma
data = re.sub(pattern=',', repl='.', string=data)

#Reciept Date
Recieptdate=re.search(r'[0-9][0-9]/[0-9][0-9]/[0-9][0-9]', data)
Recieptdate = Recieptdate.group(0)

#split into list from pattern on reciept. every transaction ends in 'N F' or 'T'
data = re.split(' F ', data)

#regex to extract prices and append to list
prices = []
for i in range(len(data)):
    price = right(data[i], 5)
    price = str(price)
    price = price.replace(' ', '')
    price = re.findall('[0-9]\.[0-9][0-9]|[0-9][0-9]\.[0-9][0-9]', price)
    prices.append(price)
    
#remove empty elements from list    
prices = list(filter(None, prices))

#unlist results
prices=list(chain.from_iterable(prices))

#----------------------------------------------------------------------Items----------------------------------------------------------

#reducing text to get the first item of reciept 
firstitem = re.split('VERIFIED TOTAL SAVINGS', string=data[0].upper())
firstitem = re.sub('[^A-Za-z\s]', '', firstitem[1])
firstitem = firstitem.replace('lb', '')
firstitem = firstitem.rstrip()
firstitem = firstitem.lstrip()

items = []
#next items
for i in range(len(data)):
    item=re.split('RALPHS SAVED YOU', string=data[i].upper())
    if len(item) > 1:
        item=re.sub(r'[^A-Z\s]+', '', item[len(item)-1])
        item=re.sub(r'\b[A-Z]\b', '', item)
        item=re.sub(r'\b[A-Z][A-Z]\b', '', item)
        item=item.lstrip()
        item=item.rstrip()
        items.append(item)
    else:
        item=re.sub(r'[^A-Z\s]+', '', item[0])
        item=re.sub(r'\b[A-Z]\b', '', item)
        item=re.sub(r'\b[A-Z][A-Z]\b', '', item)
        item=item.lstrip()
        item=item.rstrip()
        items.append(item)

items.pop(len(items)-1)
items.pop(0)
items.insert(0, firstitem)
items = list(filter(None, items))

try:
    if len(prices) == len(items):
        #Uploading the data to gsheets
        os.chdir('//home//pi//Downloads')
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('glowing-thunder-261100-88aeecb27e6e.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open("Ralphs_PO_History")
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
    else:
        raise(KeyboardInterrupt)
except:
    os.chdir('//home//pi//Downloads//MarketPdf')
    o = '\n'.join(items)
    p = '\n'.join(prices)
    erroroutput = '{}\n{}\n{}\n{}'.format(o, p, str(len(items)), str(len(prices)))
    error = open('error.txt', mode='w')
    error.write(erroroutput)
    error.close()
    print('Error: mismatch of item & price list lengths. Check Marketpdf folder for error.txt file')