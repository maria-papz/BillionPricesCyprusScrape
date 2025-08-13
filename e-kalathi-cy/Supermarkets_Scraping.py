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

from ast import Try
from lxml import html, etree
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.error import URLError
from tabula import read_pdf

# Ignore specific warning
warnings.simplefilter("ignore")

# Read necessary data
df = pd.read_csv("e-kalathi/Supermarkets_ScrapedData.csv")
urls = pd.read_csv("e-kalathi/Supermarkets_ProductsList.csv")

# Create a null dataframe
daily_errors = pd.DataFrame(columns = ["Name","Subclass","Url","Division","Retailer"])
list_ = pd.DataFrame(columns = ["Date","Name","Price","Subclass","Division","Retailer"])

# Define the functions for the web-scraping of the target retailers

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
'''        
def results_supermarketcy(u):

    url_new = "https://www.supermarketcy.com.cy/" + Item_url_
    
    ## with headers
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    #bs = BeautifulSoup(url_new, "html.parser")
    #response = requests.get(bs, {'headers': header})

    # without headers
    response = requests.get(url_new)
           
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
        #soup = BeautifulSoup(response.text, "html.parser")
        name_wrappers = soup.find('h1', {'class':"text-h6 md:text-h4 text-gray-dark font-bold mb-8 lg:mb-40 lg:max-w-520 leading-snug italic"}).text
        price_wrappers = soup.find('div', {'class':"text-primary text-24 lg:text-h3 font-bold italic my-4 lg:my-8"}).text
        value = price_wrappers.split('\xa0')[0].replace('.', '').replace(',', '.')
        print(value)
        
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_wrappers)
        new_row.append(float(value))
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("SupermarketCy")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)  
'''
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
            print(price_)
            
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

        # Extract only the number
        match = re.search(r'\d+', price_)
        if match:
            price_ = int(match.group())
        
        print(price_)
            
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

def results_metro(u):
    
    #website: "https://wolt.com/en/cyp/larnaca/venue/metro-larnaca/" 

    ## without headers
    response = requests.get(Item_url_)
    
    ## with headers
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers':header})

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

#Initialization of the scraping/processing time
start_time = time.time()

# Run the code
for u in range(0, len(urls)):
    print(u)
    
    # Creative a new row each time 
    new_row = []
    website_false = []
    
    # Read the data
    Item_url_ = urls["Url"].iloc[u]
    name_ = urls["Name"].iloc[u]
    print(name_)
    subclass_ = urls["Subclass"].iloc[u]
    division_ = urls["Division"].iloc[u]
    retailer_ = urls["Retailer"].iloc[u]
  
    if retailer_ == "Alphamega":
        results_alphamega(u)  
    #elif retailer_ == "SupermarketCy":
        #results_supermarketcy(u)      
    elif retailer_ == "Cheap Basket":
        results_cheapbasket(u)  
    elif retailer_ == "Opa":
        results_opacy(u)
    elif retailer_ == "METRO":
        results_metro(u)      
    
# Change the type as float
list_["Price"].astype(float)

# Total computational/processing time
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time/60, "minute")

# Export/Save the scraped data 
df.to_csv("e-kalathi/Supermarkets_ScrapedData.csv", index=False) 

combined_df = pd.concat([df, list_], axis = 0)
combined_df.reset_index(drop = True, inplace = True)
combined_df.to_csv("e-kalathi/Supermarkets_ScrapedData.csv", index=False, header=True)
daily_errors.to_csv("e-kalathi/Supermarkets_DailyScrapingErrors.csv", index=False)
