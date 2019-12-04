import re
import os

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
# extract total number of items to later validate correct number of items
numberofitems = re.search('ITEMS [0-9][0-9]', r)
#remove the misc information on the reciept
itemsprice = re.search('DAILY(.*)ITEMS', r)
itemsprice = itemsprice.group(1)
itemsprice = itemsprice.split('  ')
#remove OZ description
regex = re.compile(r'/OZ$')
masterlist = list(filter(lambda i: not regex.search(i), itemsprice))
#get description of items
itemsregex = re.compile(r'[0-9][0-9].[0-9][0-9]|[0-9].[0-9][0-9]|TOTAL|CASH|STATE TAX|SUBTOTAL')
itemslist = list(filter(lambda i: not itemsregex.search(i), masterlist))




outputregex = open('outputregex.txt', 'w')

outputregex.write(t1)
outputregex.close