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
urls = pd.read_csv("ECOICOPv2/Daily-Scraping-Errors-IterationA.csv")

# Create a null data frame
daily_errors = pd.DataFrame(columns = ["Name","Subclass","Url","Division","Retailer"])
list_ = pd.DataFrame(columns = ["Date","Name","Price","Subclass","Division","Retailer"])

# Define the web-scraping functions for the target retailers


        
# Change the type as float
list_["Price"].astype(float)

# Export/Save the scraped data
combined_df = pd.concat([df, list_], axis=0)
combined_df.reset_index(drop=True, inplace=True)
combined_df.to_csv("ECOICOPv2/Raw-Data-2.csv", index=False, header=True)

# Export/Save the unscraped data (daily errors of iteration B) 
daily_errors.to_csv("ECOICOPv2/Daily-Scraping-Errors-IterationB.csv", index=False)
