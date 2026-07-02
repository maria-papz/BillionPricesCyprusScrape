# Important libraries 
import pandas as pd 
import tabula as tb
import numpy as np
import matplotlib.pyplot as plt

import re
import requests
import time
import urllib.request
import json
import warnings
import xlsxwriter
#import PyPDF2
import pypdf
import pdfplumber
import httpx

from ast import Try
from lxml import html, etree
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.error import URLError
#from tabula import read_pdf
from pypdf import PdfReader
from docx import Document

# Ignore specific warning
warnings.simplefilter("ignore")

# Read necessary data
df = pd.read_csv("ECOICOPv2/Datasets/Raw-Data/Raw-Data-2-2026Q3.csv")
#df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
df = df.sort_values(["Date","Retailer"])

urls = pd.read_csv("ECOICOPv2/Datasets/Products-Urls-2.csv")

# Create a null dataframe
daily_errors = pd.DataFrame(columns=["Name","Subclass","Url","Division","Retailer"])
list_ = pd.DataFrame(columns=["Date","Name","Price","Subclass","Division","Retailer"])

# Define the functions for the web-scraping of the target retailers

def results_supermarketcy(u):

    response = requests.get(Item_url_)
    print(response)
           
    if (response.status_code != 200) or ("Η σελίδα δεν βρέθηκε" in response.text) or ("Η σελίδα αφαιρέθηκε" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        price_ = soup.find('div', {'class':"text-primary text-24 lg:text-h3 font-bold italic my-4 lg:my-8"}).text.replace('€','')
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("SupermarketCy")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)
        
"""
def results_supermarketcy(u):
    
    url_new = "https://www.supermarketcy.com.cy/" + Item_url_
    
    ###  without headers 
    ## 1 
    #bs = BeautifulSoup(url_new, "html.parser")
    #response = requests.get(bs)
    ## 2
    #response = requests.get(url_new)
    
    ### with headers 
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    '''
    header = {
        "authority": "www.supermarketcy.com.cy",
        "method": "GET",
        "scheme": "https",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "max-age=0",
        "cookie": "_ga=GA1.1.281549953.1750067102; _gcl_au=1.1.1682745339.1750067102; cp_total_cart_items=0; cp_total_cart_value=0; cpab=3b260882-8582-487a-bfbd-dba2324e4489; _fbp=fb.2.1750067102781.253208881548223402; CookieConsent={stamp:'eexCFNMWujSOe4q3kf3iW8satLGH048/2ptDwTtCR134Gsh95l5YHQ==',necessary:true,preferences:true,statistics:true,marketing:true,method:'explicit',ver:1,utc:1750067102028,region:'cy'}; _nicid=a03c1e42-e50a-46ff-bec2-386f0732526d; _ga_KHCDSL47Y2=GS2.1.s1751360534$o5$g1$t1751360534$j60$l0$h0; cp_sessionTime=1751360533438; XSRF-TOKEN=eyJpdiI6IkhLTENwSTBxSm11ZVlRQnh2bnQ5S3c9PSIsInZhbHVlIjoiTUoxcitJS3o4dGlHdkV5SStPLzRmdG9sa3pZWUc3MC9QVE55TjYrdTlaeFhoZzZ6RE9LcTNiSS8zRWs5V3MyYi9ZeGJMc2JPOTk3TG5aK3M2eXhWNzRVdWdhVDF2MHZCcVRaRHFpOElUUWVGVmlGeFl4ak5PZ2RyOGxGc3RlWHAiLCJtYWMiOiIwZGE5NDZhMGZmOGQwNWRmNGQzZWQzNDA2MDI4ZjgxMGVjZTBkMmQwZDQ0MDdkODg2MjNiNDM1ZjQyMDI0N2IyIiwidGFnIjoiIn0=; supermarketcy_session=eyJpdiI6IlF0RWVLT3FnMmxGazFmQkJKM2Z4eEE9PSIsInZhbHVlIjoiMXk3ZnFlYWE1MFJvQ2xOUXNIUjE1OERUTnRrVWpMQ2hLK2g4UXEvcnp6K0cxVnROLzd0UHlnVUZGZ0owbTJORlRxWlRZZlIzUnpHTVZOSUdrM0dkTnZSejFIR0NHcGFjQVhXUVZwN3Z0cDc3dGhhUWpJalZOb0xWUWdLYXRtcFMiLCJtYWMiOiJlNDE5YjkxNzFhNGE3N2IzMjFlZmIxNTk5YzljMjQ2NGE5ZDA0Y2U3NzE3YWMyODc0MGZlMmRhNWQ4MzYwODkwIiwidGFnIjoiIn0=; recently_viewed=eyJpdiI6IncyaUEzeWVzN3pVUUlWeDh6SmtRWVE9PSIsInZhbHVlIjoiVjdXd3pSbzFMOXFrc0hFWDdCaHVvc3U3QmRVem9SbEVRNWdkYmxXOGQ1OUZFVVA0YmV1Nzd5cnUrOGxwZG1RWCIsIm1hYyI6ImUxOTc1NjBjNmY1MjJlZTYyMzNhNDNkMjk4YmRkNzU4NWIwZDc3OTVjZDQ0OTlkYWY3MGVkNDViY2UzMTQ1MDkiLCJ0YWciOiIifQ==",
        "priority": "u=0, i",
        "sec-ch-ua": "\"Google Chrome\";v=\"137\", \"Chromium\";v=\"137\", \"Not/A)Brand\";v=\"24\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
    }
    '''
    ## 1 
    #bs = BeautifulSoup(url_new, "html.parser")
    #response = requests.get(bs, {'headers':header})
    ## 2
    #response = requests.get(url_new, headers = header) 
    ## 3 
    with httpx.Client(headers = header) as client:
        response = client.get(url_new)
    
    print(response)

    if (response.status_code != 200) : #or ("Η σελίδα δεν βρέθηκε" in response.text) or ("Η σελίδα αφαιρέθηκε" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        #soup = BeautifulSoup(response.text, "html.parser")
        name_wrappers = soup.find('h1', {'class':"text-h6 md:text-h4 text-gray-dark font-bold mb-8 lg:mb-40 lg:max-w-520 leading-snug italic"}).text
        
        if (name_wrappers=='Τσιπούρα Φρέσκια Καθαρισμένη 1.5kg') |  (name_wrappers=='Χταπόδι Φρέσκο 1.5kg') :
            price_wrappers = soup.find('div', {'class':"text-small text-grey-light-darker"}).text
            price_ = price_wrappers.split('\xa0')[0].replace(',', '.').replace('1kg: ', '')
        else:
            price_wrappers = soup.find('div', {'class':"text-primary text-24 lg:text-h3 font-bold italic my-4 lg:my-8"}).text
            price_ = price_wrappers.split('\xa0')[0].replace(',', '.')
        
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_wrappers)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("SupermarketCy")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)
"""

def results_fueldaddy(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    
    response = requests.get(Item_url_, headers=header)
    print(response)
        
    if (response.status_code != 200) or ("Η σελίδα δεν βρέθηκε" in response.text) or ("404 Not Found" in response.text):
        print("No URL")
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)  
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("div", {"class":"col-md-7 pump-info-right"})
        
        for brand_name in element_soup:
            brand = brand_name.find_all(class_ = "col-sm-9")[1]
            
            for brand_name in brand:
                brand_word = brand_name.get_text(strip = True).upper()
            
        if brand_word:
            if brand_word=="Πετρολίνα" or (brand_word=="ΠΕΤΡΟΛΊΝΑ"):
                brand_word="PETROLINA"
        else:
            brand_word="PETROLINA"
            
        name = element_soup[0].find_all("div", {"class" : "col-sm-9"})
        name_word = name[0].text.strip().replace("\n","")
        element_price = soup.find_all("div", {"class":"price-item"})
        
        price_list = []
        for i in range(len(element_price)):
            name = element_price[i].find(class_ = "brandtag cut-text fueltype-heading").get_text(strip = True)
            price = element_price[i].find(class_ = "pricetag").get_text(strip = True).replace(" €","")
            price_list.append(name)
            price_list.append(price)
        
        for i in range(1,len(price_list),2):
            new_row = []
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    
            if price_list[i-1]=='Unleaded 95':
                new_row.append(name_word+" - "+"Αμόλυβδη 95")
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Petrol")
                new_row.append("TRANSPORT")
                
            elif price_list[i-1]=='Unleaded 98':
                new_row.append(name_word+" - "+'Αμόλυβδη 98')
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Petrol")
                new_row.append("TRANSPORT")
                
            elif price_list[i-1]=='Diesel':
                new_row.append(name_word+" - "+'Πετρέλαιο Κίνησης')
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Diesel")
                new_row.append("TRANSPORT")
                 
            elif price_list[i-1]=='Heating Diesel':
                new_row.append(name_word+" - "+'Πετρέλαιο Θέρμανσης')
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Liquid fuels")
                new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
                   
            elif price_list[i-1]=='Kerosene':
                new_row.append(name_word+" - "+'Κηροζίνη')
                new_row.append(float(price_list[i].replace(",",".")))
                new_row.append("Liquid fuels")
                new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
                
            new_row.append(brand_word) 
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_akentia(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs, {'headers':header})
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all('div', {"class":"product-price"})
        price_ = element_name[0].text.replace("€","").replace(" ","").replace(",",".")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Akentia")
        list_.loc[len(list_)] = new_row

def results_intercity_buses(u):
    
    ### without headers
    ## 1
    #response = requests.get(Item_url_)
    ## 2
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers':header})
    
    ### with headers
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    ## 1
    response = requests.get(Item_url_, {'headers':header})
    ## 2
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers':header})

    print(response)
        
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        table_ = soup.find_all("table", {"class":"tablesorter eael-data-table center"})[0]
        if table_:
            element_ = table_.find_all("div", {"class":"td-content-wrapper"}) 
            for i in range(0,2):
                new_row = []
                if i%2 == 0:
                    ticket_name_ = element_[i].text.replace(" ","").replace("\n","").replace("\t","")
                    price_ = element_[i+1].text.replace(" ","").replace("\n","").replace("\t","").replace("€","")
                    if (price_=="NOTAVAILABLE") or (price_=='ΔΕΝΔΙΑΤΙΘΕΤΑΙ'):
                        pass
                    else:
                        print(price_)
                        new_row.append(datetime.now().strftime('%Y-%m-%d'))
                        new_row.append(ticket_name_ + Item_url_)
                        new_row.append(float(price_))
                        new_row.append(subclass_)
                        new_row.append(division_)
                        new_row.append("Intercity Buses")
                        list_.loc[len(list_)] = new_row
                        
