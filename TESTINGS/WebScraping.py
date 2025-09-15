# Important libraries 
import pandas as pd 
import re
import requests
import time
import xlsxwriter
import urllib.request
import json
import tabula as tb
#import PyPDF2
import pypdf
import warnings
import matplotlib.pyplot as plt
import numpy as np
import pdfplumber
import httpx

from ast import Try
from lxml import html, etree
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.error import URLError
from tabula import read_pdf
from docx import Document

# Ignore specific warning
warnings.simplefilter("ignore")

# Read necessary data
df = pd.read_csv("Datasets/Raw-Data-2025Q3.csv")
#df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y").dt.strftime("%Y-%m-%d")
df = df.sort_values("Date")

#df = pd.read_csv("Datasets/Raw-Data.csv")
urls = pd.read_csv("Datasets/Products-Urls.csv")

# Create a null dataframe
daily_errors = pd.DataFrame(columns=["Name","Subclass","Url","Division","Retailer"])
list_ = pd.DataFrame(columns=["Date","Name","Price","Subclass","Division","Retailer"])

# Define the functions for the web-scraping of the target retailers

def results_supermarketcy(u):
    
    url_new = "https://www.supermarketcy.com.cy/" + Item_url_
    
    ###  without headers 
    
    ## 1 (*NOT working*)
    #bs = BeautifulSoup(url_new, "html.parser")
    #response = requests.get(bs)

    ## 2 (*NOT working*)
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
    ## 1 (*NOT working*)
    #bs = BeautifulSoup(url_new, "html.parser")
    #response = requests.get(bs, {'headers':header})
    
    ## 2 (*NOT working*)
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

def results_metro(u):
    
    #website: "https://wolt.com/en/cyp/larnaca/venue/metro-larnaca/" 
    response = requests.get(Item_url_)
    soup = BeautifulSoup(response.text, 'html.parser')
    element_ = soup.find_all("span", {"data-test-id":"product-modal.price"})
    
    if (response.status_code != 200) or (element_ == []) :
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        price_ = element_[0].text.replace('€','').replace(',','.').replace('/kg','')
        print(price_)
            
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("METRO")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)  

def results_alphamega(u):

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    #header = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(Item_url_, headers = header)
           
    if (response.status_code != 200) or ("Η σελίδα δεν βρέθηκε" in response.text) or ("Η σελίδα αφαιρέθηκε" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.content, "html.parser")
        '''
        element_soup = soup.find_all("div",{"class":"content-row__item__body padding-size-none padding-position-around margin-sm margin-position- dw-mod"})
        # Extract the script tag content
        script_tag = element_soup[0].find('script')
        if script_tag:
            script_content = script_tag.string or script_tag.get_text()
            # Use regex to extract 'ecomm_totalvalue'
            match = re.search(r"'ecomm_totalvalue':\s*([\d.]+)", script_content)
            if match:
                price_= float(match.group(1))
                print(price_)
        '''
        element_soup = soup.find("span",{"class":"text-price fs-5"}).text.strip()
        price_ = element_soup.replace('€', '').replace(',', '.').strip()
        print(price_)
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Alphamega")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)  

def results_fueldaddy(u):
    
    url_new = "https://www.fueldaddy.com.cy/" + Item_url_
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'}
    
    response = requests.get(url_new, headers=header)
        
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
            
        name = element_soup[0].find_all("div",{"class" : "col-sm-9"})
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

def results_ikea(u):
    '''
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)  

    if (response.status_code != 200) or ("ERROR 404" in response.text) or ("μήπως κάτι λείπει;" in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
        
    else:
        if ("Προσθήκη στο καλάθι" in response.text) or ("Ενημέρωση διαθεσιμότητας" in response.text):
            soup = BeautifulSoup(response.content, "html.parser")
            element_soup = soup.find_all("span",{"class":"price__sr-text"})
        
            if (element_soup):
                element_soup_1=element_soup[0]
                element_soup_2=element_soup_1.text
                element_soup_3 = element_soup_2.replace('€', '').replace(",",".").strip()
                if "Τρέχουσα τιμή" in element_soup_3:
                    element_soup_3=element_soup_3.replace("Τρέχουσα τιμή  ","").replace(",",".")
            
                if "Αρχική τιμή" in element_soup_3:
                    element_soup_3=element_soup_3.replace("Αρχική τιμή  ","").replace(",",".")
                
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(element_soup_3))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("IKEA")
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
    '''
    ## 1st way (without header)
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)  
    
    ## 2nd (with header) 
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    #response = requests.get(Item_url_, headers=header)

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
        #soup = BeautifulSoup(response.text, "html.parser")
        element_soup = soup.find_all("span",{"class":"price__sr-text"})
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
                     
