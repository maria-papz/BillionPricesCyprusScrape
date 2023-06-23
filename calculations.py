import pandas as pd 
from datetime import date, datetime

#read from csv 
weights = pd.read_csv("Ref_weights.csv")
products = pd.read_csv("BillionPricesProject_ProductList.csv")
calculations = pd.read_csv("Calculations.csv")

# Convert to resolve typos
weights['subclass'] = weights['subclass'].str.lower()
products['product_subclass'] = products['product_subclass'].str.lower()
products['product_subclass'] = products['product_subclass'].replace('yogurt', 'yoghurt')
products['product_subclass'] = products['product_subclass'].replace('miscellaneous printer matter', 'miscellaneous printed matter')
products['product_subclass'] = products['product_subclass'].replace('other tobaco products', 'other tobacco products')
products['product_subclass'] = products['product_subclass'].replace('hairdressing for men', 'hairdressing for men and children')

# Convert 'date time scraped' column to datetime type
products['date_time_scraped'] = pd.to_datetime(products['date_time_scraped'])

# Filter products for today's date
today = date.today()
products_today = products[products['date_time_scraped'].dt.date == today]


# Merge the weights dataframe with the 'Subclass Average' column from products_today
df = weights.merge(products_today[['product_subclass', 'subclass_average']].drop_duplicates(), 
                   left_on='subclass', right_on='product_subclass', how='left')

# Drop the redundant 'product_subclass' column
df.drop('product_subclass', axis=1, inplace=True)
df.drop_duplicates(subset=['subclass'], inplace=True)

df['weighted.mean.price'] = df['subclass_average'] * df['weight.subclass']
df['weighted.mean.price.division'] = df.groupby(['division'], as_index=False)['weighted.mean.price'].transform('sum')
df['weighted.mean.price.total'] = df.groupby('division')['weighted.mean.price.division'].first().sum()
df['weight.matched']=df['weight.subclass']*df['matching']
df['weight.matched.division'] = df.groupby(['division'], as_index=False)['weight.matched'].transform('sum')
df['weight.matched.total'] = df['weight.matched'].sum()
df['datetime.calculated']= [datetime.now()]*len(df)



df['CPI_total']=100*(df['weighted.mean.price.total']/df['reference.weighted.mean.price.total'])
df['CPI_division']=100*(df['weighted.mean.price.division'])/df['reference.weighted.mean.price.division']
df['weighted_CPI_division']=df['weight.matched.division']*df['CPI_division']
df['CPI_general'] = df.groupby('division')['weighted_CPI_division'].first().sum()

calculations = pd.concat([calculations,df])

df.to_csv("Calculations.csv")

