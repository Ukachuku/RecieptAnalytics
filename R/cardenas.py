import pandas as pd
import os
import re

#function to mimic excel right function
def right(s, amount):
    return s[-amount:]

os.chdir('\home\pi\OCR')

#read text file from tesseract OCR in r
file = open('output.txt', mode='r')
#replace the newline char with space. simplify the reg expression process
data = file.read().replace('\n', ' ')
#split into list from pattern on reciept. every transaction ends in 'N F' or 'T'
data = re.split(' T |N F', data)
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
