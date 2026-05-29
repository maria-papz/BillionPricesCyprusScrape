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

#================================================================================================================================
# Alphamega
#================================================================================================================================
print("Alphamega")
url = "https://www.alphamega.com.cy/en/groceries/personal-care/mens-toiletries/shaving/gillette-blue-ii-plus-slalom-disposable-razors-5-pieces"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# SupermarketCy
#================================================================================================================================
print("SupermarketCy")
url = "https://www.supermarketcy.com.cy/sifounas-frantzolakia-stroggyla-4tem"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Stephanis
#================================================================================================================================
print("Stephanis")
url = "https://www.stephanis.com.cy/en/products/396845"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#soup = BeautifulSoup(response.content, "html.parser")    
#element_soup = soup.find_all("div", {"class":"listing-details-heading"})
#if (len(element_soup) < 2):
#    element_soup = element_soup[0]
#else:
#    element_soup = element_soup[1]
#price_ = element_soup.text.replace("€","").replace("\n","")
#print(price_)

#================================================================================================================================
# Public
#================================================================================================================================
print("Public")
url = "https://www.public.cy/public/v1/mm/productPage?sku=1867127&locale=el"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Cablenet
#================================================================================================================================
print("Cablenet")
### Bundled telecommunication services
url = "https://cablenet.com.cy/hbo-max/"

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

#soup = BeautifulSoup(response.content, "html.parser")
#element = soup.find_all("span", {"style":"font-size: 50px"})
#price = float(element[0].text) #Purple Max Mobile HBO Max Edition	
#print(price)

#================================================================================================================================
# Intercity Buses
#================================================================================================================================
print("Intercity Buses")
url = "https://intercity-buses.com/en/routes/nicosia-limassol-limassol-nicosia/"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Moto Race
#================================================================================================================================
print("Moto Race")
url = "https://www.motorace.com.cy/ktm-sx-e-1-20-factory-edition.html"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Centroptical
#================================================================================================================================
print("Centroptical")
url = "https://centroptical-cyprus.com/product/lacoste-3/"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
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
# Wolt
#================================================================================================================================
print("Wolt")
url = "https://wolt.com/en/cyp/nicosia/restaurant/kfc-aglantzia/twister-itemid-692eae75bc0a1e597836f510"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
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

#================================================================================================================================
# EOA Larnaca (https://ndlgo.org.cy/)
#================================================================================================================================
print("Water Board of Larnaca")
url = "https://eoal.org.cy/exypiretisi/teli/teli-chrisis-nerou/"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

print("Sewerage Board of Larnaca")
url = "https://eoal.org.cy/exypiretisi/teli/apocheteftika-teli/"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# EOA Nicosia (https://ndlgo.org.cy/)
#================================================================================================================================
print("Water Board of Nicosia")
url = "https://ndlgo.org.cy/water-supply/water-fees-wbn/"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

print("Sewerage Board of Nicosia")
url = "https://ndlgo.org.cy/sewage/sewer-fees/"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# EOA Limassol (https://eoalemesos.org.cy/el/fees)
#================================================================================================================================
print("Water/Sewerage Board of Limassol")
url = "https://eoalemesos.org.cy/el/fees"

response_1 = requests.get(url)
print(response_1)

headerA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
headerB = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36'}
response_2A = requests.get(url, headers=headerA)
print(response_2A)
response_2B = requests.get(url, headers=headerB)
print(response_2B)

#================================================================================================================================
# Music Avenue
#================================================================================================================================
print("Music Avenue")
url = "https://www.musicavenue.com.cy/product/stagg-c505-1-4-2/"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# Alter Vape
#================================================================================================================================
print("Alter Vape")
url = "https://altervape.eu/product/geekvape-zeus-sub-ohm-76"

response_1 = requests.get(url)
print(response_1)

#header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# E-wholesale
#================================================================================================================================
print("E-wholesale")
url = "https://www.ewsale.com/product-page/ske-crystal-4in1-%CE%B7%CE%BB%CE%B5%CE%BA%CF%84%CF%81%CE%BF%CE%BD%CE%B9%CE%BA%CE%AC-%CF%84%CF%83%CE%B9%CE%B3%CE%AC%CF%81%CE%B1-%CE%BC%CE%AF%CE%B1%CF%82-%CF%87%CF%81%CE%AE%CF%83%CE%B7%CF%82-8-%CF%80%CF%81%CE%BF%CE%B3%CE%B5%CE%BC%CE%B9%CF%83%CE%BC%CE%AD%CE%BD%CE%B5%CF%82-%CE%BA%CE%AC%CF%88%CE%BF%CF%85%CE%BB%CE%B5%CF%82"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

#================================================================================================================================
# The CYgar shop
#================================================================================================================================
print("The CYgar shop")
url = "https://www.thecygarshop.com/product-page/la-aurora-preferidos-hors-d-age-2020"

response_1 = requests.get(url)
print(response_1)

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',}
#header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'}
response_2 = requests.get(url, headers=header)
print(response_2)

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
