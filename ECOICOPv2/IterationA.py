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
df = pd.read_csv("ECOICOPv2/Raw-Data-2.csv")
urls = pd.read_csv("ECOICOPv2/Daily-Scraping-Errors.csv")

# Create a null data frame
daily_errors = pd.DataFrame(columns = ["Name","Subclass","Url","Division","Retailer"])
list_ = pd.DataFrame(columns = ["Date","Name","Price","Subclass","Division","Retailer"])

# Define the web-scraping functions for the target retailers


        
#=========================================================================================================
## Manually added data            

#Water EOA Nicosia (https://ndlgo.org.cy/water-supply/water-fees-wbn/) --> Banned access in 17-10-2025
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Πάγιο ανά μήνα - Nicosia")
new_row.append(float(5.5))
new_row.append("Water supply delivered through network systems")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water EOA Nicosia") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)
            
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Κυβικά ανά μήνα - Nicosia")
new_row.append(float(0.5))
new_row.append("Water supply delivered through network systems")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water EOA Nicosia") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Sewerage EOA Nicosia (https://ndlgo.org.cy/sewage/sewer-fees/) --> Banned access in 17-10-2025
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Ετήσιο Τέλος - Nicosia")
new_row.append(float(0.31))
new_row.append("Sewage collection through sewer systems")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Sewerage EOA Nicosia") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)
            
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Τέλος Χρήσης - Nicosia")
new_row.append(float(0.55))
new_row.append("Sewage collection through sewer systems")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Sewerage EOA Nicosia") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)
"""
#Water EOA Limassol (https://eoalemesos.org.cy/el/fees) --> Connection error since 13-03-2026
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Πάγιο ανά μήνα - Limassol")
new_row.append(float(4))
new_row.append("Water supply delivered through network systems")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water EOA Limassol") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Δικαίωμα Συντήρησης ανά μήνα - Limassol")
new_row.append(float(1.5))
new_row.append("Water supply delivered through network systems")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water EOA Limassol") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Κυβικά ανά μήνα - Limassol")
new_row.append(float(0.225))
new_row.append("Water supply delivered through network systems")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Water EOA Limassol") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)

#Sewerage EOA Limassol (https://eoalemesos.org.cy/el/fees) --> Connection error since 13-03-2026
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Ετήσιο Τέλος - Limassol")
new_row.append(float(0.475142857))
new_row.append("Sewage collection through sewer systems")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Sewerage EOA Limassol") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)
            
new_row=[]
new_row.append(datetime.today().strftime("%Y-%m-%d"))
new_row.append("Τέλος Χρήσης - Limassol")
new_row.append(float(0.64))
new_row.append("Sewage collection through sewer systems")
new_row.append("HOUSING, WATER, ELECTRICITY, GAS AND OTHER FUELS")
new_row.append("Sewerage EOA Limassol") 
list_.loc[len(list_)] = new_row
list_['Name'] = list_['Name'].apply(lambda x:x)
"""
#===============================================================================

# Change the type as float
list_["Price"].astype(float)

# Export/Save the scraped data
combined_df = pd.concat([df, list_], axis=0)
combined_df.reset_index(drop=True, inplace=True)
combined_df.to_csv("ECOICOPv2/Raw-Data-2.csv", index=False, header=True)

# Export/Save the unscraped data (daily errors of iteration A) 
daily_errors.to_csv("ECOICOPv2/Daily-Scraping-Errors-IterationA.csv", index=False)