def results_cyprus_transport(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, headers = header)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        wrapper = soup.find_all('tbody')[0]
        data = []
        for row in wrapper.find_all('tr'):
            row_data = []
            for cell in row.find_all(['td', 'th']):
                row_data.append(cell.get_text().strip())
            data.append(row_data)
        df1 = pd.DataFrame(data)
        df1.columns = ['Ticket type', 'Paper Ticket (CASH)', 'Plastic ANONYMOUS Card', 'Plastic PERSONALISED Motion Bus Card - Normal Charge', 'Plastic PERSONALISED Motion Bus Card - Beneficiaries of 50%' ]
        df1 = df1.drop(0)
        df1 = df1.drop(1)
        df1 = df1.drop(6)
        df1 = df1.set_index('Ticket type')
        new_list = []
        
        for column in df1.columns:  
            for index in df1.index:
                value = df1.loc[index, column]
                new_row = {'Date': datetime.now().strftime('%Y-%m-%d'), 'Name': f'{column} / {index}', 'Price': value, 'Subclass': 'Passenger transport by bus and coach', 'Division': 'TRANSPORT', 'Retailer': 'Cyprus Public Transport'}  # Create a new row with the concatenated column name and index value
                new_list.append(new_row)
                
        df2 = pd.DataFrame.from_records(new_list)
        df_cy_transport = df2[df2["Price"] != '-']
        df_cy_transport['Price'] = df_cy_transport['Price'].str.replace('€', '').replace('Αρχική τιμή ', '')
        df_cy_transport['Price'] = df_cy_transport['Price'].astype(float)
        df_cy_transport.reset_index(drop = True, inplace = True)

        for index, row in df_cy_transport.iterrows():
            if row['Name'] == name_:
                list_.loc[len(list_)] = row
                list_['Name'] = list_['Name'].apply(lambda x:x)
                
def results_max_7_taxi(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, {'headers':header})
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        table_ = soup.find('table', {"class" :'tbl',"style":"width: 100%;","border":"1","frame":"void","cellspacing":"1","cellpadding":"3","align":"center"})
        table_ = table_.text
        if "Initial charge" in name_:
            pattern = r'Initial charge\s+([\d,]+)\s+([\d,]+)'
        if "Fare per Km" in name_:
            pattern = r'Fare per Km\s+([\d,]+)\s+([\d,]+)'  
        matches = re.findall(pattern, table_)
        charges_ = [float(charge.replace(',', '.')) for charge in matches[0]]
        
        for i in range(0,2):
            if i == 0:
                add_ = "Fixed"
            if i == 1:
                add_ = "Variable"
            new_row = []
            new_row.append(datetime.today().strftime("%Y-%m-%d"))
            new_row.append(name_ + add_)
            print(float(charges_[i]))
            new_row.append(float(charges_[i]))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Max 7 Taxi") 
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_costastheodorou(u):
    
    response = requests.get(Item_url_)
    print(response)

    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all("p", {"class":"price"})
        price_ = element_name[0].text.replace("€","").split('\xa0')[0]
        print(price_)
        new_row.append(datetime.today().strftime("%Y-%m-%d"))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Costas Theodorou")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_leroymerlin(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, {'headers':header})
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code != 200 or ("Η σελίδα που αναζητάτε δεν βρέθηκε." in soup.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_ = soup.find_all("span",{"class":"priceBigMain"})
        price_ = element_[0].text.replace("€","").replace(" ","").replace(",",".")
        print(price_)
        new_row.append(datetime.today().strftime("%Y-%m-%d"))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Leroy Merlin") 
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_ikea(u):
    
    ## 1st way (without header)
    response = requests.get(Item_url_)
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs)  
    
    ## 2nd (with header) 
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    #response = requests.get(Item_url_, headers=header)

    print(response)

    soup = BeautifulSoup(response.content, "html.parser")
    
    if (response.status_code != 200) or ("διαθέσιμα προϊόντα" in soup.text) or ("0 προϊόντα" in soup.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x) 
    else:
        element_soup = soup.find_all("span", {"class":"price__sr-text"})
        price_ = element_soup[0].text.strip("Τρέχουσα τιμή € ").replace("Αρχική τιμή € ","").replace(",",".")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("IKEA")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x) 

def results_premier(u):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Origin': 'https://premierlaundry.com.cy',
        'Connection': 'keep-alive',
        'Referer': 'https://premierlaundry.com.cy/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',}

    params = { }
    json_data = {'email': 'kendeas123@gmail.com', 'password': 'Kendeas',}
    response = requests.post('https://cleancloudapp.com/webapp/public/api/auth/login/16130', params=params, headers=headers, json=json_data,)
    print(response)
    data = response.json()
    user_id = data['id']
    token = data['token']

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'X-CC-User': str(user_id), 
        'X-CC-Token': token, 
        'Origin': 'https://premierlaundry.com.cy',
        'Connection': 'keep-alive',
        'Referer': 'https://premierlaundry.com.cy/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',}

    params = {'ccascv': '0.20327901592645015',}
    json_data = {'priceListId': 0,}
    response = requests.post('https://cleancloudapp.com/webapp/public/api/store/products', params=params, headers=headers, json=json_data,)
    print(response)
    all_data_products = response.json()
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        products = all_data_products['Products']
        names = [item['name'] for item in products]
        price = [item["price"] for item in products]
        for i in range(len(names)):
            if name_ == names[i]:
                new_row.append(datetime.today().strftime("%Y-%m-%d"))
                new_row.append(names[i])
                new_row.append(float(price[i]))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Premier Laundry")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_musicavenue(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, {'headers':header})
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        new_row.append(datetime.today().strftime("%Y-%m-%d"))
        name = soup.find('h1', class_ = 'product-title')
        new_row.append(name_)
        price_ = soup.find_all("bdi")[1].text.replace("€", "").replace(",", "")
        print(price_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Musicavenue")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_electroline(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("ins", {"class":"product-price product-price--single product-price--sale-price product-price--single--sale-price"}) 
        if element_soup:
            price_ = element_soup[0].text.replace("\n",'').replace("€","").replace(" ","")
        else:
            element_soup = soup.find_all("h2", {"class":"product-price product-price--single"}) 
            price_ = element_soup[0].text.replace("\n","").replace("€","").replace(" ","")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Electroline")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_stephanis(u):

    ### with headers 
    #header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    ## 1 
    #response = requests.get(Item_url_, headers = header)
    ## 2 
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers':header})
    ## 3 
    #with httpx.Client(headers = header) as client:
    #    response = client.get(Item_url_)
    
    ### without headers
    ## 1 
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs) 
    ## 2 
    response = requests.get(Item_url_)

    print(response)
    
    if (response.status_code != 200) or ("This product is no longer available" in response.text) or ("404 Not Found" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")    
        element_soup = soup.find_all("div", {"class":"listing-details-heading"})
        price_ = element_soup[0].text.replace("€","").replace("\n","")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Stephanis")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_public(u):
        
    ###  without headers 
    ## 1 
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    ## 2 
    #response = requests.get(Item_url_)

    ### with headers 
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    ## 1 
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers':header})
    ## 2 
    #response = requests.get(Item_url_, headers = header) 

    print(response)
    
    if (response.status_code != 200) : 
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        data = response.json()
        price_ = data["prices"][0]["salePrice"] #OR "listPrice"
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Public")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)

def results_parga(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, {'headers':header})
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('span', {'class':'productPriceStore'})
        price_ = element_[1].text.replace("€","")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Parga")
        list_.loc[len(list_)] = new_row

def results_cyta(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")

    if (response.status_code == 200):
        
        # Fixed/Mobile communication services
        if (name_=="Τέλη κλήσεων προς Σταθερό") | (name_=="Τέλη κλήσεων προς Κινητή Τηλεφωνία") :
            element_soup = soup.find_all("td", {"class":"xl176"})
            if name_=="Τέλη κλήσεων προς Σταθερό":
                price_ = element_soup[0].text.replace(",",".")
            if name_=="Τέλη κλήσεων προς Κινητή Τηλεφωνία":
                price_ = element_soup[3].text.replace(",",".")
                
        # Internet access provision services and online storage services
        elif (name_=="Internet Home 200Mbps") | (name_=="Internet Home 500Mbps"):
            element_soup = soup.find_all("div", {"class":"price-block py-2 text-center"})
            if name_=="Internet Home 200Mbps":
                element_ = element_soup[0].text
            if name_=="Internet Home 500Mbps":
                element_ = element_soup[1].text    
            prices_ = re.findall(r'€(\d+,\d+)', element_)
            price_ = prices_[0].replace(",",".")
            
        # Bundled telecommunication services
        elif (name_=="FREEDOM") |  (name_=="FREEDOM Plus") :
            element_soup = soup.find_all("h4", {"class":"text-24 text-center mb-0 pb-0"})
            if name_=="FREEDOM":
                element_ = element_soup[0].text
            if name_=="FREEDOM Plus":
                element_ = element_soup[1].text
            prices_ = re.findall(r'€(\d+,\d+)', element_)
            price_ = prices_[0].replace(",",".")    
            
        print(price_)   
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("CYTA")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        
def results_epic(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs, verify=False)  # bypasses SSL verification
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")

    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        #Bundled telecommunication services
        if name_ == "5G Unlimited Max Plus":
            element_ = soup.find_all("div", {"class":"price"})
            price_ = element_[0].text.replace("€","")
            print(price_)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Epic")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        
        if name_ == "5G Unlimited Max":
            element_ = soup.find_all("div", {"class":"price"})
            price_ = element_[1].text.replace("€","")
            print(price_)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Epic")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)  
        
        #Fixed/Mobile communication services
        if name_ == "To fixed telephony lines of other providers":
            element_ = soup.find_all("table", {"class":"yellow-top-zebra"})
            data = element_[0].text.replace("€","")
            pattern = r"To fixed telephony lines of other providers.*?\n(\d+\.\d+)$" 
            match = re.search(pattern, data, re.MULTILINE)
            if match:
                value = match.group(1) # Extract the captured group 
            price_ = float(value) 
            print(price_)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Epic")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)      
        
        if name_ == "To mobile telephony lines of other providers":
            element_ = soup.find_all("table", {"class":"yellow-top-zebra"})
            data = element_[0].text.replace("€","")
            pattern = r"To mobile telephony lines of other providers.*?\n(\d+\.\d+)$" 
            match = re.search(pattern, data, re.MULTILINE)
            if match:
                value = match.group(1) # Extract the captured group 
            price_ = float(value) 
            print(price_)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Epic")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x) 
        
        #Internet access provision services and online storage services    
        if name_ == "Broadband Homebox 1":
            element_ = soup.find_all("table", {"class":"yellow-top"})
            data = element_[0].text.replace("€","")
            pattern = r"Monthly Fee.*?\n(\d+\.\d+)\n(\d+\.\d+)\n(\d+\.\d+)$" #1st, 2nd, and 3rd values
            match = re.search(pattern, data, re.MULTILINE)
            if match:
                value = match.group(1) # Extract the captured group (1st value)
            price_ = float(value)
            print(price_)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Epic")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        
        if name_ == "Broadband Homebox 2":
            element_ = soup.find_all("table", {"class":"yellow-top"})
            data = element_[0].text.replace("€","")
            pattern = r"Monthly Fee.*?\n(\d+\.\d+)\n(\d+\.\d+)\n(\d+\.\d+)$" #1st, 2nd, and 3rd values
            match = re.search(pattern, data, re.MULTILINE)
            if match:
                value = match.group(2) # Extract the captured group (2nd value)
            price_ = float(value)
            print(price_)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Epic")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)    

def results_primetel(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")

    if ("Pay my bill" in soup.text) or (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        # Bundled telecommunication services	
        if (name_=="GIGA Unlimited 5G") | (name_=="GIGA Unlimited 5G MAX") :
            
            element_ = soup.find_all('p', {"class":"price"})
             
            if name_ == "GIGA Unlimited 5G" :
                text_ = element_[0].text
                pattern = r"(\d+\.\d+)\n"
                match = re.search(pattern, text_)
                price_ = match.group(1) 
                print(price_)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Primetel")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)    
             
            if name_ == "GIGA Unlimited 5G MAX" :
                text_ = element_[1].text
                pattern = r"(\d+\.\d+)\n"
                match = re.search(pattern, text_)
                price_ = match.group(1) 
                print(price_)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Primetel")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

        # Fixed/Mobile communication services           
        elif (name_=="Calls to other providers landline") | (name_=="Calls to other providers mobile") :
            
            element_ = soup.find_all("table", {"id":"call_rates"}, {"class":"table-striped table-bordered dt-responsive table-hover nowrap dataTable dtr-inline data_table_resp"})
            element_td = element_[0].find_all("td")
                
            if name_ == "Calls to other providers landline" :
                    price_ = element_td[9].text.replace("\n","").replace(" ","").replace("€","").replace("/minute","")
                    print(price_)
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("Primetel")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)
                    
            if name_ == "Calls to other providers mobile" :
                    price_ = element_td[11].text.replace("\n","").replace(" ","").replace("€","").replace("/minute.Minimumcharge1minute","")        
                    print(price_)
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("Primetel")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)
                
        # Internet access provision services and online storage services 
        elif  (name_=="Fiber Family & 200Mbps") | (name_=="Fiber Entertainment & 200Mbps") :

            element_ = soup.find_all("div", {"class":"price_tv_pack"})
            
            if name_ == "Fiber Family & 200Mbps" :
                    text_3 = element_[3].text
                    match = re.search(r'€\d+\.\d+\ / month', text_3)
                    if match:
                        price_ = match.group(0).replace('€','').replace(' ','').replace('/','').replace('month','')
                    print(price_)    
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("Primetel")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)
            
            if name_ == "Fiber Entertainment & 200Mbps" :
                    text_4 = element_[4].text
                    match = re.search(r'€\d+\.\d+\ / month', text_4)
                    if match:
                        price_ = match.group(0).replace('€','').replace(' ','').replace('/','').replace('month','')
                    print(price_)    
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)
                    new_row.append("Primetel")
                    list_.loc[len(list_)] = new_row
                    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_cablenet(u):

    ### without headers
    ## 1 
    response = requests.get(Item_url_)
    ## 2 
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs) 

    ### with headers 
    #header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    ## 1 
    #response = requests.get(Item_url_, headers = header)
    ## 2 
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers':header})
    ## 3
    #with httpx.Client(headers = header) as client:
    #    response = client.get(Item_url_)

    print(response)

    if response.status_code != 200 :
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Internet access provision services and online storage services
        if (name_=="GigaMax 1000M") | (name_=="Super 300M") : 
            element_soup = soup.find_all("span", {"class":"service-price"})
            if name_=="GigaMax 1000M":
                price_ = element_soup[3].text.replace('€','')
            if name_=="Super 300M":
                price_ = element_soup[0].text.replace('€','') 
            
        # Bundled telecommunication services
        elif (name_=="5G Unlimited") | (name_=="5G Unlimited Max") :
            element_soup = soup.find_all("span", {"class":"service-price"})
            if name_ == "5G Unlimited":
                price_ = float(element_soup[0].text.replace("€",""))
            if name_ == "5G Unlimited Max":
                price_ = float(element_soup[0].text.replace("€",""))
            
        else:
        # Fixed/Mobile communication services
            element_name = soup.find_all("td")
            for i in element_name:
                if i.text == name_:
                    price_ = element_name[28].text.replace("€","").replace(" ","").replace("/","").replace("30","").replace("''","")
                if i.text == name_:
                    price_ = element_name[33].text.replace("€","").replace(" ","").replace("/","").replace("30","").replace("''","")
                    
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Cablenet")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
        
