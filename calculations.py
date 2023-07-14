import pandas as pd 
from datetime import date, datetime, timedelta

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

yestarday= today - timedelta(days = 1)
calculations_yesterday=calculations[products['date_time_scraped'].dt.date == yestarday]


# Merge the weights dataframe with the 'Subclass Average' column from products_today
df = weights.merge(products_today[['product_subclass', 'subclass_average']].drop_duplicates(), 
                   left_on='subclass', right_on='product_subclass', how='left')

# Drop the redundant 'product_subclass' column
df.drop('product_subclass', axis=1, inplace=True)
df.drop_duplicates(subset=['subclass'], inplace=True)

df['weighted.mean.price'] = round(df['subclass_average'] * df['weight.subclass'],4)
df['weighted.mean.price.division'] = round(df.groupby(['division'], as_index=False)['weighted.mean.price'].transform('sum'),4)
df['weighted.mean.price.total'] = round(df.groupby('division')['weighted.mean.price.division'].first().sum(),4)
df['weight.matched']=round(df['weight.subclass']*df['matching'],4)
df['weight.matched.division'] = round(df.groupby(['division'], as_index=False)['weight.matched'].transform('sum'),4)
df['weight.matched.total'] = round(df['weight.matched'].sum(),4)
df['datetime.calculated']= [datetime.now()]*len(df)



df['CPI_total']=round(100*(df['weighted.mean.price.total']/df['reference.weighted.mean.price.total']),4)
df['CPI_division']=round(100*(df['weighted.mean.price.division'])/df['reference.weighted.mean.price.division'],4)
df['weighted_CPI_division']=round(df['weight.matched.division']*df['CPI_division'],4)
df['CPI_general'] = round(df.groupby('division')['weighted_CPI_division'].first().sum(),4)
CPI_ref_total=[100]*len(df)
CPI_ref_general=df['weight.matched.total']*100
if calculations_yesterday['CPI_total']:
    df['CPI_total_inflation']=round(100*((df['CPI_total']-calculations_yesterday['CPI_total'])/calculations_yesterday['CPI_total']),4)
    df['CPI_general_inflation']=round(100*((df['CPI_general']-calculations_yesterday['CPI_general'])/calculations_yesterday['CPI_general']),4)
else:
    df['CPI_total_inflation']=round(100*((df['CPI_total']-CPI_ref_total)/CPI_ref_total),4)
    df['CPI_general_inflation']=round(100*((df['CPI_general']-CPI_ref_general)/CPI_ref_general),4)

calculations = pd.concat([calculations,df],ignore_index=True)

calculations.to_csv("Calculations.csv")