def results_stephanis(u):

    ## with headers 
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    # 1 (*NOT working*)
    response = requests.get(Item_url_, headers = header)
    # 2 (*NOT working*)
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers':header})
    # 3 (*NOT working*)
    #with httpx.Client(headers = header) as client:
    #    response = client.get(Item_url_)
    
    ## without headers
    # 1 (*NOT working*)
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs) 
    # 2 (*NOT working*)
    #response = requests.get(Item_url_)

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
        if (len(element_soup) < 2):
            element_soup = element_soup[0]
        else:
            element_soup = element_soup[1]
        price_ = element_soup.text.replace("€","").replace("\n","")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Stephanis")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_cyta(u):
    '''
    q=0
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    
    if (response.status_code==200):
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Wired/Wireless telephone services	
        element_soup = soup.find_all("div",{"class":"table-responsive"})
        for o in range(0,len(element_soup)):
            if "Κλήσεις προς" in element_soup[o].text:
                element_ = element_soup[o]
                element_soup_1 = element_.find_all("td")
                for p in range(0, len(element_soup_1)):
                    ken=element_soup_1[p].text
                    if (ken==name_):
                        price_=element_soup_1[p+1].text.replace("€","").replace(",",".").replace(" /λεπτό","")
                        q=1
        
        # Internet access provision services	
        if (q==0):
            element_soup = soup.find_all("div",{"class":"card-body px-1"})
            qq=0
            for o in range(0,len(element_soup)):
                text = element_soup[o].get_text()
                price_pattern = r'€(\d+(?:,\d+)?)' 
                matches = re.findall(price_pattern, text)
            
                if (matches) and (qq==0):
                    price_ = matches[0].replace(",",".")
                    qq=1
                    q=1
        
        # Bundled telecommunication services
        if (q==0):
            element_soup = soup.find_all("h4",{"class":"text-24 text-center mb-0 pb-0"})
            text = element_soup[0].get_text()
            price_pattern = r'€(\d+(?:,\d+)?)'  
            matches = re.findall(price_pattern, text) 

            if matches:
                price_ = matches[0].replace(",",".")
    '''
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    
    if (response.status_code == 200):
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Wired/Wireless telephone services	
        if (name_=="Κλήσεις προς σταθερό") | (name_=="Κλήσεις προς κινητό") :
            element_soup = soup.find_all("div",{"class":"table-responsive"})
            element_ = element_soup[1].text
            prices_ = re.findall(r'€(\d+,\d+)', element_)
            if name_=="Κλήσεις προς σταθερό":
                price_ = prices_[0].replace(",",".")
                print(price_)
            if name_=="Κλήσεις προς κινητό":
                price_ = prices_[3].replace(",",".")
                print(price_)
                
        # Internet access provision services	
        elif name_=="Mobile Internet Home 1" :
            element_soup = soup.find_all("div",{"class":"card-body px-1"})
            element_ = element_soup[0].text
            prices_ = re.findall(r'€(\d+,\d+)', element_)
            price_ = prices_[0].replace(",",".")
            print(price_)
            
        # Bundled telecommunication services
        elif name_=="FREEDOM" :
            element_soup = soup.find_all("h4",{"class":"text-24 text-center mb-0 pb-0"})
            element_ = element_soup[0].text
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
        #Bundled telecommunication services
        if name_ == "5G Unlimited Max Plus":
            element_ = soup.find_all("div",{"class":"price"})
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
            element_ = soup.find_all("div",{"class":"price"})
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
        
        #Wireless and Wired telephone services
        if name_ == "To fixed telephony lines of other providers":
            element_ = soup.find_all("table",{"class":"yellow-top-zebra"})
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
            element_ = soup.find_all("table",{"class":"yellow-top-zebra"})
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
        
        #Internet access provision services    
        if name_ == "Broadband Homebox 1":
            element_ = soup.find_all("table",{"class":"yellow-top"})
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
            element_ = soup.find_all("table",{"class":"yellow-top"})
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
        
        if name_ == "Broadband Homebox 3":
            element_ = soup.find_all("table",{"class":"yellow-top"})
            data = element_[0].text.replace("€","")
            pattern = r"Monthly Fee.*?\n(\d+\.\d+)\n(\d+\.\d+)\n(\d+\.\d+)$" #1st, 2nd, and 3rd values
            match = re.search(pattern, data, re.MULTILINE)
            if match:
                value = match.group(3) # Extract the captured group (3rd value)
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

