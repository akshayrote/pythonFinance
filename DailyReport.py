# -*- coding: utf-8 -*-
"""
Created on Mon Nov 09 11:40:35 2015

@author: akshayr
"""
import numpy as np
import pandas as pd
import smtplib
import time

#Day 1 CM Bhavcopy
cmday1 = pd.read_csv('cm05NOV2015bhav.csv', index_col=False, 
                  names=['SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TOTTRDVAL','TIMESTAMP','TOTALTRADES','ISIN'], 
                header=0)

#Day 2 CM Bhavcopy
cmday2 = pd.read_csv('cm06NOV2015bhav.csv', index_col=False, 
                  names=['SYMBOL','SERIES','OPEN','HIGH','LOW','CLOSE','LAST','PREVCLOSE','TOTTRDQTY','TOTTRDVAL','TIMESTAMP','TOTALTRADES','ISIN'], 
                header=0)                

#Day 2 FO bhavcopy
foday2= pd.read_csv('fo06NOV2015bhav.csv', index_col=False, 
                  names=['INSTRUMENT','SYMBOL','EXPIRY_DT','STRIKE_PR','OPTION_TYP','OPEN','HIGH','LOW','CLOSE','SETTLE_PR','CONTRACTS','VAL_INLAKH','OPEN_INT','CHG_IN_OI','TIMESTAMP'],
                header=0)

#Merging CMDay 1 and CMDay 2 bhavcopy Data
mergecm = pd.merge(cmday1, cmday2, how='outer', on=['SYMBOL', 'SERIES'],suffixes=('_day1', '_day2'))

#Merging CM Day 2 and FO Day 2 bhavcopy Data
mergecmfo = pd.merge(cmday2, foday2, how='outer', on=['SYMBOL'],suffixes=('_day2cm', '_day2fo'))

#Considering only EQ Series
mergecm = mergecm[(mergecm.SERIES == 'EQ')]
mergecmfo = mergecmfo[(mergecmfo.SERIES == 'EQ')]

#Filling null values with 0
mergecm = mergecm.fillna(0)
mergecmfo = mergecmfo.fillna(0)
#Converting Column data type to date
mergecmfo['EXPIRY_DT'] = pd.to_datetime(mergecmfo['EXPIRY_DT'])
mergecmfo['TIMESTAMP_day2cm'] = pd.to_datetime(mergecmfo['TIMESTAMP_day2cm'])
mergecmfo['TIMESTAMP_day2fo'] = pd.to_datetime(mergecmfo['TIMESTAMP_day2fo'])

#Neglecting Illiquid Scrips
mergecm = mergecm[mergecm.TOTTRDQTY_day1 != 0]
mergecm = mergecm[mergecm.TOTTRDQTY_day2 != 0]

#Neglecting non derivative Scrips
mergecmfo = mergecmfo[mergecmfo.INSTRUMENT != 0]

#Selecting only Future Scrips
mergecmf = mergecmfo[mergecmfo.INSTRUMENT == 'FUTSTK']

#Selecting only Option Scrips
mergecmo = mergecmfo[mergecmfo.INSTRUMENT == 'OPTSTK']

#Calculations
#Actual Basis = (Fut Px-Spot Px)/Fut Px
mergecmf['ACTUAL BASIS'] = ((mergecmf.SETTLE_PR - mergecmf.CLOSE_day2cm)/mergecmf.SETTLE_PR)
mergecmf['ACTUAL BASIS %'] = (((mergecmf.SETTLE_PR - mergecmf.CLOSE_day2cm)/mergecmf.SETTLE_PR)*100)
mergecmf['DAYS TO EXPIRE'] = mergecmf['EXPIRY_DT'] - mergecmf['TIMESTAMP_day2cm']
mergecmf['DAYS TO EXPIRE'] = (mergecmf['DAYS TO EXPIRE'] / np.timedelta64(1, 'D')).astype(int)
#Continously compounded Future Value with Risk Free Rate = 7%
mergecmf['FV'] = mergecmf['CLOSE_day2cm']*(pow(2.71,((mergecmf['DAYS TO EXPIRE']/365)*0.07)))
#Risk Free Arbitrage Basis
mergecmf['ARBITRAGE BASIS'] = ((mergecmf.SETTLE_PR - mergecmf.FV)/mergecmf.SETTLE_PR)
mergecmf['ARBITRAGE BASIS %'] = (((mergecmf.SETTLE_PR - mergecmf.FV)/mergecmf.SETTLE_PR)*100)
#Selcting the Monthwise Future Contracts
mergecmfnear = mergecmf[mergecmf.EXPIRY_DT == '26-Nov-2015']
cfarbnear = mergecmfnear.sort(['ARBITRAGE BASIS %'],ascending=False).head(n=5)
mergecmfmiddle = mergecmf[mergecmf.EXPIRY_DT == '31-Dec-2015']
cfarbmiddle = mergecmfmiddle.sort(['ARBITRAGE BASIS %'],ascending=False).head(n=5)
mergecmffar = mergecmf[mergecmf.EXPIRY_DT == '28-Jan-2016']
cfarbfar = mergecmffar.sort(['ARBITRAGE BASIS %'],ascending=False).head(n=5)