def results_famousports(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if (response.status_code != 200) or ("Oops! Page Not Found!" in soup.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("h2", {"class":"product-price product-price--single"}) 
        element_soup = soup.find_all("strong", {"class":"text-xl lg:text-2xl font-bold tracking-tight"})
        price_ = element_soup[0].text.replace("\n","").replace(" ","").replace("€","").replace(",",".")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Famous Sports")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_Marks_Spencer(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("Sorry, we can't" in soup.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)   
    else:
        element_soup = soup.find_all("span",{"class":"list-pricecolour"})
        price_ = element_soup[0].text.replace("\n","").replace(" ","").replace("€","").replace(",",".")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Marks & Spencer")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_Athlokinisi(u):
        
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("span",{"class":"ammount"})
        
        if not element_soup:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x) 
        else:
            price_ = float(element_soup[0].text.strip().replace("€",""))
            print(price_)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Athlokinisi")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_AlterVape(u):
    
    response = requests.get(Item_url_)
    print(response)

    if ("Page not found" in response.text) or (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        scripts = soup.find_all("script", type = "application/ld+json")

        for script in scripts:
            
            try:
                data = json.loads(script.string)
                
                if data.get("@type") == "Product":
                    price_ = data["offers"]["price"]
                    break
                    
            except Exception:
                pass
            
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Alter Vape")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_ewholesale(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x) 
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_soup = soup.find_all("div", {"class":"hM4gpp"}) 
        price_= element_soup[0].text.replace(",",".").replace(" ","").replace("€","").replace("Τιμή","").replace("Price","")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("E-wholesale")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_CYgar_shop(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all('div', {"class":"hM4gpp"})
        price_ = element_name[0].text.replace('€','').replace('Price','')
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("The CYgar shop")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
            
def results_royal_cigars(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all('div', {"class":"itemDetailsPrice"})
        if element_name:
            price_amount = element_name[0].text.replace("€","")
            print(price_amount)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_amount))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("The Royal Cigars")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_hotboxcy(u):
    
    response = requests.get(Item_url_)
    print(response)

    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")    
        element_soup = soup.find_all("s", {"class":"price-item price-item--regular"})
        price_ = element_soup[0].text.replace("€","").replace("EUR","").replace(",",".").replace("\n","").replace(" ","")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Hotbox Cy")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_moto_race(u):
    
    ### without headers
    ## 1 (not working)
    response = requests.get(Item_url_)
    ## 2 (not working)
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs) 

    ### with headers 
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    ## 1 (not working)
    #response = requests.get(Item_url_, headers = header)
    ## 2 (not working)
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers':header})
    ## 3 (not working)
    #with httpx.Client(headers = header) as client:
    #    response = client.get(Item_url_)
    
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("404 Not Found" in soup.text) or (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)  
    else:
        element_soup = soup.find_all("span", {"class":"price-wrapper"})
        price_ = element_soup[0].text.replace(",","").replace("€","")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Moto Race")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_awol(u):
    
    p = 0
    price_ = "0"
        
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    element_soup = soup.find_all("span", {"class":"price price--sale"})
    
    if element_soup:
        p = 0
    else:
        element_soup = soup.find_all("span", {"class":"price"})   
        
    if ((response.status_code !=200) or ("Page Not Found" in response.text)):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x) 
    else:
        if element_soup[0] is not None:
            amounts_list = element_soup[0].text.split('€')
            if len(amounts_list) > 2:
                price_ = amounts_list[2]
            if len(amounts_list) <= 2:
                price_ = amounts_list[1] 
        price_= price_.replace(",",".")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("AWOL")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_novella(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    
    soup = BeautifulSoup(response.content, "html.parser")
 
    if (response.status_code != 200) or ("404 Page Not Found." in soup.text) :
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        services_list = soup.find_all('td', {'class':'column-1'}, string=True)
        prices_list = soup.find_all('td', {'class':'column-2'}, string=True)
            
        if name_ == "Services, LADIES CUT" :
            price_ = prices_list[0].text.replace('€',"").replace(',','.')
          
        elif name_ == "Services, MEN'S CUT" :
            price_ = prices_list[3].text.replace('€',"").replace(',','.')
            
        elif name_ == "Services, CHILDREN'S CUT" :
            price_ = prices_list[4].text.replace('€',"").replace(',','.')  
         
        elif name_ == "Student Offers, LADIES CUT" :
            price_ = prices_list[27].text.replace('€',"").replace(',','.')
          
        elif name_ == "Student Offers, MEN'S CUT" :
            price_ = prices_list[28].text.replace('€',"").replace(',','.')
        
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Novella")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x) 

def results_hairspray(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, headers=header)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
 
    if response.status_code != 200 :
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    
    else:
        table_rows = soup.find_all("tr")
        
        if name_ == "Womens Cut":
            text_ = table_rows[1].get_text(strip=True)
            price_ = re.findall(r"€(\d+)", text_)[0]

        elif name_ == "Kids Boy Haircut 6-10 year":
            text_ = table_rows[4].get_text(strip=True)
            price_ = re.findall(r"€(\d+)", text_)[0]

        elif name_ == "Kids Girl Haircut 6-10 year":
            text_ = table_rows[5].get_text(strip=True)
            price_ = re.findall(r"€(\d+)", text_)[0]

        elif name_ == "Mens Hair Cut":
            text_ = table_rows[6].get_text(strip=True)
            price_ = re.findall(r"€(\d+)", text_)[0]
        
        print(price_) 
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Hairspray")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x) 

def results_studio37(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, headers=header)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
 
    if response.status_code != 200 :
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    
    else:
        table_rows = soup.find_all("tr")
        
        if name_ == "Women's Cut & Blowdry":
            text_ = table_rows[0].get_text(strip=True)
            price_ = re.findall(r"€(\d+)", text_)[0]

        elif name_ == "Men's Cut":
            text_ = table_rows[3].get_text(strip=True)
            price_ = re.findall(r"€(\d+)", text_)[0]

        elif name_ == "Boy's Cut":
            text_ = table_rows[4].get_text(strip=True)
            price_ = re.findall(r"€(\d+)", text_)[0]

        elif name_ == "Girl's Cut":
            text_ = table_rows[5].get_text(strip=True)
            price_ = re.findall(r"€(\d+)", text_)[0]
        
        print(price_) 
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Studio 37 For Hair")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x) 
        
def results_magdas(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, headers=header)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
 
    if response.status_code != 200 :
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    
    else:
        element = soup.find_all("div", {"class":"et_pb_text_inner"})
        text_prices = element[9].get_text(strip=True)
        prices = re.findall(r"(\d+)€", text_prices)
        
        if name_ == "Women's wet cut":
            price_ = prices[0]

        elif name_ == "Girls cut":
            price_ = prices[2]

        elif name_ == "Men's cut":
            price_ = prices[3]

        elif name_ == "Boys cut":
            price_ = prices[4]
        
        print(price_) 
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Magdas Hair Boutique")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)         

def results_douce_et_belle(u):
    
    response = requests.get(Item_url_)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
 
    if response.status_code != 200 :
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    
    else:
        element_soup = soup.find_all("span", {"class":"mkdf-bsl-price"})
        
        if name_ == "Women haircut only":
            price_ = element_soup[0].text.replace("from ","").replace("€","")

        elif name_ == "Men haircut":
            price_ = element_soup[1].text.replace("€","")

        elif name_ == "Children haircut":
            price_ = element_soup[2].text.replace("€","")
        
        print(price_) 
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Douce et Belle")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)  
        
def results_rio(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("404 Not Found!" in soup.text) or (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_name = soup.find_all('p',{"style":"text-align: center;"})
        for i in range(0,len(element_name)):
            if name_ in element_name[i].text:
                if "3D" in element_name[i].text:
                    match = re.search(r'(\S+)\s*€(\d+)', element_name[i].text)

                    if match:
                        new_row=[]
                        new_row.append(datetime.now().strftime('%Y-%m-%d'))
                        new_row.append(name_+" 3D")
                        new_row.append(float(match.group(2)))
                        new_row.append(subclass_)
                        new_row.append(division_)
                        new_row.append("Rio Cinema")
                        list_.loc[len(list_)] = new_row
                        list_['Name'] = list_['Name'].apply(lambda x:x)
                    else:
                        website_false.append(name_)
                        website_false.append(subclass_)
                        website_false.append(Item_url_)
                        website_false.append(division_)
                        website_false.append(retailer_)
                        daily_errors.loc[len(daily_errors)] = website_false
                        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)     
                else:
                    amount_match = re.search(r'€(\d+)', element_name[i].text)
                    if amount_match:
                        price_ = amount_match.group(1)
                        print(price_)
                        new_row=[]
                        new_row.append(datetime.now().strftime('%Y-%m-%d'))
                        new_row.append(name_)
                        new_row.append(float(price_))
                        new_row.append(subclass_)
                        new_row.append(division_)
                        new_row.append("Rio Cinema")
                        list_.loc[len(list_)] = new_row
                        list_['Name'] = list_['Name'].apply(lambda x:x)
                    else:
                        website_false.append(name_)
                        website_false.append(subclass_)
                        website_false.append(Item_url_)
                        website_false.append(division_)
                        website_false.append(retailer_)
                        daily_errors.loc[len(daily_errors)] = website_false
                        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
                        
def results_EUC(u):
    '''
    #Scrape the tuition fees from the URL-PDF
    response = requests.get(Item_url_)
    print(response)
    euc = tb.read_pdf(Item_url_, pages = '2', pandas_options = {'header': None}, stream = True)
    list_euc = []
    imax = 4 # *be careful to set this value correctly when each new year's tuition fees are published* 
    for i in range(0, imax): 
        new_row = []
        euc[i][1] = euc[i][1].astype('string')
        for word in euc[i][1].to_list():
            word = word.replace(',','')
            word = int(word)
            list_euc.append(word)
    price_ = (sum(list_euc) + 23000 + 25000 + 23000 + 21000) / (len(list_euc) + 4) #add manually the tuition fees of the medical, dental and veterinary studies
    '''
    #Scrape the tuition fees from the PDF
    pdf_path = r"ECOICOPv2/PDFs/EUC-tuition-fees-2025-26.pdf"
    amounts = []
    price_1 = 0
    count_ = 0
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[1]
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if len(row) > 1 and row[1]:
                    cell = row[1]
                    if re.fullmatch(r"\d{1,3}(?:,\d{3})*", cell):
                        amount_ = cell.replace(",","")
                        amount_ = float(amount_)
                        price_1 += amount_
                        count_ += 1
    price_ = price_1 / count_
    print(price_)
    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(float(price_))
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("European University Cyprus")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_CyMinistryEducation(u):

    ## 2025-26: Fees available online in 17/06/2025 (https://www.moec.gov.cy/idiotiki_ekpaidefsi/didaktra.html)

    #THE GRAMMAR JUNIOR SCHOOL (Nicosia)
    if "ΝΗΠΙΑΓΩΓΕΙΩΝ" in name_:
        
        # Read the pdf file using pdfplumber
        with pdfplumber.open("ECOICOPv2/PDFs/didaktra_idiotikon_nipiagogeion_2025_26.pdf") as pdf:
            page = pdf.pages[3]
            table = page.extract_table()
        
        price_1_1 = float(table[2][2].replace("€","").split("\n")[0])
        price_1_2 = float(table[2][2].replace("€","").split("\n")[1])
        price_1 = (price_1_1 + price_1_2) / 2
        price_2 = float(table[2][4].split("εγγραφή")[0].replace("€",""))
        price_ = price_1 + price_2
        print(price_)

    if "ΔΗΜΟΤΙΚΩΝ" in name_:        
            
        with pdfplumber.open("ECOICOPv2/PDFs/didaktra_idiotikon_dimotikon_scholeion_2025_26.pdf") as pdf:
            page = pdf.pages[0]  # 4th page (index starts from 0)
            table = page.extract_table()
            
            price_1 = float(table[8][2].replace("€","").replace(".","")) + float(table[8][3].replace("€","").replace(".","")) + float(table[8][4].replace("€","").replace(".","")) + float(table[8][5].replace("€","").replace(".","")) + float(table[8][6].replace("€","").replace(".","")) + float(table[8][7].replace("€","").replace(".",""))
            price_2 = price_1 / 6
            price_3 = table[8][8] #.split("τέλος εγγραφής, τετράδια, εκδρομές,\nασφάλεια παιδιών €280")[1].replace("€","")
            amount = re.search(r'€\s*(\d+)', price_3)
            if amount:
                price_3 = amount.group(1)
            else:
                price_3 = 0
            price_ = price_2 + float(price_3)
            print(price_)

    #THE GRAMMAR SCHOOL (NICOSIA)
    if ("Nicosia" in name_) and ("ΜΕΣΗΣ" in name_):
                
        with pdfplumber.open("ECOICOPv2/PDFs/didaktra_idiotikon_mesi_ekpaidefsi_2025_26.pdf") as pdf:
            page = pdf.pages[0] 
            table = page.extract_table()
            
            #Α΄ τάξη - ΣΤ΄ τάξη
            if subclass_ == "Secondary education":
                price_1 = float(table[4][2].replace("€","").replace(".","")) + float(table[4][3].replace("€","").replace(".","")) + float(table[4][4].replace("€","").replace(".","")) + float(table[4][5].replace("€","").replace(".","")) + float(table[4][6].replace("€","").replace(".","")) + float(table[4][7].replace("€","").replace(".",""))
                price_ = price_1 / 6
                print(price_)
            
            #Ζ' τάξη
            if subclass_ == "Post-secondary non-tertiary education":
                price_ = float(table[4][8].replace("€",'').replace(".",""))
                print(price_)
    
    #THE GRAMMAR SCHOOL (LIMASSOL)
    if ("Limassol" in name_) and ("ΜΕΣΗΣ" in name_):
    
        with pdfplumber.open("ECOICOPv2/PDFs/didaktra_idiotikon_mesi_ekpaidefsi_2025_26.pdf") as pdf:
            page = pdf.pages[1] 
            table = page.extract_table()

            #Α΄ τάξη - ΣΤ΄ τάξη
            if subclass_ == "Secondary education":
                price_1 = float(table[8][2].replace("€","").replace(".","")) + float(table[8][3].replace("€","").replace(".","")) + float(table[8][4].replace("€","").replace(".","")) + float(table[8][5].replace("€","").replace(".","")) + float(table[8][6].replace("€","").replace(".","")) + float(table[8][7].replace("€","").replace(".",""))
                price_ = price_1 / 6
                print(price_)
            
            #Z΄ τάξη
            if subclass_ == "Post-secondary non-tertiary education":
                price_ = float(table[8][8].replace("€",'').replace(".",""))
                print(price_)

    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(float(price_))
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("Cyprus Ministry of Education, Sport and Youth")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_CyPost(u):
    '''
    #code using the products URLs and the read_pdf function to read the URL-PDF file: 
    if ("ΜΕΜΟΝΩΜΕΝΩΝ" in name_):
        p=6
        d=2
        if ("50 γρ." in name_):
            qp=14
        elif ("500 γρ." in name_):
            qp=21
        elif ("2000 γρ." in name_):
            qp=44
        
    if ("ΔΕΜΑΤΩΝ" in name_):
        p=11
        d=1
        if ("0.5 κιλό" in name_):
            qp=2
        elif("15 κιλά" in name_):
            qp=17
        elif ("30 κιλά" in name_):
            qp=32

    response = requests.get(Item_url_)
    print(response)
    pdf_ = tb.read_pdf(Item_url_, pages = p, pandas_options = {'header': None}, stream = True)[0]
    pdf_[d] = pdf_[d].astype('string')
    price_ = pdf_[d][qp].split(' ')[0].replace(',','.')
    print(price_)
    '''
    
    #code using the PDF file and the pdfplumber function to read the PDF file: 
    pdf_path = r"ECOICOPv2/PDFs/CyprusPost_Jun2018.pdf"

    if ("ΜΕΜΟΝΩΜΕΝΩΝ" in name_):
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[5]
            tables = page.extract_tables()
        
        if ("50 γρ." in name_):
            target_weight = "50"
        elif ("500 γρ." in name_):
            target_weight = "500"
        elif ("2000 γρ." in name_):
            target_weight = "2000"

        #main part
        table = tables[0]  
        df = pd.DataFrame(table[1:], columns = table[0])
        df = df.applymap(lambda x: str(x).strip() if x is not None else x)
        filtered = df[df.iloc[:, 1] == target_weight]
        price_ = filtered.iloc[:, 2] .values[0]
        price_ = price_.replace(',','.')
        
    if ("ΔΕΜΑΤΩΝ" in name_):
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[10]
            tables = page.extract_tables()

        if ("0.5 κιλό" in name_):
            target_weight = "0,5"
        elif("15 κιλά" in name_):
            target_weight = "15"
        elif ("30 κιλά" in name_):
            target_weight = "30"    
        
        #main part
        table = tables[0]  
        df = pd.DataFrame(table[1:], columns = table[0])
        df = df.applymap(lambda x: str(x).strip() if x is not None else x)
        row = df[df[df.columns[0]] == target_weight]
        price_ = row.iloc[0, 1]
        price_ = price_.replace(',','.')

    print(price_)
    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(float(price_))
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("Cyprus Post")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_AHK(u):
    '''
    response = requests.get(Item_url_)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)  
    else:
        pdf_AHK = "ECOICOPv2/PDFs/AHK_Mar2024.pdf"
        with open(pdf_AHK, "wb") as f:
            f.write(response.content)
        with open(pdf_AHK, "rb") as f:
            #pdf_reader = PyPDF2.PdfReader(f)
            pdf_reader = pypdf.PdfReader(f)
            page = pdf_reader.pages[2]
            text = page.extract_text()
    '''
    pdf_AHK = "ECOICOPv2/PDFs/AHK_Mar2026.pdf"
    
    with open(pdf_AHK, "rb") as f:
        pdf_reader = pypdf.PdfReader(f)
        page = pdf_reader.pages[2]
        text = page.extract_text()
    
    lines = text.split("\n")
       
    for line in lines:
        new_row = []
        if name_ in line:
            ken = line.strip()
            match = re.search(r'\d+,\d+', ken)
            if match:     
                if "Προμήθειας" in ken:
                    price_ = float(match.group(0).replace(",","."))
                else:
                    price_ = float(match.group(0).replace(",",".")) / 100 #convert to euros  
                print(price_)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(price_)
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("AHK")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_water(u):
    
    if "Nicosia" in retailer_:
        city_ = "Nicosia"
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        print(response)
        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.find_all("table", {"width":"992"})
        text = element[0].get_text()
        prices = re.findall(r'€\s*(\d+,\d{2})', text)

        if name_ == "Πάγιο ανά μήνα":
            price_1 = prices[0].replace(",",".")
            price_ = float(price_1) / 2 #per month
        if name_ == "Κυβικά ανά μήνα":
            price_2 = prices[4].replace(",",".")
            price_ = float(price_2) / 2 #per month
    
    if "Larnaca" in retailer_:
        city_ = "Larnaca"
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        print(response)
        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.find_all("table", {"class":"table-format-left"})
        text_ = element[0].text
        element_1 = re.search(r'Πάγιο(\d+,\d+)', text_)
        element_2 = re.search(r'Δικαίωμα Συντήρησης(\d+,\d+)', text_)
        element_3 = re.search(r'1Μέχρι15(\d+,\d+)', text_)
        
        if name_ == "Πάγιο ανά μήνα":
            if element_1:
                price_1 = element_1.group(1).replace(",",".")
                price_ = float(price_1) / 3 #per month
        if name_ == "Δικαίωμα Συντήρησης ανά μήνα":
            if element_2:
                price_2 = element_2.group(1).replace(",",".")
                price_ = float(price_2) / 3 #per month
        if name_ == "Κυβικά ανά μήνα":
            if element_3:
                price_3 = element_3.group(1).replace(",",".")
                price_ = float(price_3) / 3 #per month

    if "Limassol" in retailer_:
        city_ = "Limassol"
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        print(response)
        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.find_all("div", {"class":"acd-des"})

        if name_ == "Πάγιο ανά μήνα":
            element_1 = element[2].find_all("td")
            price_1 = element_1[3].text.replace("\n","").replace(",",".")
            price_ = float(price_1) / 4 #per month
        if name_ == "Δικαίωμα Συντήρησης ανά μήνα":
            element_2 = element[2].find_all("td")
            price_2 = element_2[5].text.replace("\n","").replace(",",".")
            price_ = float(price_2) / 4 #per month
        if name_ == "Κυβικά ανά μήνα":
            element_3 = element[2].find_all("td")
            price_3 = element_3[11].text.replace("\n","").replace(",",".")
            price_ = float(price_3) / 4 #per month

    if price_:
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_ + " - " + city_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Water EOA " + city_)
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_sewerage(u):
    
    values = 0

    if "Nicosia" in retailer_:
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        print(response)
        soup = BeautifulSoup(response.content, "html.parser")
        new_row = []
        city_ = "Nicosia"
        
        if "Ετήσιο Τέλος" in name_:  
            element_ = soup.find_all("div",{"class":"elementor-element elementor-element-f737ced elementor-widget elementor-widget-text-editor"})
            element_1 = element_[0].find_all("li")
            for i in range(0, len(element_1)):
                price_amount = element_1[i].text
                match = re.search(r'€(\d+,\d+)', price_amount)
                if match:
                    value = float(match.group(1).replace(",","."))
                    values = value + values
            values = values / 3
            print(values)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_ + " - " + city_)
            new_row.append(float(values))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Sewerage EOA " + city_)
            list_.loc[len(list_)] = new_row
        
        if "Τέλος Χρήσης" in name_:
            element_ = soup.find_all("div",{"class":"elementor-element elementor-element-dbb217e elementor-widget elementor-widget-text-editor"})
            new_row = []
            for i in range(0, len(element_)):
                price_amount = element_[i].text
                match = re.search(r'(\d+)', price_amount)
                if match:
                    values = float(match.group(1)) / 100
                print(values)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_ + " - " + city_)
                new_row.append(float(values))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Sewerage EOA " + city_)
                list_.loc[len(list_)] = new_row
                      
    if "Limassol" in retailer_:
        city_ = "Limassol"
        new_row = []
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        print(response)
        soup = BeautifulSoup(response.content, "html.parser")
            
        if "Ετήσιο Τέλος" in name_:
            if "SSL handshake failed" in soup.text:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
            else:
                element_name = soup.find_all('table', {"class":"table table-striped"})
                element_name_2 = element_name[0].find_all('tr')
                element_name_2 = element_name_2[len(element_name_2) - 5]
                desired_lines = [element_name_2.find_all('td')[1].get_text(), 
                                 element_name_2.find_all('td')[2].get_text(),
                                 element_name_2.find_all('td')[3].get_text(),
                                 element_name_2.find_all('td')[4].get_text(),
                                 element_name_2.find_all('td')[5].get_text(),
                                 element_name_2.find_all('td')[6].get_text(),
                                 element_name_2.find_all('td')[7].get_text()
                                ]
                print(desired_lines)
                for lines in desired_lines:
                    value = float(lines.replace(",","."))
                    values = value + values
                values = values / len(desired_lines)
                print(values)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_ + " - " + city_)
                new_row.append(float(values))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Sewerage EOA " + city_)
                list_.loc[len(list_)] = new_row
            
        if "Τέλος Χρήσης" in name_:
            element_name = soup.find_all('table', {"class":"table table-striped"})
            element_name_2 = element_name[1].find_all('tr')
            element_name_2 = element_name_2[len(element_name_2) - 1]
            desired_lines = [element_name_2.find_all('td')[1].get_text()]
            for lines in desired_lines:
                values = float(lines.replace(",","."))
            print(values)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_ + " - " + city_)
            new_row.append(float(values))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Sewerage EOA " + city_)
            list_.loc[len(list_)] = new_row
                
    if "Larnaca" in retailer_:
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        print(response)
        soup = BeautifulSoup(response.content, "html.parser")
        new_row = []
        city_ = "Larnaca"
        
        if "Ετήσιο Τέλος" in name_: 
            number_2 = []
            sum_ = 0
            count_12 = 0
            list_target_place = ["ΛΑΡΝΑΚΑ","ΛΕΙΒΑΔΙΑ","ΟΡΟΚΛΙΝΗ","ΠΥΛΑ","ΑΡΑΔΙΠΠΟΥ","ΚΙΤΙ","ΔΡΟΜΟΛΑΓΙΑ","ΜΕΝΕΟΥ","ΠΕΡΒΟΛΙΑ","ΤΕΡΣΕΦΑΝΟΥ","ΑΓΙΟΙ ΒΑΒΑΤΣΙΝΙΑΣ","ΑΘΗΕΝΟΥ""ΑΓΓΛΙΣΙΔΕΣ","ΞΥΛΟΦΑΓΟΥ","ΞΥΛΟΤΥΜΠΟΥ","ΟΡΜΗΔΕΙΑ"]
            for kk in range(0, len(list_target_place)):
                target_cell = soup.find(string = str(list_target_place[kk]))
                if target_cell:
                    tr = target_cell.find_parent("tr")
                    numbers = []
                    current_tr = tr
                    while len(numbers) < 4: ###to lenght na einai megalitero apo oles tis times tou pinaka, grammes==16 kai stiles==4
                        tds = current_tr.find_all("td")
                        for td in tds:  #Grafoume oles tis times tis grammis
                            text = td.get_text(strip=True).replace(',', '.')
                            if re.match(r'^\d+(\.\d+)?$', text):
                                numbers.append(float(text))     
                    number_2.append(numbers[2])
            number_2 = list(set(number_2))
            for o in number_2:
                print(o)
                sum_ += o
                count_12 += 1
            print(float(sum_/count_12))
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_ + " - " + city_)
            new_row.append(float(sum_/count_12))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Sewerage EOA " + city_)
            list_.loc[len(list_)] = new_row
 
        if "Τέλος Χρήσης" in name_:
            new_row = []
            target_cell = soup.find(string="ΛΑΡΝΑΚΑ")
            if target_cell:
                tr = target_cell.find_parent("tr")
                numbers = []
                current_tr = tr
                while len(numbers) < (4*16) + 1: ###to lenght na einai megalitero apo oles tis times tou pinaka, grammes==16 kai stiles==4
                    tds = current_tr.find_all("td")
                    if tds and tds[0].get_text(strip=True) == "ΛΑΡΝΑΚΑ": #testaroume an einai i proti grammi tis larnakas
                        tds = tds[1:]
                    for td in tds:  #Grafoume oles tis times tis grammis
                        text = td.get_text(strip=True).replace(',', '.')
                        if re.match(r'^\d+(\.\d+)?$', text):
                            numbers.append(float(text))
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
            
            if numbers[3]:
                print(float(numbers[3]))
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_ + " - " + city_)
                new_row.append(float(numbers[3]))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Sewerage EOA " + city_)
                list_.loc[len(list_)] = new_row
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_toyota(u):
    
    if (name_ == "The New Toyota Yaris Cross") | (name_ == "The New Toyota Yaris") | (name_ == "Toyota Aygo X"):    
        
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs, {'headers':header})
        print(response)
        
        if response.status_code != 200:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            # Find the div with the relevant data attribute
            data_div = soup.find('div', class_='dnb-sales-hero-outer-container').find('div', attrs={'data-component-props': True})
            # Extract the value of the data-component-props attribute
            data_component_props = data_div['data-component-props']    
            # Unescape the JSON string
            data_component_props = data_component_props.replace('&quot;', '"')    
            # Parse the JSON data
            data = json.loads(data_component_props)
            # Extract the TotalPrice from financeConfig
            finance_config_str = data['salesHeroDto'].get('financeConfig', '')
            finance_config = json.loads(finance_config_str)
            price_ = finance_config.get('TotalPrice')
            print(price_)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_) 
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Toyota")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_nissan(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(Item_url_, headers=header)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("THIS IS A DEAD END..." in response.text) or (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)  
    else:
        tree = html.fromstring(response.content)
        price_tree = tree.xpath('//iframe[@id="individualVehiclePriceJSON"]/text()')
        
        if price_tree:
            price_json = price_tree[0]
            price_data = json.loads(price_json)
            if "LVL001" in name_:
                price_ = price_data["qashqai-e-power"]['default']['grades']['LVL001']['gradePrice']
            if "LVL004" in name_:
                price_ = price_data["qashqai-e-power"]['default']['grades']['LVL004']['gradePrice']
            if "LVL005" in name_:
                price_ = price_data["qashqai-e-power"]['default']['grades']['LVL005']['gradePrice']
            if name_ == "NISSAN JUKE 1.6lt 143HP N-CONNECTA 2-TONE":
                price_ = price_data["juke_2019"]['default']['grades']['LVL001']['gradePrice']
        
        print(price_)
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Nissan")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_stock_center(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    print(response)

    if (response.status_code != 200) or ("Το όχημα αυτό δεν είναι πλέον διαθέσιμο" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_price_ = soup.find_all("div",{"class":"price"})
        price_ = element_price_[0].text.replace("Τιμή μετρητοίς","").replace(" ","").replace("\t","").replace("\r","").replace("\n","").replace(".","").replace("€","")
        
        # Extract only the number
        match = re.search(r'\d+', price_)
        if match:
            price_ = int(match.group())
            print(price_)
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Stock Center")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_wolt(u):
    
    ###  without headers 
    ## 1 
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs)
    ## 2
    #response = requests.get(Item_url_)
    
    ### with headers (*NOT WORKING*)
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    ## 1 
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers':header})
    ## 2
    response = requests.get(Item_url_, headers = header) 
    ## 3 
    #with httpx.Client(headers = header) as client:
    #    response = client.get(Item_url_)
    
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all('span', {"data-test-id":"product-modal.price"})
        if element_name:
            price_ = element_name[0].text.replace("€","").replace(",",".").replace("/xa0","").replace(" ","")
            print(price_)
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Wolt")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false