def results_Athlokinisi(u):
    
    url = "https://athlokinisi.com.cy" + Item_url_
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
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
            price_=float(element_soup[0].text.strip().replace("€",""))
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Athlokinisi")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_awol(u):
    
    p=0
    price_="0"
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    url="https://www.awol.com.cy/"+Item_url_
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    element_soup = soup.find_all("span",{"class":"price price--sale"})
    
    if element_soup:
        p=0
    else:
        element_soup = soup.find_all("span",{"class":"price"})   
        
    if ((response.status_code !=200) or ("Page Not Found" in response.text)):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x) 
    else:
        if element_soup[0] is not None:
            amounts_list = element_soup[0].text.split('€')
            if len(amounts_list) > 2:
                price_ = amounts_list[2]
            if len(amounts_list) <= 2:
                price_ = amounts_list[1] 
        price_= price_.replace(",",".")
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("AWOL")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_AlterVape(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)

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
        element_soup = soup.find_all("span",{"class":"woocommerce-Price-amount amount"})
        price_ = element_soup[2].text.replace("\n","").replace("\xa0€","").replace(",",'.')
        print(price_)

        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Alter Vape")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_bwell_pharmacy(u):
    
    url = "https://bwell.com.cy/shop/" + Item_url_
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("404. The page you are looking for does not exist" in response.text)or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("span",{"class":"woocommerce-Price-amount amount"})
        element_soup_1 = element_soup[1].text
        price_ = element_soup_1.replace("€","")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Bwell Pharmacy")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_cablenet(u):

    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    
    else:
        # Internet access provision services	
        if name_ == "Purple Internet HBO Max Edition": 
            element_soup = soup.find_all("div",{"class":"elementor-heading-title elementor-size-default"}) 
            euro_ = element_soup[1].text.count("€")
            price_ = float(element_soup[1].text.replace(" ",'').split("€")[euro_].split("/")[0])
            print(price_)
        # Bundled telecommunication services
        if name_ == "Purple Max Mobile":
            element_soup = soup.find_all("div",{"class":"elementor-heading-title elementor-size-default"})
            price_ = float(element_soup[1].text.replace("μετά €","").replace("/μήνα ",""))
            print(price_)
        else: 
        # Wired and Wireless telephone services	
            element_name = soup.find_all("td")
            for i in element_name:
                if i.text == name_:
                    value_ = element_name[28].text
                    price_ = value_.replace("€","").replace(" ","").replace("/","").replace("30","").replace("''","")
                    print(price_)
                if i.text == name_:
                    value_ = element_name[33].text
                    price_ = value_.replace("€","").replace(" ","").replace("/","").replace("30","").replace("''","")
                    print(price_)
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Cablenet")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_CyMinistryEducation(u):
    '''
    ## PREVIOUS VERSION (2024-25)
    url = "http://archeia.moec.gov.cy/mc/698/" + Item_url_
    
    if "ΝΗΠΙΑΓΩΓΕΙΩΝ" in name_:
        #THE GRAMMAR JUNIOR SCHOOL (Nicosia)
        pdf_ = tb.read_pdf(url, pages = '4', pandas_options = {'header': None}, stream = True)
        pdf_ = pdf_[0]
        
        #Annual cost
        pdf_[3] = pdf_[3].astype('string')
        pdf = pdf_[3][1]
        price_1 = float(pdf.strip('€*').replace(".", ""))

        #Other costs
        pdf_[5] = pdf_[5].astype('string')
        pdf = pdf_[5][0]
        price_2 = float(pdf.replace("τέλος εγγραφής ","").strip('€*').replace(".", ""))

        pdf_[5] = pdf_[5].astype('string')
        pdf = pdf_[5][2]
        price_3 = float(pdf.replace("βιβλία και στολές ","").strip('€*').replace(".", ""))
        
        #Total cost
        price_ = price_1 + price_2 + price_3
    
    if "ΔΗΜΟΤΙΚΩΝ" in name_:
        #THE GRAMMAR JUNIOR SCHOOL (Nicosia)
        pdf_ = tb.read_pdf(url, pages = '1', pandas_options = {'header': None}, stream = True)
        pdf_ = pdf_[0]

        #Annual cost
        for i in range(0,7):
            pdf_[i] = pdf_[i].astype('string')

        price_1 = float(pdf_[1][25].strip('€*').replace(".", "")) + float(pdf_[2][25].strip('€*').replace(".", "")) + float(pdf_[3][25].strip('€*').replace(".", "").split(" €")[0]) + float(pdf_[3][25].strip('€*').replace(".", "").split(" €")[1]) + float(pdf_[4][25].strip('€*').replace(".", "")) + float(pdf_[5][25].strip('€*').replace(".", ""))
        price_1 = price_1 / 6

        #Other costs
        pdf = pdf_[6][24]
        price_2 = float(pdf.replace("τέλος εγγραφής ","").strip('€*').replace(".", ""))

        pdf = pdf_[6][26]
        price_3 = float(pdf.replace("βιβλία και στολές ","").strip('€*').replace(".", ""))
        
        #Total cost
        price_ = price_1 + price_2 + price_3
                     
    if ("Nicosia" in name_) and ("ΜΕΣΗΣ" in name_):
        pdf_ = tb.read_pdf(url, pages = '1', pandas_options = {'header': None}, stream = True)
        pdf_ = pdf_[0]

        for i in range(2,7):
            pdf_[i] = pdf_[i].astype('string')
            if subclass_ == "Secondary education":
                #THE GRAMMAR SCHOOL (NICOSIA): Α΄ τάξη - ΣΤ΄ τάξη
                value_1 = (float(pdf_[2][4].replace("€",'').replace(".","")))
                value_2 = (float(pdf_[3][4].replace("€",'').replace(".","")))
                value_3 = (float(pdf_[4][4].replace("€",'').replace(".","")))
                value_4 = (float(pdf_[5][4].replace("€",'').replace(".","")))
                value_5 = (float(pdf_[6][4].replace("€",'').replace(".","")))
                value_6 = (float(pdf_[7][4].replace("€",'').replace(".","")))
                price_ = float(value_1 + value_2 + value_3 + value_4 + value_5 + value_6) / 6

            if subclass_ == "Post-secondary non-tertiary education (ISCED 4)":
                #THE GRAMMAR SCHOOL (NICOSIA): Ζ΄ τάξη
                pdf_[8] = pdf_[8].astype('string')
                value_7 = (float(pdf_[8][4].replace("€",'').replace(".",""))) 
                price_ = float(value_7)
    
    if ("Limassol" in name_) and ("ΜΕΣΗΣ" in name_):
        pdf_ = tb.read_pdf(url, pages = '2', pandas_options = {'header': None}, stream = True)
        pdf_ = pdf_[0]
        
        for i in range(2,7):
            pdf_[i] = pdf_[i].astype('string')
            if subclass_ == "Secondary education":
                #THE GRAMMAR SCHOOL (LIMASSOL): Α΄ τάξη - ΣΤ΄ τάξη
                value_1 = (float(pdf_[2][15].replace("€",'').replace(".","")))
                value_2 = (float(pdf_[3][15].replace("€",'').replace(".","")))
                value_3 = (float(pdf_[4][15].replace("€",'').replace(".","")))
                value_4 = (float(pdf_[5][15].replace("€",'').replace(".","")))
                value_5 = (float(pdf_[6][15].replace("€",'').replace(".","")))
                value_6 = (float(pdf_[7][15].replace("€",'').replace(".","")))
                price_ = float(value_1 + value_2 + value_3 + value_4 + value_5 + value_6) / 6

            if subclass_ == "Post-secondary non-tertiary education (ISCED 4)":
                #THE GRAMMAR SCHOOL (LIMASSOL): Ζ΄ τάξη
                pdf_[8] = pdf_[8].astype('string')
                value_7 = (float(pdf_[8][15].replace("€",'').replace(".",""))) 
                price_ = float(value_7)
    '''
    ## 2025-26: NEW VERSION from 17/06/2025
    
    #url = "https://sch.cy/mc/698/" + Item_url_

    #THE GRAMMAR JUNIOR SCHOOL (Nicosia)
    if "ΝΗΠΙΑΓΩΓΕΙΩΝ" in name_:
        
        # Read the pdf file using pdfplumber
        with pdfplumber.open("PDFs/didaktra_idiotikon_nipiagogeion_2025_26.pdf") as pdf:
            page = pdf.pages[3]
            table = page.extract_table()
        
        price_1_1 = float(table[2][2].replace("€","").split("\n")[0])
        price_1_2 = float(table[2][2].replace("€","").split("\n")[1])
        price_1 = (price_1_1 + price_1_2) / 2
        price_2 = float(table[2][4].split("εγγραφή")[0].replace("€",""))
        price_ = price_1 + price_2
        print(price_)

    if "ΔΗΜΟΤΙΚΩΝ" in name_:        
            
        with pdfplumber.open("PDFs/didaktra_idiotikon_dimotikon_scholeion_2025_26.pdf") as pdf:
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
                
        with pdfplumber.open("PDFs/didaktra_idiotikon_mesi_ekpaidefsi_2025_26.pdf") as pdf:
            page = pdf.pages[0] 
            table = page.extract_table()
            
            #Α΄ τάξη - ΣΤ΄ τάξη
            if subclass_ == "Secondary education":
                price_1 = float(table[4][2].replace("€","").replace(".","")) + float(table[4][3].replace("€","").replace(".","")) + float(table[4][4].replace("€","").replace(".","")) + float(table[4][5].replace("€","").replace(".","")) + float(table[4][6].replace("€","").replace(".","")) + float(table[4][7].replace("€","").replace(".",""))
                price_ = price_1 / 6
                print(price_)
            
            #Ζ' τάξη
            if subclass_ == "Post-secondary non-tertiary education (ISCED 4)":
                price_ = float(table[4][8].replace("€",'').replace(".",""))
                print(price_)
    
    #THE GRAMMAR SCHOOL (LIMASSOL)
    if ("Limassol" in name_) and ("ΜΕΣΗΣ" in name_):
    
        with pdfplumber.open("PDFs/didaktra_idiotikon_mesi_ekpaidefsi_2025_26.pdf") as pdf:
            page = pdf.pages[1] 
            table = page.extract_table()

            #Α΄ τάξη - ΣΤ΄ τάξη
            if subclass_ == "Secondary education":
                price_1 = float(table[8][2].replace("€","").replace(".","")) + float(table[8][3].replace("€","").replace(".","")) + float(table[8][4].replace("€","").replace(".","")) + float(table[8][5].replace("€","").replace(".","")) + float(table[8][6].replace("€","").replace(".","")) + float(table[8][7].replace("€","").replace(".",""))
                price_ = price_1 / 6
                print(price_)
            
            #Z΄ τάξη
            if subclass_ == "Post-secondary non-tertiary education (ISCED 4)":
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
          
    pdf_ = tb.read_pdf(Item_url_, pages = p,pandas_options={'header': None}, stream=True)[0]
    pdf_[d]=pdf_[d].astype('string')
    price_=pdf_[d][qp].split(' ')[0].replace(',','.')
    
    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(float(price_))
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("Cyprus Post")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_ewholesale(u):
    
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    
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
        element_soup = soup.find_all("div",{"class":"hM4gpp"}) 
        price_= element_soup[0].text.replace(",",".").replace(" ","").replace("€","").replace("Τιμή","")
        print(price_)
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("E-wholesale")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_electroline(u):
    
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("ins",{"class":"product-price product-price--single product-price--sale-price product-price--single--sale-price"}) 
        
        if element_soup:
            price_ = element_soup[0].text.replace("\n",'').replace("€","")
        else:
            element_soup = soup.find_all("h2",{"class":"product-price product-price--single"}) 
            price_ = element_soup[0].text.replace("\n","").replace("€","")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Electroline")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_EUC(u):
    """
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
    """
    pdf_path = r"PDFs/EUC-tuition-fees-2025-26.pdf"
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
    price_ = price_1/count_
    print(price_)
    
    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(float(price_))
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("European University Cyprus")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)

