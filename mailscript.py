# -*- coding: utf-8 -*-
"""
Created on Thu Nov 05 10:41:20 2015

@author: akshayr
"""
import numpy as np
import pandas as pd
import smtplib
import time

day1 = pd.read_csv('cm05NOV2015bhav.csv', index_col=False, 
                  names=['SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TOTTRDVAL','TIMESTAMP','TOTALTRADES','ISIN'], 
                header=0)

day2 = pd.read_csv('cm06NOV2015bhav.csv', index_col=False, 
                  names=['SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TOTTRDVAL','TIMESTAMP','TOTALTRADES','ISIN'], 
                header=0)                

merge = pd.merge(day1, day2, how='outer', on=['SYMBOL', 'SERIES'],suffixes=('_day1', '_day2'))
merge = merge[(merge.SERIES == 'EQ')]
merge = merge.fillna(0)
merge['Volume Decision UP'] = np.where(merge['TOTTRDVAL_day2'] >2.5*( merge['TOTTRDVAL_day1']), 'Volume Increase 2.5X', '')
merge['Volume Decision DOWN'] = np.where(merge['TOTTRDVAL_day2'] <0.4*( merge['TOTTRDVAL_day1']), 'Volume Decrease 2.5X', '')
merge['Price Decision UP'] = np.where(merge['CLOSE_day2'] >1.05*( merge['CLOSE_day1']), 'Price Increase 5%', '')
merge['Price Decision DOWN'] = np.where(merge['CLOSE_day2'] <0.95*( merge['CLOSE_day1']), 'Price Decrease 5%', '')
merge.to_csv('result.csv')


voluppriceup= merge[merge['Volume Decision UP'].isin(['Volume Increase 2.5X']) & merge['Price Decision UP'].isin(['Price Increase 5%'])] 
voluppricedw= merge[merge['Volume Decision UP'].isin(['Volume Increase 2.5X']) & merge['Price Decision DOWN'].isin(['Price Decrease 5%'])] 
voldwpriceup= merge[merge['Volume Decision DOWN'].isin(['Volume Decrease 2.5X']) & merge['Price Decision UP'].isin(['Price Increase 5%'])] 
voldwpricedw= merge[merge['Volume Decision DOWN'].isin(['Volume Decrease 2.5X']) & merge['Price Decision DOWN'].isin(['Price Decrease 5%'])] 

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

vuputext = "Price Up–Volume Up. View stocks where the price, volumes and delivery volumes have increased for 2 consecutive days. This indicates bullishness in the share as not only the price is moving up but also the volumes as well as the delivery volumes are increasing every day showing higher investor interest in it."
vupusym = voluppriceup[['SYMBOL','SERIES']].to_string()

vupdtext = "Price Down–Volume Up. In a down trend Signals a Change in trend & in Up trends it signals crisis and panic selling"
vupdsym = voluppricedw[['SYMBOL','SERIES']].to_string()

vdputext = "Price Up-Volume Down. In uptrebds this gives bearish signals as no volume support. In downtrends signals continuation of downtrend "
vdpusym = voldwpriceup[['SYMBOL','SERIES']].to_string()

vdpdtext = "Price Down–Volume Down. View stocks where the price, volumes and delivery volumes have decreased for 2 consecutive days. This indicates bearishness in the share as not only the price is moving down but also the volumes as well as the delivery volumes are decreasing every day showing lower investor interest in it."
vdpdsym = voldwpricedw[['SYMBOL','SERIES']].to_string()

from cStringIO import StringIO
buf1 = StringIO()
buf2 = StringIO()
buf3 = StringIO()
buf4 = StringIO()

buf1.write(vuputext)
buf1.write('\n')
buf1.write(vupusym)
buf1.write('\n')
buf1.write('\n')

buf2.write(vupdtext)
buf2.write('\n')
buf2.write(vupdsym)
buf2.write('\n')
buf2.write('\n')

buf3.write(vdputext)
buf3.write('\n')
buf3.write(vdpusym)
buf3.write('\n')
buf3.write('\n')

buf4.write(vdpdtext)
buf4.write('\n')
buf4.write(vdpdsym)
buf4.write('\n')
buf4.write('\n')
buf4.write('~~')
buf4.write('Ambit Capital Quantitative Desk')

sender = "roteakshay9@gmail.com"
recipients = ['akshay.rote@gmail.com', 'akshayrote@ambitcapital.com']
msg = MIMEMultipart('alternative')
msg['Subject'] = "Price Volume Calls for " + time.strftime("%c")
msg['From'] = sender
msg['To'] = ", ".join(recipients)

msg = """From: Ambit Python <roteakshay9@gmail.com>
To: Akshay Rote <akshay.rote@gmail.com>
Subject: Price Volume Calls for Today
""" + buf1.getvalue() + buf2.getvalue() + buf3.getvalue() + buf4.getvalue()


username = 'roteakshay9@gmail.com'
password = '****'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(sender, recipients, msg)
server.quit()        
print("Success")