#Volume Price Relationships
mergecm['Volume Decision UP'] = np.where(mergecm['TOTTRDVAL_day2'] >2.5*( mergecm['TOTTRDVAL_day1']), 'Volume Increase 2.5X', '')
mergecm['Volume Decision DOWN'] = np.where(mergecm['TOTTRDVAL_day2'] <0.4*( mergecm['TOTTRDVAL_day1']), 'Volume Decrease 2.5X', '')
mergecm['Price Decision UP'] = np.where(mergecm['CLOSE_day2'] >1.05*( mergecm['CLOSE_day1']), 'Price Increase 5%', '')
mergecm['Price Decision DOWN'] = np.where(mergecm['CLOSE_day2'] <0.95*( mergecm['CLOSE_day1']), 'Price Decrease 5%', '')

voluppriceup= mergecm[mergecm['Volume Decision UP'].isin(['Volume Increase 2.5X']) & mergecm['Price Decision UP'].isin(['Price Increase 5%'])] 
voluppricedw= mergecm[mergecm['Volume Decision UP'].isin(['Volume Increase 2.5X']) & mergecm['Price Decision DOWN'].isin(['Price Decrease 5%'])] 
voldwpriceup= mergecm[mergecm['Volume Decision DOWN'].isin(['Volume Decrease 2.5X']) & mergecm['Price Decision UP'].isin(['Price Increase 5%'])] 
voldwpricedw= mergecm[mergecm['Volume Decision DOWN'].isin(['Volume Decrease 2.5X']) & mergecm['Price Decision DOWN'].isin(['Price Decrease 5%'])] 

#Scrips with Most % change in Prices
mergecm['Change']=((mergecm.CLOSE_day2 - mergecm.CLOSE_day1)/mergecm.CLOSE_day1)*100
priceshocker = mergecm.sort(['Change'], ascending=False).head(n=5)

#Scrips with Highest Traded Value/Turnover/Most Active
mostactive = mergecm.sort(['TOTTRDVAL_day2'], ascending=False).head(n=5)

vuputext = "Price Up–Volume Up. In uptrends Bullish Scrips with support & In a down trend this signals a possible correction or change in the trend’s short term direction to upwards"
vupusym = voluppriceup[['SYMBOL','SERIES']].to_string()

vupdtext = "Price Down–Volume Up. In a down trend Signals a Change in trend & in Up trends it signals crisis and panic selling"
vupdsym = voluppricedw[['SYMBOL','SERIES']].to_string()

vdputext = "Price Up-Volume Down. In uptrebds this gives bearish signals as no volume support. In downtrends signals continuation of downtrend "
vdpusym = voldwpriceup[['SYMBOL','SERIES']].to_string()

vdpdtext = "Price Down–Volume Down. Suggests a continuation of the main down trend, or a pull back and possible continuation of an uptrend"
vdpdsym = voldwpricedw[['SYMBOL','SERIES']].to_string()

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = "roteakshay9@gmail.com"
recipients = ['akshay.rote@gmail.com']
msg = MIMEMultipart('alternative')
msg['Subject'] = "Cash Future Arbitrage Calls " + time.strftime("%c")
msg['From'] = sender
msg['To'] = ", ".join(recipients)

text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org"
html = cfarbnear[['SYMBOL','ARBITRAGE BASIS %']].to_html()

part1 = MIMEText(html, 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)

username = 'roteakshay9@gmail.com'
password = '****'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(sender, recipients, msg.as_string())
server.quit()        
print("Success")