def results_famousports(u):
    
    url = "https://www.famousports.com/en" + Item_url_
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if (response.status_code !=200) or ("Oops! Page Not Found!" in soup.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all("h2",{"class":"product-price product-price--single"}) 
        element_soup = soup.find_all("strong",{"class":"text-xl lg:text-2xl font-bold tracking-tight"})
        price_ = element_soup[0].text.replace("\n","").replace(" ","").replace("€","").replace(",",".")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Famous Sports")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_Marks_Spencer(u):
    
    url="https://www.marksandspencer.com/cy"+Item_url_
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
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
        price_=element_soup[0].text.replace("\n","").replace(" ","").replace("€","").replace(",",".")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Marks & Spencer")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_moto_race(u):
    
    url = "https://www.motorace.com.cy/" + Item_url_
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(url, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("404 Not Found" in soup.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)  
    else:
        element_soup = soup.find_all("span",{"class":"price"})
        price_=element_soup[0].text.replace(",","").replace("€","")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Moto Race")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_nissan(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(Item_url_, headers=header)
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

def results_novella(u):
    
    new_row=[]
    website_false=[]
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
 
    if ("404 Page Not Found." in soup.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        scripts_1 = soup.find_all('td',{'class':'column-1'},string=True)
        scripts_2 = soup.find_all('td',{'class':'column-2'},string=True)
 
        for i in range(0,len(scripts_1)):
            new_row=[]
            website_false=[]
            
            if (scripts_1[i].text=="LADIES CUT") and (name_=="Women's Services, HAIRCUT Stylist"):
                price_=scripts_2[i].text.replace('€',"").replace(',','.')
                
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Novella")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)
 
            elif (name_=="Men's Services, HAIRCUT Stylist") and (scripts_1[i].text== "MEN'S CUT"):
                price_=scripts_2[i].text.replace('€',"").replace(',','.')
                
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Novella")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_numbeo(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")

    if ("Status code: 404" in soup.text) or (response.status_code !=200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_soup = soup.find_all('tr', {"class":"tr_standard"})
        for o in range(0, len(element_soup)):
            ken = element_soup[o].text.replace("\n","").replace(" ","")
            if "Cyprus" in ken:
                result = re.sub(r'^.*?(Cyprus)', r'\1', ken).replace("Cyprus","").replace("$","").replace(" ","")
                price_ = round((float(result)/1.08),2)
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Numbeo")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_primetel(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
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
        if (name_=="GIGA Unlimited") | (name_=="GIGA Unlimited 5G") | (name_=="GIGA Unlimited 5G MAX") :
            
            element_ = soup.find_all('p', {"class":"price"})
            
            if name_ == "GIGA Unlimited" :
                text = element_[0].text.replace("\n","").replace(" ","").replace("from€","")
                pattern = r"(\d+\.\d+)"
                match = re.search(pattern, text)
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
             
            if name_ == "GIGA Unlimited 5G" :
                text = element_[1].text.replace("\n","").replace(" ","").replace("from€","")
                pattern = r"(\d+\.\d+)"
                match = re.search(pattern, text)
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
                text = element_[2].text.replace("\n","").replace(" ","").replace("from€","")
                pattern = r"(\d+\.\d+)"
                match = re.search(pattern, text)
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

        # Wired & Wireless telephone services           
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
        
        # Internet access provision services 
        elif (name_=="Fiber Family & 200Mbps") | (name_=="Fiber Entertainment & 200Mbps") :

            element_ = soup.find_all("div", {"class":"price_tv_pack"})
                
            if name_ == "Fiber Family & 200Mbps" :
                    text_3 = element_[3].text
                    match = re.search(r'€(\d+\.\d+) / month\n€(\d+\.\d+)/month after 12 months', text_3)
                    if match:
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
            
            if name_ == "Fiber Entertainment & 200Mbps" :
                    text_4 = element_[4].text
                    match = re.search(r'€(\d+\.\d+) / month\n€(\d+\.\d+)/month after 12 months', text_4)
                    if match:
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
                
def results_rio(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if ("404 Not Found!" in soup.text)or(response.status_code != 200):
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
                        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)     
                else:
                    amount_match = re.search(r'€(\d+)', element_name[i].text)

                    if amount_match:
                        price_ = amount_match.group(1)
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
                        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)
                        
def results_AHK(u):
    '''
    response = requests.get(Item_url_)
    pdf_AHK = "PDFs/AHK_Mar2024.pdf"
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)  
    else:
        with open(pdf_AHK, "wb") as f:
            f.write(response.content)
        with open(pdf_AHK, "rb") as f:
            #pdf_reader = PyPDF2.PdfReader(f)
            pdf_reader = pypdf.PdfReader(f)
            page = pdf_reader.pages[2]
            text = page.extract_text()
    '''
    pdf_AHK = "PDFs/AHK_Jul2025.pdf"
    
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
                if "για" in ken:
                    price_ = float(match.group(0).replace(",","."))/100
                else:
                    price_ = float(match.group(0).replace(",","."))   
                
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(price_)
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("AHK")
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

def results_CERA(u):
    
    response = requests.get(Item_url_)
    CERA = tb.read_pdf(Item_url_, pages='8', pandas_options={'header': None}, stream=True)
    amount_ = CERA[0][1].to_list()
    names_ = CERA[0][0].to_list()
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:   
        for i in range(0, len(names_) - 1):
            n1 = names_[i] + " " + names_[i + 1]
            if name_ == n1:
                price_ = float(amount_[i]) / 100
                
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(price_)
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Cyprus Energy Regulatory Authority")
                list_.loc[len(list_)] = new_row
                list_['Name'] = list_['Name'].apply(lambda x:x)

def results_water(u):
    
    if "Nicosia" in retailer_:
        city_ = "Nicosia"
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
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
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_ + " - " + city_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Water Board of " + city_)
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

def results_wolt(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs, {'headers':header})
    
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
        element_name = soup.find_all('span',{"data-test-id":"product-modal.price"})
        
        if element_name:
            price_ = element_name[0].text.replace("€","").replace(",",".").replace("/xa0","")
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

def results_vasos(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs, {'headers':header}, verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
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
        new_row.append("Vasos Psarolimano")
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
    """
    header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs,{'headers':header},verify=False)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code !=200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] =daily_errors["Name"].apply(lambda x:x)    
    else:
        element_name = soup.find_all('div',{"class":"mprm-simple-view-column mprm-first"})
        for i in range(0,len(element_name)):
            if ("Meat Meze" in element_name[i].text) and ("Meat Meze" in name_):
                element_name_2 = element_name[i].find_all('li',{"class":"mprm-flex-item mprm-price"})
                price_=element_name_2[0].text.replace("€","")

        for i in range(0,len(element_name)):
            
            if "Fish Meze" in element_name[i].text and ("Fish Meze" in name_):
                element_name_2 = element_name[i].find_all('li',{"class":"mprm-flex-item mprm-price"})
                price_=element_name_2[0].text.replace("€","")

        if price_:
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Meze Tavern")
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
    """
    file_path = "PDFs/Meze_Taverna_Jan2025.docx" #the prices of meat and fish meze are displayed in page 4
    doc = Document(file_path)
    for para in doc.paragraphs:
        text_ = para.text

        if name_ == "Meat Meze for 2 persons - Limassol":
            match = re.search(r'KPEATOMEZEΔE>\s*(€\s*\d+(?:[.,]\d{2})?)', text_)
            if match:
                value = match.group(1)
                price_ = value.replace("€","").replace(" ","")
                print(price_)

        if name_ == "Fish Meze for 2 persons - Limassol":
            match = re.search(r'TAPOMEZEΔE>\s*(€\s*\d+(?:[.,]\d{2})?)', text_)
            if match:
                value = match.group(1)
                price_ = value.replace("€","").replace(" ","")
                print(price_)
    
    new_row.append(datetime.now().strftime('%Y-%m-%d'))
    new_row.append(name_)
    new_row.append(price_)
    new_row.append(subclass_)
    new_row.append(division_)
    new_row.append("Meze Tavern")
    list_.loc[len(list_)] = new_row
    list_['Name'] = list_['Name'].apply(lambda x:x)
    
def results_CYgar_shop(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_name = soup.find_all('div',{"class":"hM4gpp"})
        price_ = element_name[0].text.replace('€','').replace('Price','')
        
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
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        element_name = soup.find_all('div',{"class":"itemDetailsPrice"})
        if element_name:
            price_amount = element_name[0].text.replace("€","")
            
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

def results_pydixa(u):
    
    pdf_pixida = "PDFs/Pixida-Nic-En-2024-Sept-2.pdf"
    '''
    response = requests.get(Item_url_)
    if response.status_code!=200:
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
    if matches:
        new_row.append(datetime.now().strftime('%Y-%m-%d'))        
        new_row.append(name_)
        new_row.append(float(matches[0]))
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

def results_sewerage(u):
    
    values = 0
    
    if "Nicosia" in retailer_:
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
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
            new_row.append("Sewerage Board of " + city_)
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
                new_row.append("Sewerage Board of " + city_)
                list_.loc[len(list_)] = new_row
                      
    if "Limassol" in retailer_:
        city_ = "Limassol"
        new_row = []
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
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
                element_name = soup.find_all('table',{"class":"table table-striped"})
                element_name_2 = element_name[0].find_all('tr')
                element_name_2 = element_name_2[len(element_name_2) - 1]
                desired_lines = [element_name_2.find_all('td')[4].get_text(), element_name_2.find_all('td')[6].get_text()]

                for lines in desired_lines:
                    value = float(lines.replace(",","."))
                    values = value + values
                values = values / 2
                print(values)
                
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_ + " - " + city_)
                new_row.append(float(values))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Sewerage Board of " + city_)
                list_.loc[len(list_)] = new_row
            
        if "Τέλος Χρήσης" in name_:
            element_name = soup.find_all('table',{"class":"table table-striped"})
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
            new_row.append("Sewerage Board of " + city_)
            list_.loc[len(list_)] = new_row
                
    if "Larnaca" in retailer_:
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
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
            new_row.append("Sewerage Board of " + city_)
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
                new_row.append("Sewerage Board of " + city_)
                list_.loc[len(list_)] = new_row
                
            else:
                website_false.append(name_)
                website_false.append(subclass_)
                website_false.append(Item_url_)
                website_false.append(division_)
                website_false.append(retailer_)
                daily_errors.loc[len(daily_errors)] = website_false
                daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
'''
def results_toyota(u):
    
    if name_ == "The New Toyota Yaris Cross":
        
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs,{'headers':header})
        
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
            element_soup = soup.find_all("a", {"class":"cmp-mega-menu__card","data-model-name":"Yaris Cross"})
            #element_soup2 = element_soup[0].find_all("span",{"class":"cmp-mega-menu__price"})
            price_ = element_soup[0]['data-price']
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Toyota")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
            
    if name_ == "The New Toyota Yaris":
        
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs,{'headers':header})
        
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
            element_soup = soup.find_all("a", {"class":"cmp-mega-menu__card","data-model-name":"Yaris"})
            #element_soup2 = element_soup[0].find_all("span",{"class":"cmp-mega-menu__price"})
            price_ = element_soup[0]['data-price']
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Toyota")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        
    if name_ == "Toyota Aygo X":
            
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs,{'headers':header})
        
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
            #element_soup = soup.find_all('p',{"class":"t-milli-headline mb-0 text-normal cmp-mega-menu__price-wrapper d-flex"})
            #element_soup2 = element_soup[0].find_all("span",{"class":"cmp-mega-menu__price"})
            #price_ = float(element_soup2[0]['data-price'])
            element_soup = soup.find_all("a", {"class":"cmp-mega-menu__card","data-model-name":"Aygo x"})
            price_ = element_soup[0]['data-price']
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(price_)
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Toyota")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
                  
    #if subclass_=="Second-hand motor cars":
        
        #1st way
        """ 
        query = {"component":"used-stock-cars-v2","fetches":[
        {"fetchType":"fetchUscVehiclePrice","vehicleForSaleId":"4077c595-5c2c-42bd-8133-203d770ad125","context":"used","uscEnv":"production"}
        ]}
        headers = {"Host": "usc-webcomponents.toyota-europe.com","User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:126.0) Gecko/20100101 Firefox/126.0","Accept": "*/*","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate, br, zstd","Content-Type": "application/json","Content-Length": "180","Origin": "https://www.toyota.com.cy","Connection": "keep-alive","Referer": "https://www.toyota.com.cy/","Sec-Fetch-Dest": "empty","Sec-Fetch-Mode": "cors","Sec-Fetch-Site": "cross-site","Priority": "u=6","TE": "trailers"
        }
        response = requests.get(Item_url_,{'headers':headers})
        r = requests.post("https://usc-webcomponents.toyota-europe.com/v1/api/data/cy/en?brand=toyota&uscEnv=production", json=query, headers=headers)
        price_ = r.json()['fetches'][0]['result']['fetchResult'] ['sellingPriceInclVAT']
        """
        
        #2nd way
        """
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs)
        soup = BeautifulSoup(response.content, "html.parser")
        isnone = soup.find("div", {"role": "cpdqm_ignore"}).text

        if isnone == None:
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        else:
            data = json.loads(isnone)
            price_ = data['vehicle']['result']['price']['sellingPriceInclVAT']
            if price_:
                new_row.append(datetime.now().strftime('%Y-%m-%d'))
                new_row.append(name_)
                new_row.append(float(price_))
                new_row.append(subclass_)
                new_row.append(division_)
                new_row.append("Toyota")
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
                """
'''

def results_toyota(u):
    
    if (name_ == "The New Toyota Yaris Cross") | (name_ == "The New Toyota Yaris") | (name_ == "Toyota Aygo X"):    
        
        header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
        bs = BeautifulSoup(Item_url_, "html.parser")
        response = requests.get(bs,{'headers':header})
        
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

def results_ithaki(u):
    
    pdf_ithaki = "PDFs/ithaki-2024.pdf"

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
        pdf_flames1 = "PDFs/flames-grill-specialities-Mar2024.pdf"
    
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
        pdf_flames2 = "PDFs/flames-cyprus-dishes-Mar2024.pdf"
    
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

def results_lensescy(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs,{'headers':header})
    
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
        element_name = soup.find_all('div',{"class":"product-price"})
        price_ = element_name[0].text.replace("€","").replace(" ","").replace(",",".")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append("Corrective eye-glasses and contact lenses")
        new_row.append("HEALTH")
        new_row.append("LensesCY")
        list_.loc[len(list_)] = new_row

def results_intercity_buses(u):
    
    url_new = "https://intercity-buses.com/en/routes/" + Item_url_

    ## without headers
    #response = requests.get(url_new)
    
    ## with headers
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    
    # way 1
    response = requests.get(url_new, {'headers':header})
    # way 2
    #bs = BeautifulSoup(url_new, "html.parser")
    #response = requests.get(bs, {'headers':header})
        
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
            
def results_parga(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, {'headers':header})
    
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

def results_evdokia_jewellery(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, headers = header)
    
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
        price_soup = soup.find('p', class_='price')
        price_element = price_soup.find('span', {'class':'woocommerce-Price-amount amount'})
        price_ = price_element.text.replace("€","")
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Evdokia Jewellery")
        list_.loc[len(list_)] = new_row

def results_centroptical(u):
    
    response = requests.get(Item_url_, headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0"})
    soup = BeautifulSoup(response.content, "html.parser")
    
    if response.status_code != 200:
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        price_element = soup.find('p', class_ = 'price')
        bdi_element = price_element.find('bdi')
        price_ = bdi_element.text.replace("€","").replace(",",".")
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Centroptical")
        list_.loc[len(list_)] = new_row

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

def results_cyprus_transport(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, headers = header)
    
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

def results_musicavenue(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, {'headers':header})
    
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
        
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Musicavenue")
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_max_7_tax(u):
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(Item_url_, {'headers':header})
    
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
            new_row.append(float(charges_[i]))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Max 7 Taxi") 
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_costastheodorou(u):
    
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
        soup = BeautifulSoup(response.content, "html.parser")
        element_name = soup.find_all("p", {"class":"price"})
        price_ = element_name[0].text.replace("€","").split('\xa0')[0]
        
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
        
        new_row.append(datetime.today().strftime("%Y-%m-%d"))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Leroy Merlin") 
        list_.loc[len(list_)] = new_row
        list_['Name'] = list_['Name'].apply(lambda x:x)

def results_stock_center(u):
    
    bs = BeautifulSoup(Item_url_, "html.parser")
    response = requests.get(bs)

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

def results_cheapbasket(u):
    
    url = "https://cheapbasket.com.cy/product/" + Item_url_
    response = requests.get(url)
    
    if (response.status_code != 200):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.text, 'html.parser')

        if ("New Products" in soup.get_text()):
            website_false.append(name_)
            website_false.append(subclass_)
            website_false.append(Item_url_)
            website_false.append(division_)
            website_false.append(retailer_)
            daily_errors.loc[len(daily_errors)] = website_false
            daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
        else:
            element_ = soup.find_all("div",{"class":"shop-detail-right klb-product-right"})
            element_price = element_[0].find_all("span",{"class":"woocommerce-Price-amount amount"})
            price_ = element_price[0].text.replace("€","").replace(" ","").replace(",",".")
            
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Cheap Basket")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_opacy(u):
    
    url_ = "https://opa.cy/product/" + Item_url_
    response = requests.get(url_)
    
    if (response.status_code != 200) or ("Oops! It seems we are missing something." in response.text):
        website_false.append(name_)
        website_false.append(subclass_)
        website_false.append(Item_url_)
        website_false.append(division_)
        website_false.append(retailer_)
        daily_errors.loc[len(daily_errors)] = website_false
        daily_errors["Name"] = daily_errors["Name"].apply(lambda x:x)
    else:
        soup = BeautifulSoup(response.text, 'html.parser')
        element_ = soup.find_all("span",{"class":"product-span price"})
        price_ = element_[0].text.replace("Price: €","")
        
        if (name_=="Tomatoes Ripe for Salsa")|(name_=="Cucumbers fleid")|(name_=="Red Onions")|(name_=="Cucumbers Greenhouse")|(name_=="Cherry Tomatos"):
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_)*2) #since the price of the above 5 products is per 500g, we multiply *2 to have Eur/Kg 
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Opa")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)
        else:
            new_row.append(datetime.now().strftime('%Y-%m-%d'))
            new_row.append(name_)
            new_row.append(float(price_))
            new_row.append(subclass_)
            new_row.append(division_)
            new_row.append("Opa")
            list_.loc[len(list_)] = new_row
            list_['Name'] = list_['Name'].apply(lambda x:x)

def results_piatsa_gourounaki(u):
    
    pdf_path = "PDFs/Piatsa_JUN2025.pdf"
    output_path = "PDFs/piatsa_gourounaki_output.txt"
    
    with pdfplumber.open(pdf_path) as pdf, open(output_path, 'w', encoding='utf-8') as outfile:
        
        results = []
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            
            if text:
                lines = text.split('\n')
                keep_next = False
                
                for line in lines:
                    
                    if keep_next:
                        #outfile.write(line.strip() + '\n')
                        keep_next = False
                        results.append(line.strip())
                        break  # Αν θες μόνο την πρώτη επόμενη γραμμή μετά τη 1122
                    
                    if line.strip().startswith("1122"):
                        #outfile.write(line.strip() + "\n")
                        results.append(line.strip())
                        keep_next = True
    
    pattern = r'\d+(?:,\d{2})?'
    price_ = []
    for line in results:
        found = re.findall(pattern, line)
        price_ = float(found[0].replace(",","."))
        print(price_)
        
    if price_:
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(float(price_))
        new_row.append(subclass_)
        new_row.append(division_)
        new_row.append("Piatsa Gourounaki")
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
    '''
    if os.path.exists(output_path):  # os should be defined !!!
        os.remove(output_path)
    else:
        print("File not found.")
    '''
    
def results_pagkratios(u):

    bs = BeautifulSoup(Item_url_, "html.parser")
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    response = requests.get(bs,{'headers':header})
    
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.content, "html.parser")
        elemenet_2 = soup.find_all("span",{"class":"woocommerce-Price-amount amount"})
        price_ = elemenet_2[1].text.replace("€","")
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
    
    pdf_path = "PDFs/Christos_JUN2025.pdf"

    with pdfplumber.open(pdf_path) as pdf:
        if len(pdf.pages) >= 9:
            page9 = pdf.pages[8]  
            text = page9.extract_text()
            match = re.search(r"Seafood Platter MEZE for 2 persons\s+(\d+(?:\.\d+)?)", text)
            
            if match:
                price = match.group(1)
                price_ = float(price)/2
                print(price_)

            if price_:
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
    
    #if retailer_=="SupermarketCy":
    #    results_supermarketcy(u) 
    #elif retailer_=="METRO":
    #    results_metro(u)
    #elif retailer_=="Alphamega":
    #    results_alphamega(u)    
    #elif retailer_=="Cheap Basket":
    #    results_cheapbasket(u)
    #elif retailer_=="Opa":
    #    results_opacy(u)    
    if retailer_=="Fuel Daddy":
        results_fueldaddy(u)
    elif retailer_=="Costas Theodorou":
        results_costastheodorou(u)
    elif retailer_=="Parga":
        results_parga(u)    
    elif retailer_=="Leroy Merlin":
        results_leroymerlin(u)   
    elif retailer_=="IKEA":
        results_ikea(u)
    #elif retailer_=="Stephanis":
    #    results_stephanis(u)
    #elif retailer_=="Public":
    #    results_public(u)
    elif retailer_=="Electroline":
        results_electroline(u)
    elif retailer_=="CYTA":
        results_cyta(u)
    elif retailer_=="Cablenet":
        results_cablenet(u)  
    elif retailer_=="Primetel":
        results_primetel(u)    
    elif retailer_=="Epic":
        results_epic(u)
    elif retailer_=="Athlokinisi":
        results_Athlokinisi(u)
    elif retailer_=="Famous Sports":
        results_famousports(u) 
    elif retailer_=="Marks&Spencer":
        results_Marks_Spencer(u)    
    elif retailer_=="Bwell Pharmacy":
        results_bwell_pharmacy(u)
    elif retailer_=="Novella":
        results_novella(u) 
    elif retailer_=="Evdokia Jewellery":
        results_evdokia_jewellery(u)
    elif retailer_=="LensesCY":
        results_lensescy(u)    
    elif retailer_=="Centroptical":
        results_centroptical(u)
    elif retailer_=="Premier Laundry":
        results_premier(u)
    elif retailer_=="Music Avenue":
        results_musicavenue(u)    
    elif retailer_=="Rio Cinema":
        results_rio(u)    
    elif retailer_=="Cyprus Ministry of Education, Sport and Youth":
        results_CyMinistryEducation(u)
    elif retailer_=="European University Cyprus":
        results_EUC(u)    
    elif retailer_=="Cyprus Post":
        results_CyPost(u)
    elif retailer_=="AHK":
        results_AHK(u)
    elif retailer_=="Cyprus Energy Regulatory Authority":
        results_CERA(u)
    elif (retailer_=="Water Board of Larnaca") or (retailer_=="Water Board of Limassol") or (retailer_=="Water Board of Nicosia"):
        results_water(u)
    elif (retailer_=="Sewerage Board of Nicosia") or (retailer_=="Sewerage Board of Larnaca") or (retailer_=="Sewerage Board of Limassol"):
        results_sewerage(u)    
    elif retailer_=="MotoRace":
        results_moto_race(u)
    elif retailer_=="AWOL":
        results_awol(u)    
    elif retailer_=="Toyota":
        results_toyota(u)    
    elif retailer_=="Nissan":
        results_nissan(u)
    elif retailer_=="Stock Center":
        results_stock_center(u)    
    elif retailer_=="Alter Vape":
        results_AlterVape(u)    
    elif retailer_=="The CYgar shop":
        results_CYgar_shop(u)
    elif retailer_=="The Royal Cigars":
        results_royal_cigars(u)  
    elif retailer_=="E-wholesale":
        results_ewholesale(u)    
    elif retailer_=="NUMBEO":
        results_numbeo(u)
    elif retailer_=="Wolt":
        results_wolt(u)
    elif retailer_=="Vasos Psarolimano":
        results_vasos(u)
    elif retailer_=="Meze Tavern":
        results_meze(u)    
    elif retailer_=="Pyxida":
        results_pydixa(u)
    elif retailer_=="Ithaki":
        results_ithaki(u)
    elif retailer_=="Flames":
        results_flames(u)
    elif retailer_=="Piatsa Gourounaki":
        results_piatsa_gourounaki(u)
    elif retailer_=="Pagkratios":
        results_pagkratios(u)
    elif retailer_=="Christos Grill&Seafood":
        results_christos_grill_seafood(u)    
    #elif retailer_=="Intercity Buses":
    #    results_intercity_buses(u)  
    elif retailer_=="Cyprus Transport":
        results_cyprus_transport(u)
    elif retailer_=="Max 7 Taxi":
        results_max_7_tax(u)
   
# Change the type as float
list_["Price"].astype(float)

# Total computational/processing time
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time/60, "minute")

# Export/Save the scraped data 
df.to_csv("Datasets/Raw-Data-2025Q3.csv", index=False) 
#df.to_csv("Datasets/Raw-Data.csv", index=False) 

combined_df = pd.concat([df, list_], axis=0)
combined_df.reset_index(drop=True, inplace=True)
combined_df.to_csv("Datasets/Raw-Data-2025Q3.csv", index=False, header=True)
#combined_df.to_csv("Datasets/Raw-Data.csv", index=False, header=True)
daily_errors.to_csv("Datasets/Daily-Scraping-Errors.csv",index=False)
