import pandas as pd 

# Creating initial dataframe 
df = pd.DataFrame(columns=['product_name','product_price','date_time_scraped','product_class','product_subclass','retailer','subclass_average'])

# Create csv file to store our date
df.to_csv("BillionPricesProject_ProductList.csv",index=False)
#