def results_vassos(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs, {'headers':header}, verify=False)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all('p', {"class":"slider-text3"})
        price_ = element_name[0].text.replace("\n","").replace(" ","")
        price_ = ''.join(filter(str.isdigit, price_))
        price_ = float(price_) / 100
        
    if price_:
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Vassos Psarolimano")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(comidity_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_meze(u):

    # Open PDF
    reader = PdfReader("ECOICOPv2/PDFs/MEZE-TAVERNA-ENGLISH-MENU-Jun2026.pdf")
                
    # Extract text from pages 3 and 4 (the prices of meat and fish meze are displayed in page 3 and 4, respectively)
    text_page3 = reader.pages[3].extract_text()
    text_page4 = reader.pages[4].extract_text()

    # Product names
    product1 = "MEAT MEZE"
    product2 = "FISH MEZE"

    # Search patterns: product name followed by a price
    pattern1 = rf"{re.escape(product1)}.*?(\d+[.,]\d{{2}})"
    pattern2 = rf"{re.escape(product2)}.*?(\d+[.,]\d{{2}})"

    # Extract prices
    match1 = re.search(pattern1, text_page3, re.DOTALL)
    match2 = re.search(pattern2, text_page4, re.DOTALL)

    price1 = match1.group(1) if match1 else None
    price2 = match2.group(1) if match2 else None
    
    if "Meat Meze" in name_ :
        price_ = price1
    
    if "Fish Meze" in name_ :
        price_ = price2

    print(price_)
    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(price_)
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("Meze Tavern")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_pydixa(u):
    
    pdf_pixida = "ECOICOPv2/PDFs/Pixida-Nic-En-2025-May.pdf"
    
    '''
    response = requests.get(Item_url_)
    print(response)
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
    with open(pdf_pixida, "wb") as f:
        f.write(response.content)
    '''
    with pdfplumber.open(pdf_pixida) as pdf:
        page = pdf.pages[4]  
        text = page.extract_text()

    matches = re.findall(r'Ψαρομεζές .*?(\d+\.\d+)', text)
    price_ = float(matches[0])
    
    if matches:
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))        
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Pyxida")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_ithaki(u):
    
    pdf_ithaki = "ECOICOPv2/PDFs/ithaki-2025.pdf"

    with pdfplumber.open(pdf_ithaki) as pdf:
        first_page = pdf.pages[5]
        text = first_page.extract_text()
        
    pattern = r'(\d+.*?\d+\.\d{2})'
    matches = re.findall(pattern, text)
    
    for match in matches:
        new_row = []
        website_false = []
        
        if ("Ποικιλία Κρεατικών" in match) and ("Ποικιλία Κρεατικών για 2 άτομα - Larnaca"== name_):
            pattern = r'€(\d+\.\d{2})'
            price_ = re.findall(pattern, match)
            if price_:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_[0]))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Ithaki")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        
        elif ("Ποικιλία Θαλασσινών" in match) and ("Ποικιλία Θαλασσινών για 2 άτομα - Larnaca"==name_):
            pattern = r'€(\d+\.\d{2})'
            price_ = re.findall(pattern, match)
            if price_:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_[0]))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Ithaki")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)

