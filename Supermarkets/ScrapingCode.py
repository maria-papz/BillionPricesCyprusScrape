# Important libraries 
import pandas as pd 
import numpy as np
import tabula as tb
import matplotlib.pyplot as plt

import re
import requests
import time
import xlsxwriter
import pypdf
import pdfplumber
import urllib.request
import json
import warnings
import httpx

from ast import Try
from lxml import html, etree
from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import date, timedelta
from urllib.error import URLError
#from tabula import read_pdf
from docx import Document
from pypdf import PdfReader

# Ignore specific warning
warnings.simplefilter("ignore")

# Read necessary data
df = pd.read_csv("Supermarkets/ScrapedData.csv")
urls = pd.read_csv("Supermarkets/ProductsList.csv")

# Create a null dataframe
daily_errors = pd.DataFrame(columns = ["Name","Subclass","Url","Division","Retailer"])
list_ = pd.DataFrame(columns = ["Date","Name","Price","Subclass","Division","Retailer"])

# Define the functions for the web-scraping of the target retailers

def results_alphamega(u):
    
    ## with headers
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
    #response = requests.get(Item_url_, headers=header)
    
    ## without headers
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
        element_soup = soup.find("span", {"class":"text-price fs-5"}).text.strip()
        price_ = element_soup.replace('€','').replace(',','.').strip()
        print(price_)
        new_row.append(datetime.now().strftime('%Y-%m-%d'))
        new_row.append(name_)
        new_row.append(price_)
        new_row.append(subclass_)
        new_row.append(division_)  
        new_row.append("Alphamega")
        list_.loc[len(list_)] = new_row
        list_["Name"] = list_["Name"].apply(lambda x:x)  
      
def results_supermarketcy(u):

    ## with headers
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
    #header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    response = requests.get(Item_url_, headers = header)

    #bs = BeautifulSoup(Item_url_, "html.parser")
    #response = requests.get(bs, {'headers': header})

    ## without headers
    #response = requests.get(Item_url_)
    
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
    #    results_supermarketcy(u)    

# Change the type as float
list_["Price"].astype(float)

# Total computational/processing time
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time/60, "minute")

# Export/Save the scraped data 
df.to_csv("Supermarkets/ScrapedData.csv", index=False) 

combined_df = pd.concat([df, list_], axis = 0)
combined_df.reset_index(drop = True, inplace = True)
combined_df.to_csv("Supermarkets/ScrapedData.csv", index=False, header=True)
daily_errors.to_csv("Supermarkets/ScrapingErrors.csv", index=False)
