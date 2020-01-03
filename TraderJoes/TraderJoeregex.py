import re
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from itertools import chain

def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)

#function to mimic excel right function
def right(s, amount):
    return s[-amount:]

os.chdir('/home/pi/Downloads/MarketPdf')
'''
Tesseract OCR
'''
#read text file from tesseract OCR in r
file = open('output.txt', mode='r')
#replace the newline char with space. simplify the reg expression process
#data = file.read().replace('\n', ' ')
f = file.read()
#date of reciept
recieptdate = re.search(r'[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]', f)
recieptdate = recieptdate.group(0)
f = f.split('\n')

data=[]
#should not be any commas in reciept regardless of store. this will fix any ocr errors that misplaced period for a comma
for x in range(len(f)):
    nocomma = re.sub(pattern=',', repl='.', string=f[x])
    data.append(nocomma)

'''
Google Vision
'''

#open ocr file to perform regex
#f = open('output0.txt', 'rb')
#string1 = f.read()
#string1 = str(string1)
##count n number of instances and keep last occurrence of "text: ". this is to extract the entire reciept information from the JSON file
#s=string1.count('text:')
#x = string1.replace('text:', '', s-1)
#match = re.search('text:(.*$)', x)
#string2 = match.group(1)
##replace the newline char with space. simplify the reg expression process
#t = string2.replace('\\', '\n')
#t1 = t.replace('\nn', '\n')
#data = t1.replace('\n', ' ')






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

value = prices.pop(len(prices)-1)
value = prices.pop(len(prices)-1)
value = prices.pop(len(prices)-1)
value = prices.pop(len(prices)-1)

#----------------------------------------------------------------------Items----------------------------------------------------------

items = []
#next items
for i in range(len(data)):
        item=re.sub(r'[^A-Z\s]+', '', data[i])
        item=re.sub(r'\b[A-Z]\b', '', item)
        item=re.sub(r'\b[A-Z][A-Z]\b', '', item)
        item=item.lstrip()
        item=item.rstrip()
        items.append(item)

items = list(filter(None, items))
value = items.pop(len(items)-1)
value = items.pop(len(items)-1)
value = items.pop(len(items)-1)
value = items.pop(len(items)-1)
value = items.pop(len(items)-1)
value = items.pop(len(items)-1)
value = items.pop(0)
value = items.pop(0)

##remove the misc information on the reciept
#itemsprice = re.search('DAILY(.*)ITEMS', data)
#itemsprice = itemsprice.group(1)
#itemsprice = itemsprice.split('  ')
##remove OZ description
#regex = re.compile(r'/OZ$')
#masterlist = list(filter(lambda i: not regex.search(i), itemsprice))
#masterlist = list(filter(None, masterlist))
#get description of items
#itemsregex = re.compile(r'[0-9][0-9].[0-9][0-9]|[0-9].[0-9][0-9]|TOTAL|CASH|STATE TAX|SUBTOTAL')
#itemslist = list(filter(lambda i: not itemsregex.search(i), masterlist))
##get price of items
#priceregex = re.compile(r'[a-zA-Z]')
#pricelist = list(filter(lambda i: not priceregex.search(i), masterlist))
#value = pricelist.pop(len(pricelist)-1)
#value = pricelist.pop(len(pricelist)-1)
#value = pricelist.pop(len(pricelist)-1)

try:
    if len(prices) == len(items):
        #upload data into google sheet
        os.chdir('/home/pi/Downloads')
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name('glowing-thunder-261100-88aeecb27e6e.json', scope)
        gc = gspread.authorize(credentials)
        wks = gc.open("Trader Joe's PO History")
        worksheet = wks.get_worksheet(0)
        #date column
        recieptdatecolumn = []
        for i in range(len(prices)):
            if i<len(prices):
                recieptdatecolumn.append(recieptdate)
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