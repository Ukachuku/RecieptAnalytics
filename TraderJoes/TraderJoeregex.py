import re
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def next_available_row(worksheet):
    str_list = list(filter(None, worksheet.col_values(1)))
    return str(len(str_list)+1)


os.chdir('/home/pi/gcloudstuff')
#open ocr file to perform regex
f = open('output.txt', 'rb')
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
r = t1.replace('\n', ' ')
#date of reciept
recieptdate = re.search(r'[0-9][0-9]-[0-9][0-9]-[0-9][0-9][0-9][0-9]', r)
recieptdate = recieptdate.group(0)
#remove the misc information on the reciept
itemsprice = re.search('DAILY(.*)ITEMS', r)
itemsprice = itemsprice.group(1)
itemsprice = itemsprice.split('  ')
#remove OZ description
regex = re.compile(r'/OZ$')
masterlist = list(filter(lambda i: not regex.search(i), itemsprice))
masterlist = list(filter(None, masterlist))
#get description of items
itemsregex = re.compile(r'[0-9][0-9].[0-9][0-9]|[0-9].[0-9][0-9]|TOTAL|CASH|STATE TAX|SUBTOTAL')
itemslist = list(filter(lambda i: not itemsregex.search(i), masterlist))
#get price of items
priceregex = re.compile(r'[a-zA-Z]')
pricelist = list(filter(lambda i: not priceregex.search(i), masterlist))
value = pricelist.pop(len(pricelist)-1)
value = pricelist.pop(len(pricelist)-1)
value = pricelist.pop(len(pricelist)-1)

#upload data into google sheet
os.chdir('/home/pi/Downloads')
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('glowing-thunder-261100-88aeecb27e6e.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("Trader Joe's PO History")
worksheet = wks.get_worksheet(0)
#date column
recieptdatecolumn = []
for i in range(len(pricelist)):
    if i<len(pricelist):
        recieptdatecolumn.append(recieptdate)
    else:
        pass
#loop to enter all data    
for date in range(len(recieptdatecolumn)):
    if i<len(recieptdatecolumn):
        next_row = next_available_row(worksheet)
        worksheet.update_acell("A{}".format(next_row), recieptdatecolumn[date])    
        worksheet.update_acell("B{}".format(next_row), itemslist[date])
        worksheet.update_acell("C{}".format(next_row), pricelist[date])
    else:
        pass
#close ocr file
f.close()