def results_flames(u):

    #Mixed Grill 
    if name_ == "Mixed Grill for 2 persons - Famagusta":
        pdf_flames1 = "ECOICOPv2/PDFs/flames-grill-specialities-Mar2024.pdf"
    
        with pdfplumber.open(pdf_flames1) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()

        lines = text.split('\n')
        desired_line = None
    
        for line in lines:
    
            if "Mixed Grill" in line:
                desired_line = line.strip()  
    
        if desired_line:
            pattern = r'(\d+\.\d{2})$'
            price_ = re.findall(pattern, desired_line)

    #Flames Special Cyprus (Meze)
    if name_ == "Meat Meze for 2 persons - Famagusta":
        pdf_flames2 = "ECOICOPv2/PDFs/flames-cyprus-dishes-Mar2024.pdf"
    
        with pdfplumber.open(pdf_flames2) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
    
        lines = text.split('\n')
        desired_line = None
    
        for line in lines:
    
            if "Flames Special Cyprus (Meze)" in line:
                position = lines.index("Flames Special Cyprus (Meze)")
                correct_line = lines[position+1]
                desired_line = correct_line.strip()  
    
        if desired_line:
            pattern = r'(\d+\.\d{2})$'
            price_ = re.findall(pattern, desired_line)

    if price_:
        print(float(price_[-1]))
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_[-1]))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Flames")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_mageirisses(u):
    
    #pdf_url = "https://oimageirisses.com/wp-content/uploads/assets/menu-gr.pdf"
    pdf_mageirisses = "ECOICOPv2/PDFs/Mageirisses-Menu-Jun2026.pdf"
        
    reader = PdfReader(pdf_mageirisses)
    all_text = ""
    
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            all_text += page_text + "\n"
        
    pattern = r"Μικρός\s+Μεζές\s+([0-9]+,[0-9]{2})"
    match = re.search(pattern, all_text)
        
    if match:
        value = match.group(1)
        price_ = float(value.replace(',','.'))
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Mageirisses")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    
def results_pagkratios(u):

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, headers=header)
    print(response)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all("span", {"class":"price_item"})
        price_ = element_[0].text.replace("€","")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Pagkratios")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)
    else:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

