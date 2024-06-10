import datetime 
import calendar
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import xlwings as xw
import numpy as np
import schedule
import time
import pygsheets

import pytz
############################################################### #to add new items add new id to the end of id_onlyid###############################################################



#authorization
gc = pygsheets.authorize(service_file='C:/gSheets/osrs-flipping-76748898e2ed.json')
headers = {
  'User-Agent': "flipping tool - @betterjg#7132"
}  #user agent for wiki
url= 'http://prices.runescape.wiki/api/v1/'
gamemode = 'osrs'
endpoint = '/latest'
r = requests.get(url+gamemode+endpoint, headers=headers)
# Create empty dataframe
df = pd.DataFrame()
#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
sh = gc.open('OSRS Flipping10')   #10 is actual 49 is test
#select the first sheet 
wks = sh[0]

data=r.json()   #gets data as json
item_priceBuy=-1
item_priceSell =-1 
item_BuyTime=-1
item_SellTime=-1
#reading num of lines from csv file#
import csv

filename = 'id_onlyid.csv'

with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile)
    num = sum(1 for row in reader)
#reading csv into df2
df2 = pd.read_csv('id_onlyid.csv')

#cell_value = df2.iloc[0,0]   #example of how to read into [row,col]


#unix time to find seconds passed after last buy##########################
date = datetime.datetime.utcnow()                           #include current utc time
TIMENOW = calendar.timegm(date.utctimetuple())
            


#method
def show():
    temporary = []
    for j in range(len(df2)):
        temporary2 = df2["id"][j]
        temporary.append(temporary2)
    
    dataframe = pd.DataFrame(temporary)
    
    r = requests.get(url+gamemode+endpoint, headers=headers)
    data=r.json()
    itemBuy = []
    itemSell = []
    itemBTime =[]
    itemSTime=[]
    for i in range(num-1):
        date = datetime.datetime.utcnow()                           #include current utc time
        TIMENOW = calendar.timegm(date.utctimetuple())
        cell_value = df2.iloc[i,0]
        cell_value = str(cell_value).replace('.0', '')

        item_priceBuy = data['data'][cell_value]['high']
        itemBuy.append(item_priceBuy)

        item_priceSell = data['data'][cell_value]['low']
        itemSell.append(item_priceSell)

        item_BuyTime = data['data'][cell_value]['highTime']
        

        item_SellTime = data['data'][cell_value]['lowTime']
        

        TIMEPASSED_BUY=round(((TIMENOW - item_BuyTime)/60))
        itemBTime.append(TIMEPASSED_BUY)
        TIMEPASSED_SELL=round((TIMENOW - item_SellTime)/60)
        itemSTime.append(TIMEPASSED_SELL)
        
    #if(TIMEPASSED_BUY <60):
    #    TIMEPASSED_BUY= 'just now'
    #elif(TIMEPASSED_BUY>60 and TIMEPASSED_BUY<3600):
    #    TIMEPASSED_BUY= TIMEPASSED_BUY/60
    #    TIMEPASSED_BUY=round(TIMEPASSED_BUY,0)
    #    TIMEPASSED_BUY = str(TIMEPASSED_BUY).replace('.0', '')
    #    print(item_priceBuy , TIMEPASSED_BUY,'minutes ago',item_priceSell, TIMEPASSED_SELL)
    #    continue

        #print(item_priceBuy , TIMEPASSED_BUY,item_priceSell, TIMEPASSED_SELL)
    column = {"item_buy": itemBuy,
              "item_Buy_time": itemBTime,
              "item_sell": itemSell,
              "item_sell_time": itemSTime
              }
    
    dataframe=pd.DataFrame(column)
 
    wks.set_dataframe(dataframe,(1,2))
    
    central_tz = pytz.timezone('US/Central')
    date = datetime.datetime.now(central_tz)
    #timer= str(date)
    dt_str = date.strftime('%Y-%m-%d %H:%M:%S')
    wks.update_value('G2', dt_str)
    print(dt_str)
    
    
        
#####################################
#outline of how to retrieve data from api
#item_priceBuy = data['data']['26378']['high']       #high price retrieve of id item 26378
#item_BuyTime = data['data']['26378']['highTime']    #time of last high buy of id item 26378
#item_SellTime= data['data']['26378']['lowTime']    #time of last low buy of id item 26378



#infinite loop for calling new values


#################################################################################################
schedule.every(30).seconds.do(show)
while 1:
    schedule.run_pending()
    time.sleep(1)
################################################################################################






#cell_value = str(cell_value).replace('.0', '')    #turns cell value into str which is needed for api and replaces all ints to without .0
#print(item_priceBuy)

#df_first_13 = df.iloc[:, :13]
#print(df_first_13) # display the first 13 columns 
#if str contains comma

#item_price = item_price.replace(',','')            
#int(item_price) #str turns to int