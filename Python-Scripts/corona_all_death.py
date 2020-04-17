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
Deaths_Map={}
i=0
# Since out first row is the header, data is stored on the second row onwards
for j in range(1, int(len(tr_elements)/2)):
    # T is our j'th row
    T = tr_elements[j]
    z=['World','Total:','','Africa','Oceania','South America','Asia','Europe','North America','Country,Other','Asia']
    try:
        if (T[0].text_content().replace('\n', "").strip() not in z):
            Deaths_Map[T[0].text_content()]=int(T[3].text_content().replace(',',""))
    except:
        pass

Deaths_Map=sorted(Deaths_Map.items(), key = lambda x : x[1],reverse=True)
Deaths_Map=dict(Deaths_Map)
try:
    with open('death.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Rank','Country', 'Deaths'])
        i=0
        for key, value in Deaths_Map.items():
            i=i+1
            writer.writerow([i,key, value])
except IOError:
    print("I/O error")

active=pd.read_csv('death.csv',index_col=[0,1,2],encoding = "ISO-8859-1")
active.to_html('death.html')