def results_christos_grill_seafood(u):
    
    pdf_path = "ECOICOPv2/PDFs/Christos_JUN2025.pdf"

    with pdfplumber.open(pdf_path) as pdf:
        
        if len(pdf.pages) >= 9:
            page9 = pdf.pages[8]  
            text = page9.extract_text()
            match = re.search(r"Seafood Platter MEZE for 2 persons\s+(\d+(?:\.\d+)?)", text)
            
            if match:
                price = match.group(1)
                price_ = float(price)/2

            if price_:
                print(price_)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Christos Grill&Seafood")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
            
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false

def results_netflix(u):
    
    header = { "User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
    print(response)

    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

    else:
        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        search_text = "Pricing (Euro)"
        prices = re.findall(r'(\d+\.\d+)', text)

        #Basic
        if 'Basic' in name_:
            price_ = float(prices[0])

        #Standard
        if 'Standard' in name_:
            price_ = float(prices[1])
        print(price_)

        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Netflix")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)

def results_driving_school(u):  
    
    header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
    print(response)
    soup = BeautifulSoup(response.text, "html.parser")

    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

    else:
        element_ = soup.find_all('div',{"class":"two-columns-text-subtitle-left-right-area"})
        text = element_[0].text
        #truck = text[text.find("Φορτηγό/Λεωφορείο: €") + len("Φορτηγό/Λεωφορείο: €"):].split("\n")[0].strip()
        #trailer = text[text.find("Νταλίκα: €") + len("Νταλίκα: €"):].split("\n")[0].strip()
        
        if 'Αυτοκίνητο' in name_: 
            car = text[text.find("Αυτοκίνητο: €") + len("Αυτοκίνητο: €"):].split("\n")[0].strip()
            price_ = float(car)
            print("Αυτοκίνητο:", car)
        if 'Μοτοσυκλέτα' in name_:
            motorcycle = text[text.find("Μοτοσυκλέτα: €") + len("Μοτοσυκλέτα: €"):].split("\n")[0].strip()
            price_ =float (motorcycle)
            print("Μοτοσυκλέτα:", motorcycle)

        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Larnaca Driving School")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)        
 
def results_dentist(u):
    
    header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
    print(response)
    soup = BeautifulSoup(response.text, "html.parser")
    response = requests.get(Item_url_)

    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

    else:        
        # Βρίσκει όλα τα rows του πίνακα
        rows = soup.find_all("tr")
        
        for row in rows:
            ths = row.find_all("th")
            if len(ths) >= 2:
                title = ths[0].get_text(strip=True)
        
                if ("Φθορίωση (παιδιά 6 – 15 χρ.)" in title) and ('In office fluoride application (children 6 -15 yrs)' in name_):
                    price = ths[1].get_text(strip=True)
                    price_ = float(price)
                    print("Τιμή:", price_)
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)  
                    new_row.append("Dr Stephanos Tsitsis Dental Surgeon")
                    list_.loc[len(list_)] = new_row
                    list_["Name"] = list_["Name"].apply(lambda x:x)

                if ("Προληπτική Έμφραξη (παιδιά 6 – 13 χρ.)" in title) and ('Sealant (children 6 - 12 yrs)' in name_):
                    price = ths[1].get_text(strip=True)
                    price_ = float(price)
                    print("Τιμή:", price_)
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)  
                    new_row.append("Dr Stephanos Tsitsis Dental Surgeon")
                    list_.loc[len(list_)] = new_row
                    list_["Name"] = list_["Name"].apply(lambda x:x)

                if ("Καθαρισμός Δοντιών (Αποτρύγωση)" in title) and ('Teeth cleaning' in name_):
                    price = ths[1].get_text(strip=True)
                    price_ = float(price)
                    print("Τιμή:", price_)
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)  
                    new_row.append("Dr Stephanos Tsitsis Dental Surgeon")
                    list_.loc[len(list_)] = new_row
                    list_["Name"] = list_["Name"].apply(lambda x:x)
                
                if ("Εξέταση ασθενούς - Διάγνωση" in title) and ('Examination - Diagnosis' in name_):
                    price = ths[1].get_text(strip=True)
                    price_ = float(price)
                    print("Τιμή:", price_)
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)  
                    new_row.append("Dr Stephanos Tsitsis Dental Surgeon")
                    list_.loc[len(list_)] = new_row
                    list_["Name"] = list_["Name"].apply(lambda x:x)

                if ("Ψηφιακή Ενδοστοματική Ακτινογραφία" in title) and ('Digital intraoral X-ray' in name_):
                    price = ths[1].get_text(strip=True)
                    price_ = float(price)
                    print("Τιμή:", price_)
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)  
                    new_row.append("Dr Stephanos Tsitsis Dental Surgeon")
                    list_.loc[len(list_)] = new_row
                    list_["Name"] = list_["Name"].apply(lambda x:x)

                if ("Έμφραξη μιας επιφάνειας" in title) and ('One surface filling' in name_):
                    price = ths[1].get_text(strip=True)
                    price_ = float(price)
                    print("Τιμή:", price_)
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)  
                    new_row.append("Dr Stephanos Tsitsis Dental Surgeon")
                    list_.loc[len(list_)] = new_row
                    list_["Name"] = list_["Name"].apply(lambda x:x)

                if ("Εξαγωγή δοντιού ή απλής ρίζας" in title) and ('Tooth extraction' in name_):
                    price = ths[1].get_text(strip=True)
                    price_ = float(price)
                    print("Τιμή:", price_)
                    new_row.append(datetime.now().strftime('%Y-%m-%d'))
                    new_row.append(name_)
                    new_row.append(float(price_))
                    new_row.append(subclass_)
                    new_row.append(division_)  
                    new_row.append("Dr Stephanos Tsitsis Dental Surgeon")
                    list_.loc[len(list_)] = new_row
                    list_["Name"] = list_["Name"].apply(lambda x:x)

