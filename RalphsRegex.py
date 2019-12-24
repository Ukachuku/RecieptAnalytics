import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from itertools import chain

#function to mimic excel right function
def right(s, amount):
    return s[-amount:]

os.chdir('//home//pi//Downloads//MarketPdf')

#read text file from tesseract OCR in r
file = open('output.txt', mode='r')

#replace the newline char with space. simplify the reg expression process
data = file.read().replace('\n', ' ')

#Reciept Date
#Recieptdate=re.search(r'[0-9][0-9]/[0-9][0-9]/[0-9][0-9]', data)
#Recieptdate = Recieptdate.group(0)

#should not be any commas in reciept regardless of store. this will fix any ocr errors that misplaced period for a comma
data = re.sub(pattern=',', repl='.', string=data)
#split into list from pattern on reciept. every transaction ends in 'N F' or 'T'
data = re.split(' F ', data)

#regex to extract prices and append to list
prices = []
for i in range(len(data)):
    price = right(data[i], 5)
    price = str(price)
    price = price.replace(' ', '')
    price = re.findall('[0-9].[0-9][0-9]|[0-9][0-9].[0-9][0-9]', price)
    prices.append(price)
    
#remove empty elements from list    
prices = list(filter(None, prices))

#unlist results
prices=list(chain.from_iterable(prices))

#----------------------------------------------------------------------Items----------------------------------------------------------

