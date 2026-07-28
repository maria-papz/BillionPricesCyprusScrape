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

#############################################################################################################################
##### Kyriacos' testings

#################################################################################################################################
print("######################################################################################################################")
print("ECOICOP v2")
print("######################################################################################################################")
#################################################################################################################################

#================================================================================================================================
# SupermarketCy
#================================================================================================================================
print("SupermarketCy")
url = "https://www.supermarketcy.com.cy/sifounas-frantzolakia-stroggyla-4tem"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Stephanis
#================================================================================================================================
print("Stephanis")
url = "https://www.stephanis.com.cy/en/products/396845"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Cablenet
#================================================================================================================================
print("Cablenet")
url = "https://cablenet.com.cy/postpaid-charge-rates/"

### without headers 
## 1
#bs = BeautifulSoup(url, "html.parser")
#response_1 = requests.get(bs)
## 2
response_1 = requests.get(url)
print(response_1)

### with headers 
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
## 1 
#bs = BeautifulSoup(url, "html.parser")
#response_2 = requests.get(bs, {'headers':header})
## 2
response_2 = requests.get(url, headers = header) 
## 3 
#with httpx.Client(headers = header) as client:
#    response_2 = client.get(url)
print(response_2)

#================================================================================================================================
# Intercity Buses
#================================================================================================================================
print("Intercity Buses")
url = "https://intercity-buses.com/en/routes/nicosia-limassol-limassol-nicosia/"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Moto Race
#================================================================================================================================
print("Moto Race")
url = "https://www.motorace.com.cy/ktm-sx-e-1-20-factory-edition.html"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Famous Sports
#================================================================================================================================
print("Famous Sports")
url = "https://www.famousports.com/en/products/core-team-kit-sml-logo-t-sh-au-blue?option_variant_id=140"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# EOA Nicosia (https://ndlgo.org.cy/)
#================================================================================================================================
print("Water EOA Nicosia")
url = "https://ndlgo.org.cy/water-supply/water-fees-wbn/"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

print("Sewerage EOA Nicosia")
url = "https://ndlgo.org.cy/sewage/sewer-fees/"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Constantinou Jewels
#================================================================================================================================
print("Constantinou Jewels")
url = "https://constantinou-jewels.com/en/shop-2/jewellery/women/womens-cross-23/"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Brilliance Jewellery
#================================================================================================================================
print("Brilliance Jewellery")
url = "https://brilliancejewellery.com.cy/product/stainless-steel-vancleef-bracelet-10/"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Procopiou Medishop
#================================================================================================================================
print("Procopiou Medishop")
url = "https://www.procopioumedishop.com/product/graduated-ss-n3-surgical-handle"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Wolt
#================================================================================================================================
print("Wolt")
url = "https://wolt.com/en/cyp/nicosia/restaurant/kfc-aglantzia/twister-itemid-692eae75bc0a1e597836f510"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

'''
### *Wolt*

## What this does:
## 1. Pretends to be a Chrome browser by using a browser-like User-Agent header (so it doesn’t look like a bot).
## 2. If the site says 429 Too Many Requests, it waits 5 seconds, then retries (up to 5 times).
## 3. If it succeeds (status code 200), it returns the page HTML.

url = "https://wolt.com/en/cyp/nicosia/restaurant/kfc-aglantzia/twister-itemid-68f9dd086496eabe82f09052"

# Custom headers to mimic a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_url(url, headers, retries=10, delay=10):
    
    # Tries to fetch a URL with retries in case of 429 Too Many Requests 
    for attempt in range(1, retries + 1):
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print("Success on attempt", attempt)
            return response.text
        
        elif response.status_code == 429:
            print(f"429 Too Many Requests. Waiting {delay} seconds before retry {attempt}/{retries}...")
            time.sleep(delay)
        else:
            print(f"Failed with status {response.status_code}")
            return None
    
    print("Max retries reached. Could not fetch the page.")
    return None

# Run it
html_content = fetch_url(url, headers)

# Preview the first 500 characters if successful
if html_content:
    print(html_content[:500])
'''

"""
#####################################################################################################################################################
#### Kendeas' testings

## *Intercity Buses*

url_new = "https://intercity-buses.com/en/routes/" + "nicosia-limassol-limassol-nicosia/"

### with headers
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
#response = requests.get(url_new, {'headers':header})

### without headers
## 1 
bs = BeautifulSoup(url_new, "html.parser")
response = requests.get(bs)
## 2 
#response = requests.get(url_new)

if response.status_code != 200:
    print(response)
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
                    print(price_)
                else:
                    print(price_)  
"""