def results_ugraerio(u):
    
    pdf_path = "ECOICOPv2/PDFs/paratiritirio/paratiritirio_may_2026.pdf"
    all_rows = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            
            if not text:
                continue
            lines = text.split("\n")
    
    pattern = re.compile(r"ΚΥΛΙΝΔΡΟΣ\s*10kg", re.IGNORECASE)
    
    for item in lines:
        
        if isinstance(item, str) and pattern.search(item):
            parts = item.split()
    
            try:
                price_ = float(parts[-1])
                print("Μέση τιμή:", price_)
            
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)  
                new_row.append("Price Observatory - Consumer Protection Service")
                list_.loc[len(list_)] = new_row
                list_["Name"] = list_["Name"].apply(lambda x:x)
    
            except:
                print("FOUND BUT PARSING ERROR:", item)
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
                    
def results_teacher_finder(u):
    
    response = requests.get(Item_url_)
    print(response)

    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

    else:
        soup = BeautifulSoup(response.text, "html.parser") 
        element_ = soup.find_all('div', {'class':'no-s col-12 col-sm-12 col-md-12 col-lg-12'})
        
        values_ = 0
        count_ = 0
        for i in range(len(element_)):
            if i % 2 == 0:
                pass
            else:
                text = element_[i].text
                result_ = re.findall(r'\d+', text)[0]
                values_ = values_+ float(result_)
                count_ += 1
        
        price_ = values_ / count_
        print("Μέση Τιμή:", price_)

        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Teacher Finder")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)

def results_digicare(u):
    
    header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)

    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

    else:
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all('table', {'class': 'w-full border-collapse text-sm'})
        
        if ('Εμβόλιο - Ενήλικη Ετήσια - Βασικός Συνδυασμός' in name_):
            table = tables[0]
        elif ("Τακτικός έλεγχος" in name_) or ("Αποπαρασίτωση" in name_):
            table = tables[3]    

        for row in table.find_all('tr'):
            cols = row.find_all(['td', 'th'])
            cells = [c.get_text(strip=True) for c in cols]
    
            #dog regular check-up
            if (cells and "Τακτικός έλεγχος" in cells[0]) and ('Σκύλος' in name_) and ("Τακτικός έλεγχος" in name_):
                values_after = cells[2] 
                first_value = int(values_after.replace('€','').split("–")[0])
                second_value = int(values_after.replace('€','').split("–")[1])
                price_ = (first_value + second_value) / 2
                print(price_)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)  
                new_row.append("DigiCare")
                list_.loc[len(list_)] = new_row
                list_["Name"] = list_["Name"].apply(lambda x:x) 
        
            #cat regular check-up
            elif (cells and "Τακτικός έλεγχος" in cells[0]) and ('Γάτα' in name_) and ("Τακτικός έλεγχος" in name_):
                values_after = cells[4]
                first_value = int(values_after.replace('€','').split("–")[0])
                second_value = int(values_after.replace('€','').split("–")[1])
                price_ = (first_value + second_value) / 2
                print(price_)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)  
                new_row.append("DigiCare")
                list_.loc[len(list_)] = new_row
                list_["Name"] = list_["Name"].apply(lambda x:x) 
        
            #dog deworming
            elif (cells and "Αποπαρασίτωση (2 φορές/χρόνο)" in cells[0]) and ('Σκύλος' in name_) and ("Αποπαρασίτωση" in name_):
                values_after = cells[2]
                first_value = int(values_after.replace('€','').split("–")[0])
                price_ = float(first_value)
                print(price_)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)  
                new_row.append("DigiCare")
                list_.loc[len(list_)] = new_row
                list_["Name"] = list_["Name"].apply(lambda x:x) 
        
            #cat deworming
            elif (cells and "Αποπαρασίτωση (2 φορές/χρόνο)" in cells[0]) and ('Γάτα' in name_) and ("Αποπαρασίτωση" in name_):
                values_after = cells[4]
                first_value = int(values_after.replace('€','').split("–")[0])
                price_ = float(first_value)
                print(price_)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)  
                new_row.append("DigiCare")
                list_.loc[len(list_)] = new_row
                list_["Name"] = list_["Name"].apply(lambda x:x) 

            #dog/cat vaccination
            elif (cells and 'Βασικός συνδυασμός' in cells[0]) and ('Εμβόλιο - Ενήλικη Ετήσια - Βασικός Συνδυασμός' in name_):
                values_after = cells[2] 
                first_value = int(values_after.replace('€','').split("–")[0])
                second_value = int(values_after.replace('€','').split("–")[1].replace(' τον χρόνο',''))
                price_ = (first_value + second_value) / 2
                print(price_)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)  
                new_row.append("DigiCare")
                list_.loc[len(list_)] = new_row
                list_["Name"] = list_["Name"].apply(lambda x:x) 

def results_pluton_travel(u):
    
    header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)

    else:
        soup = BeautifulSoup(response.text, "html.parser")
        element_ = soup.find_all('div', {'class':'price-wrap eq-height3'})
        
        values_ = 0
        count_ = 0
        for i in range(0, len(element_)):
            text_ = element_[i].text
            match = re.search(r'€\s*(\d+)', text_)
            result_ = int(match.group(1))
            count_ += 1
            values_ = values_ + result_  
        
        price_ = values_ / count_
        print("Μέση Τιμή:", price_)  

        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Pluton Travel")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)

