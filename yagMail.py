# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 14:46:37 2015

@author: akshayr
"""
import yagmail
#Binding thr Email and Password once
#yagmail.register('roteakshay9@gmail.com', '*****')
#starting the connection
yag = yagmail.SMTP('roteakshay9@gmail.com')

#Mail Parameters
to = 'akshay.rote@gmail.com'
to2 = 'akshayrote@ambitcapital.com'
subject = 'Yagmail Python Package Test'
body = 'Body of the Email'
html = '<a href="https://pypi.python.org/pypi/sky/">Click me!</a>'
csv = 'E:/Akshay/Work/pythonFinance/test.csv'
img = 'E:/Akshay/Work/pythonFinance/ambit.jpg'

yag.send(to = [to, to2], subject = subject, contents = [body, html, csv, img])