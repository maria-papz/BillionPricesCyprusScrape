#  Before running install libraries
# pip install "lxml"
# pip install "requests"

# Import libraries
import pandas as pd 
from lxml import html
import requests
from datetime import datetime
import time

# XPath for breads in supermarketCy has a repeating pattern (may have the same pattern for other categories of the website as well)
# We create a function so that there is no need to find the XPath for every bread added
# Accepts name of bread and page the bread is found
# Returns scraped data
def supermarketCy_bread(bread_name,page):
    
    ## retailer 
    retailer='SupermarketCy'

    ## product class
    product_class='food'

    ## product type
    product_subclass='Bread'

    # Request the page
    page = requests.get('https://www.supermarketcy.com.cy/psomi?page='+str(page))

    # Parsing the page
    # (We need to use page.content rather than
    # page.text because html.fromstring implicitly
    # expects bytes as input.)
    tree = html.fromstring(page.content) 

    ## product name
    product_name=tree.xpath('//div[@data-title=\''+bread_name+'\']/a/h5/text()')
    # convert to string and remove whitespace
    product_name = (''.join(product_name)).replace(' ','').strip()

    ## product price
    product_price = tree.xpath('//div[@data-title=\''+bread_name+'\']/div[@class="flex-col sm:flex-row"]/div[@class=\'sm:mr-10 flex justify-between\']//div/div[@class=\'text-primary text-h4 font-medium mb-8\']/text()')
    product_price=float((''.join(product_price)).replace(' ','').replace('€','').replace(',','.').strip())

    ## scraping time
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")

    # returning list resembling row of dataframe
    new_row=[product_name, product_price,date_time_scraped,product_class,product_subclass,retailer,0]
    return new_row


# Retrieving data from CSV
df = pd.read_csv("BillionPricesProject_ProductList.csv")


# SupermarketCy breads to scrape
supermarketCy_bread_names=['Σίφουνας Μαύρο Μικρό Ψωμί Κομμένο 500g','Σίφουνας Ολικής Ψωμί Κομμένο 780g','Σίφουνας Κοινό Ψωμί Κομμένο 560g','Σίφουνας Κοινό Ψωμί Κομμένο 970g','Σίφουνας Άσπρο Ψωμί 560g','Σίφουνας Κοινό Ψωμί 970g']
supermarketCy_bread_pages=[1,1,1,1,2,2]

for i in range(6):
    df.loc[len(df)] = supermarketCy_bread(supermarketCy_bread_names[i],supermarketCy_bread_pages[i])
#print(df)

df.to_csv("BillionPricesProject_ProductList.csv", index=False)