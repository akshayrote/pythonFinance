# -*- coding: utf-8 -*-
"""
Created on Thu Nov 05 12:12:23 2015

@author: akshayr
"""

import smtplib

sender = 'aks_1103@yahoo.co.in'
receivers = ['akshay.rote@gmail.com']

message = """From: Ambit Python <aks_1103@yahoo.co.in>
To: Akshay Rote <akshay.rote@gmail.com>
Subject: Mail from Python Client

This is a test e-mail message.
"""


username = 'aks_1103@yahoo.co.in'
password = '*****'
server = smtplib.SMTP("smtp.mail.yahoo.com",587)
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(sender, receivers, message)
server.quit()        
print("Success")