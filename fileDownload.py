# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 12:06:32 2015

@author: akshayr

Downloads the CM and FO Bhavcopy files from the NSE website and unzips and store
at the reuired directory
"""
import time
import requests
from datetime import datetime

if time.strftime("%X") >= "17:00:00":
    part3 = datetime.today().day
else:
    part3 = datetime.today().day - 1    

part3 = str(part3)
part1 = 'http://www.nseindia.com/content/historical/EQUITIES/2015/NOV/' #starturl
part2 = time.strftime("cm") 
part4 = time.strftime("%b").upper()
part5 = time.strftime("%Ybhav.csv.zip")

urlcm = part1+part2+part3+part4+part5
foldernamecm = part2+part3+part4+part5
print 'Downloading from... '+urlcm
r = requests.get(urlcm)
with open(foldernamecm, "wb") as code:
    code.write(r.content)
print foldernamecm+':CM Bhavcopy file downloaded'

print 'Extracing CM Bhavcopy Zip File...'
import zipfile
with zipfile.ZipFile(foldernamecm, "r") as z:
    z.extractall("E:\\Akshay\\Work\\pythonFinance")
print foldernamecm+':CM Bhavcopy CSV extracted'

#http://www.nseindia.com/content/historical/DERIVATIVES/2015/NOV/fo18NOV2015bhav.csv.zip
if time.strftime("%X") >= "17:00:00":
    part3 = datetime.today().day
else:
    part3 = datetime.today().day - 1    

part3 = str(part3)
part1 = 'http://www.nseindia.com/content/historical/DERIVATIVES/2015/NOV/' #starturl
part2 = time.strftime("fo") 
part4 = time.strftime("%b").upper()
part5 = time.strftime("%Ybhav.csv.zip")

urlfo = part1+part2+part3+part4+part5
foldernamefo = part2+part3+part4+part5
print 'Downloading from... '+urlfo
r = requests.get(urlfo)
with open(foldernamefo, "wb") as code:
    code.write(r.content)
print foldernamefo+':FO Bhavcopy file downloaded'

print 'Extracing FO Bhavcopy Zip File...'
import zipfile
with zipfile.ZipFile(foldernamefo, "r") as z:
    z.extractall("E:\\Akshay\\Work\\pythonFinance")
print foldernamefo+':FO Bhavcopy CSV extracted'

