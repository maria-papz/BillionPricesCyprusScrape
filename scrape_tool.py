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


##########Andriani#######################
#Defining a function that takes all the urls for the bakery goods and scrape them into two lists
#the product_final and the prices_final. These two are also global defined
def bakery_goods(urls:list):
    #create lists for the products and the prices repsectively
    global products 
    global prices 
    products =[]
    prices = []

    #final list for the products and the prices
    global products_final 
    global prices_final
    products_final =[]
    prices_final =[]

    #for the different urls, putting the prices and the description of the 
    # products in the two lists
    for url in urls:
        page = urlopen(url)
        html = page.read().decode("utf-8")
        bs = BeautifulSoup(html, "html.parser")
    
        scripts = bs.find_all('script',string=True)

        #get the strings for the names and the prices of the products using regular expressions
        for script in scripts:
            product= re.findall(r"'name':.*",str(script))
            price= re.findall(r"'price':.*",str(script))
            if len(product)> 0:
                products.append(product)
                prices.append(price)
            
    #get the description of the items, by removing the ':',',' and the additional quotation marks
    for j in range(len(products)):
        for i in range(len(products[j])):
            products_final.append(products[j][i].split(':')[1].replace(",", "").replace(" ","").strip('\''))
        
    #get the price of the items, by removing the ':',',' and the additional quotation marks
    for j in range(len(prices)):
        for i in range(len(prices[j])):
            prices_final.append(prices[j][i].split(':')[1].replace(",", "").replace(" ","").strip('\''))



#the urls for the bakery goods
urls=["https://www.supermarketcy.com.cy/pites","https://www.supermarketcy.com.cy/tost"
     ,"https://www.supermarketcy.com.cy/psomakia","https://www.supermarketcy.com.cy/almyra","https://www.supermarketcy.com.cy/keik"
     ,"https://www.supermarketcy.com.cy/glyka-1"]


#apply the urls on the function
bakery_goods(urls)

#products already stored in the excel file
products_excel=['ΣίφουναςΠίττεςΆσπρεςΜεγάλες5Τεμ550g','ΣίφουναςΨωμίΦέτεςΤόστΆσπροΜικρό700g'
,'ΣίφουναςΦραντζολάκιαΣτρογγυλά4Τεμ','ΣίφουναςΦραντζολάκιαΜακρόστεναΜεγάλα4Τεμ','ΣίφουναςΚρουασάνΒουτύρου1Τεμ','ΣίφουναςΛουκανικόπιτα1Τεμ'
,'ΣίφουναςΠίταΣάτζιηςΜεΜέλι1Τεμ','ΣίφουναςΕλιόπιταΣφολιάτα1Τεμ','ΣίφουναςΚέικΓεωγραφίας750g','ΣίφουναςMixΣιροπιαστά410g']

#create the list to store only the prices that we care about based on products_excel
prices_excel =[]

#to see which items in prodcuts_final match with the list products_excel
for item in products_excel:
    for product in products_final:
        index = products_final.index(product)
        if item==product:
            prices_excel.append(prices_final[index])

#round the prices to only two decimal points
prices_excel = [ round(float(i),2) for i in prices_excel]

df_bakery=pd.DataFrame()
date = [datetime.now()]*len(prices_excel)
retailer=['SupermarketCy']*len(prices_excel)
product_class=['food']*len(prices_excel)
product_subclass= ['bakery goods']*len(prices_excel)

#store in an excel file
df_bakery = pd.DataFrame({'product_name':products_excel,'product_price':prices_excel,'date_time_scraped':date,'product_class':product_class,'product_subclass':product_subclass,'Retailer':retailer,}) 

##########Andriani#######################
 

# Retrieving data from CSV
df = pd.read_csv("BillionPricesProject_ProductList.csv")


# SupermarketCy breads to scrape
supermarketCy_bread_names=['Σίφουνας Μαύρο Μικρό Ψωμί Κομμένο 500g','Σίφουνας Ολικής Ψωμί Κομμένο 780g','Σίφουνας Κοινό Ψωμί Κομμένο 560g','Σίφουνας Κοινό Ψωμί Κομμένο 970g','Σίφουνας Άσπρο Ψωμί 560g','Σίφουνας Κοινό Ψωμί 970g']
supermarketCy_bread_pages=[1,1,1,1,2,2]

for i in range(6):
    df.loc[len(df)] = supermarketCy_bread(supermarketCy_bread_names[i],supermarketCy_bread_pages[i])
#print(df)

df.append(df_bakery)

df.to_csv("BillionPricesProject_ProductList.csv", index=False)