def results_xeyes(u):

    response = requests.get(Item_url_)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('span', {'class':'money'})
        price_ = element_[0].text.replace("€","")
        print("Τιμή:", price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("X-Eyes")
        list_.loc[len(list_)] = new_row

def results_alex(u):

    response = requests.get(Item_url_)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find('span', {'class':'price-item price-item--regular'}).get_text(strip=True)
        price_ = element_.replace("€","").replace(",",".")
        print("Τιμή:", price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Alex Optical")
        list_.loc[len(list_)] = new_row

def results_mesmer(u):

    header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('span', {'class':'woocommerce-Price-amount amount'})
        price_ = element_[0].text.replace("\xa0","").replace("€","").replace(",",".")
        print("Τιμή:", price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Mesmer Eyes")
        list_.loc[len(list_)] = new_row

def results_zouvanis(u):

    response = requests.get(Item_url_)
    print(response)
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('span', {'class':'money'})
        price_ = element_[0].text.replace("€","").replace(",",".")
        print("Τιμή:", price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Zouvanis Optics")
        list_.loc[len(list_)] = new_row        
        
def results_tsiropoulos(u):
    
    response = requests.get(Item_url_)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        element_ = soup.find_all('span', {'class':'woocommerce-Price-amount amount'})
        price_ = element_[0].text.replace("\xa0","").replace("€","").replace(",",".")
        print("Τιμή:", price_)  
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Tsiropoulos Jewelry")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)

def results_constantinou(u):
    
    response = requests.get(Item_url_)
    
    #header = {"User-Agent": "Mozilla/5.0"}
    #response = requests.get(Item_url_, headers = header)
    
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        element_ = soup.find_all('span', {'class':'woocommerce-Price-amount amount'})
        price_ = element_[4].text.replace("\xa0","").replace("€","").replace(",",".")
        print("Τιμή:", price_)  
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Constantinou Jewels")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)        
        
def results_melekkis(u):
    
    response = requests.get(Item_url_)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        #The price is not displayed in the visible HTML. Instead, it is stored inside the data-wmc_price_cache attribute as a JSON string.
        cache = json.loads(
            soup.find("span", class_ = "wmc-price-cache-list")["data-wmc_price_cache"])
        eur_html = cache["EUR"]
        price_ = re.search(r'>(\d+(?:\.\d+)?)<', eur_html).group(1)
        print("Τιμή:", price_)  
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Panos Melekkis Jewellery")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)
       
def results_brilliance(u):
    
    response = requests.get(Item_url_)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('span', {'class':'woocommerce-Price-amount amount'})
        price_ = element_[0].text.replace("\xa0","").replace("€","").replace(",",".")
        print("Τιμή:", price_)  
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Brilliance Jewellery")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)       
        
def results_aphrodite(u):
    
    header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('span', {'class':'woocommerce-Price-amount amount'})
        price_ = element_[1].text.replace("€","")
        print("Τιμή:", price_)  
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Aphrodite Jewellery")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)       
        
def results_pharmfetch(u):
    
    response = requests.get(Item_url_)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('span', {'class':'woocommerce-Price-amount amount'})
        price_ = element_[4].text.replace("€","")
        print("Τιμή:", price_)  
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("PHARMFETCH")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)
        
def results_remedy(u):
    
    response = requests.get(Item_url_)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('span', {'class':'woocommerce-Price-amount amount'})
        price_ = element_[0].text.replace("€","").replace(",",".")
        print("Τιμή:", price_)  
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Remedy")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x) 
        
def results_24evexia(u):
    
    header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('h2', {'class':'final-price'})
        price_ = element_[0].text.replace("€","")
        print("Τιμή:", price_)  
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("24evexia")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)         

def results_agathokleous(u):
    
    header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        element_ = soup.find_all('span', {'class':'woocommerce-Price-amount amount'})
        price_ = element_[0].text.replace("\xa0","").replace("€","").replace(",",".")
        print("Τιμή:", price_)  
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Agathokleous Pharmacies")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x) 
        
def results_procopiou(u):
    
    header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
    print(response)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        
        if ("Nebuliser Gem" in soup.text) or ("EASYCHECK" in soup.text) or ("Fingertip" in soup.text) :
            element_ = soup.find_all('span', {'class':'RobotoBold size20 ma5 col_df1800'})
        else:
            element_ = soup.find_all('span', {'class':'RobotoBold size20 ma3 col_18984f'})
        
        price_ = element_[0].text.replace("€","")
        print("Τιμή:", price_)  
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Procopiou Medishop")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)  

#Initialization of the scraping/processing time
start_time = time.time()

# Run the web-scraping code
for u in range(0, len(urls)):
    print(u)
    
    # Create a new row each time 
    new_row = []
    website_false = []
    
    # Read the data
    Item_url_ = urls["Url"].iloc[u]
    name_ = urls["Name"].iloc[u]
    print(name_)
    subclass_ = urls["Subclass"].iloc[u]
    division_ = urls["Division"].iloc[u]
    retailer_ = urls["Retailer"].iloc[u]
     
    #if retailer_=="SupermarketCy": #*Run only locally
    #    results_supermarketcy(u) 
    if retailer_=="Fuel Daddy":
        results_fueldaddy(u)
    if retailer_=="Costas Theodorou":
        results_costastheodorou(u)
    if retailer_=="Parga":
        results_parga(u)    
    if retailer_=="Leroy Merlin":
        results_leroymerlin(u)   
    if retailer_=="IKEA":
        results_ikea(u)
    #if retailer_=="Stephanis": #*Run only locally
    #    results_stephanis(u)
    if retailer_=="Public": #*Run only locally by 05/03/2026. Activated again and run globally (GitHub) in 06/03/26.
        results_public(u)
    if retailer_=="Electroline":
        results_electroline(u)
    if retailer_=="CYTA":
        results_cyta(u)
    #if retailer_=="Cablenet": #*Run only locally
    #    results_cablenet(u)  
    if retailer_=="Primetel": 
        results_primetel(u)    
    if retailer_=="Epic":
        results_epic(u)
    if retailer_=="Athlokinisi":
        results_Athlokinisi(u)
    #if retailer_=="Famous Sports": #*Run only locally since 09/04/26
    #    results_famousports(u) 
    if retailer_=="Marks&Spencer":
        results_Marks_Spencer(u)    
    if retailer_=="Novella": #*Deactivated in 27/12/2025 and activated again in 03/01/26
        results_novella(u) 
    if retailer_=="Hairspray":
        results_hairspray(u)
    if retailer_=="Studio 37 For Hair":
        results_studio37(u) 
    if retailer_=="Magdas Hair Boutique":
        results_magdas(u)
    if retailer_=="Douce et Belle":
        results_douce_et_belle(u)       
    if retailer_=="Akentia":
        results_akentia(u)    
    if retailer_=="Premier Laundry":
        results_premier(u)
    if retailer_=="Music Avenue": #*Deactivated in 17/05/2026 due to scraping errors. Then, run only locally.
        results_musicavenue(u)    
    if retailer_=="Rio Cinema":
        results_rio(u)    
    if retailer_=="Cyprus Ministry of Education, Sport and Youth":
        results_CyMinistryEducation(u)
    if retailer_=="European University Cyprus":
        results_EUC(u)    
    if retailer_=="Cyprus Post":
        results_CyPost(u)
    if retailer_=="AHK":
        results_AHK(u)
    if retailer_=="Water EOA Larnaca":
        results_water(u)
    #if retailer_=="Water EOA Nicosia": #*EOA Nicosia was deactivated from 17/10/25 to 04/03/26 since it banned access (https://ndlgo.org.cy/water-supply/consumer/water-fees-wbn/)
    #   results_water(u)
    if retailer_=="Water EOA Limassol":  #*EOA Limassol was diactivated in 13/03/26 because of connection error (https://eoalemesos.org.cy/el/fees) 
       results_water(u)    
    if retailer_=="Sewerage EOA Larnaca": 
        results_sewerage(u)   
    #if retailer_=="Sewerage EOA Nicosia": #*EOA Nicosia was diactivated from 17/10/25 to 04/03/26 since it banned access (https://ndlgo.org.cy/sewage/sewer-fees/) 
    #    results_sewerage(u)  
    if retailer_=="Sewerage EOA Limassol":  #*EOA Limassol was diactivated in 13/03/26 because of connection error (https://eoalemesos.org.cy/el/fees) 
        results_sewerage(u)     
    #if retailer_=="MotoRace": #*Deactivated in 21/10/25 (run only locally) and banned access in 07/11/25 (don't run neither locally) through a 'verifying you are human' check. Then, allows access locally since 28/11/25.
    #    results_moto_race(u)
    if retailer_=="AWOL":
        results_awol(u)    
    if retailer_=="Toyota": #*Deactivated in 10/12/25 due to scraping error
        results_toyota(u)    
    if retailer_=="Nissan":
        results_nissan(u)
    if retailer_=="Stock Center":
        results_stock_center(u)    
    if retailer_=="Alter Vape": 
        results_AlterVape(u)    
    if retailer_=="The CYgar shop":
        results_CYgar_shop(u)
    if retailer_=="The Royal Cigars":
        results_royal_cigars(u)  
    if retailer_=="E-wholesale":
        results_ewholesale(u)    
    if retailer_=="Hotbox Cy":
        results_hotboxcy(u)
    if retailer_=="Wolt":
        results_wolt(u)
    if retailer_=="Vassos Psarolimano":
        results_vassos(u)
    if retailer_=="Meze Tavern":
        results_meze(u)    
    if retailer_=="Pyxida":
        results_pydixa(u)
    if retailer_=="Ithaki":
        results_ithaki(u)
    if retailer_=="Flames":
        results_flames(u)
    if retailer_=="Mageirisses":
        results_mageirisses(u)    
    if retailer_=="Pagkratios": #*Deactivated in 16/11/25 due to maintenance reasons and activated in 01/12/2025
        results_pagkratios(u)
    if retailer_=="Christos Grill&Seafood":
        results_christos_grill_seafood(u)    
    #if retailer_=="Intercity Buses": #*Run only locally by 29/05/26. Then, banned access (Error 403).
    #    results_intercity_buses(u)  
    if retailer_=="Cyprus Transport":
        results_cyprus_transport(u)
    if retailer_=="Max 7 Taxi":
        results_max_7_taxi(u)
    # New Retailers
    if retailer_=="Netflix":
        results_netflix(u)
    if retailer_=="Larnaca Driving School":
        results_driving_school(u)    
    if retailer_=="Dr Stephanos Tsitsis Dental Surgeon":
        results_dentist(u)
    if retailer_=="Price Observatory - Consumer Protection Service":
        results_ugraerio(u)  
    if retailer_=="Teacher Finder":
        results_teacher_finder(u)
    if retailer_=="DigiCare":
        results_digicare(u)    
    if retailer_=="Pluton Travel":
        results_pluton_travel(u)
    # New Optical Houses
    if retailer_=="X-Eyes":
        results_xeyes(u)
    if retailer_=="Alex Optical":
        results_alex(u)
    if retailer_=="Mesmer Eyes":
        results_mesmer(u)   
    if retailer_=="Zouvanis Optics":
        results_zouvanis(u)    
    # New Jewelleries
    if retailer_=="Tsiropoulos Jewelry":
        results_tsiropoulos(u)
    if retailer_=="Constantinou Jewels":
        results_constantinou(u)
    if retailer_=="Panos Melekkis Jewellery":
        results_melekkis(u)  
    if retailer_=="Brilliance Jewellery":
        results_brilliance(u) 
    if retailer_=="Aphrodite Jewellery":
        results_aphrodite(u)
    # New Pharmacies
    if retailer_=="PHARMFETCH":
        results_pharmfetch(u) 
    if retailer_=="Remedy":
        results_remedy(u) 
    #if retailer_=="Procopiou Medishop": #*Deactivated in 24/06/36 because of 401 error ("unauthenticated": you are either not logged in, your session expired, or you provided the wrong credentials, and the server expects you to retry with the correct details)
    #    results_procopiou(u) 
    if retailer_=="Agathokleous Pharmacies":
        results_agathokleous(u)
    if retailer_=="24evexia":
        results_24evexia(u)         
   
# Total computational/processing time
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time/60, "minutes")

# Change the type as float
list_["Price"].astype(float)

# Export/Save the scraped data 
df.to_csv("ECOICOPv2/Datasets/Raw-Data/Raw-Data-2-2026Q3.csv", index=False) 
combined_df = pd.concat([df, list_], axis=0)
combined_df.reset_index(drop=True, inplace=True)
combined_df.sort_values(["Date", "Retailer"])
combined_df.to_csv("ECOICOPv2/Datasets/Raw-Data/Raw-Data-2-2026Q3.csv", index=False, header=True)
# Export/Save the unscraped data (daily errors) 
daily_errors.to_csv("ECOICOPv2/Datasets/Daily-Scraping-Errors.csv", index=False)
