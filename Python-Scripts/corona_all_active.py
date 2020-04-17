#! /usr/bin/python3

import requests
import lxml.html as lh
import matplotlib.pyplot as plt
import numpy as np
import csv
import pandas as pd

source = requests.get("https://www.worldometers.info/coronavirus/")
doc = lh.fromstring(source.content)
tr_elements = doc.xpath('//tr')
Active_Map={}
i=0
# Since out first row is the header, data is stored on the second row onwards
for j in range(1, int(len(tr_elements)/2)):
    # T is our j'th row
    T = tr_elements[j]
    z=['World','Total:','','Africa','Oceania','South America','Asia','Europe','North America','Country,Other','Asia']
    try:
        if (T[0].text_content().replace('\n', "").strip() not in z):
            Active_Map[T[0].text_content()]=int(T[6].text_content().replace(',',""))
    except:
        pass

Active_Map.pop('World',None)
Active_Map.pop('Total:',None)
Active_Map.pop('\n\n',None)
Active_Map.pop('\nAfrica\n',None)
Active_Map.pop('\nOceania\n',None)
Active_Map.pop('\nSouth America\n',None)
Active_Map.pop('\nAsia\n',None)
Active_Map.pop('\nEurope\n',None)
Active_Map.pop('\nNorth America\n',None)
Active_Map=sorted(Active_Map.items(), key = lambda x : x[1],reverse=True)
Active_Map=dict(Active_Map)
try:
    with open('active.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rank','Country', 'Active Cases'])
        i=0
        for key, value in Active_Map.items():
            i=i+1
            writer.writerow([i,key, value])
except IOError:
    print("I/O error")

active=pd.read_csv('active.csv',index_col=[0,1,2],encoding = "ISO-8859-1")
active.to_html('active.html')
