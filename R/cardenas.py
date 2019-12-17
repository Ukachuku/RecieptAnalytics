import pandas as pd
import os
import re

def right(s, amount):
    return s[-amount:]


os.chdir('\home\pi\OCR')

file = open('output.txt', mode='r')
#replace the newline char with space. simplify the reg expression process
data = file.read().replace('\n', ' ')
data = re.split(' T |N F', data)

prices = []
for i in range(len(data)):
    price = right(data[i], 7)
    price = str(price)
    price = price[price.find('$'):]
    price = price.strip()
    price = price.replace(' ', '.')
    prices.append(price)
