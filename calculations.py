# Import libraries
import pandas as pd 
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta, TH
from bs4 import BeautifulSoup
import re
import tabula as tb
import requests

# Read data from csv files 
weights = pd.read_csv("Ref_weights.csv")
products = pd.read_csv("BillionPricesProject_ProductList.csv")
calculations = pd.read_csv("Calculations.csv",  index_col=0)

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

# Assuming 'datetime.calculated' column is a string in the format 'YYYY-MM-DD HH:MM:SS'
calculations['datetime.calculated'] = pd.to_datetime(calculations['datetime.calculated'])

last_recorded_date = calculations['datetime.calculated'].dt.date.max()
calculations_yesterday = calculations[calculations['datetime.calculated'].dt.date == last_recorded_date]

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

if len(calculations_yesterday['CPI_total']) == 0:
    print('yayz')
    df['CPI_total_inflation']=round(100*((df['CPI_total']-CPI_ref_total)/CPI_ref_total),4)
    df['CPI_general_inflation']=round(100*((df['CPI_general']-CPI_ref_general)/CPI_ref_general),4)
else:
    print('yass')
    calculations_yesterday = calculations_yesterday.set_index(df.index)
    df['CPI_total_inflation']=round(100*((df['CPI_total']-calculations_yesterday['CPI_total'])/calculations_yesterday['CPI_total']+ 1e-8),4)
    df['CPI_general_inflation']=round(100*((df['CPI_general']-calculations_yesterday['CPI_general'])/calculations_yesterday['CPI_general']+ 1e-8),4)

calculations = pd.concat([calculations,df],ignore_index=True)
calculations = calculations.reset_index(drop=True)

# For the *monthly* inflation get the General CPI value on the *last Thursday* of each month 
calculations['date'] = calculations['datetime.calculated'].dt.date

#get the last thursday per month
def get_thurs(dt):
    return dt + relativedelta(day=31, weekday=TH(-1))

thursdays = list(set(get_thurs(calculations['date'])))
thursdays = sorted(thursdays)

#create the new columns/this step is only needed when one does calculations over again for all dates
#calculations['CPI_general_lastthursday'] = None
#calculations['monthly_inflation_lastthursday'] = None

for i in range(len(thursdays)):
    if calculations[calculations['date']==thursdays[i]].empty:
        try:
            rate = calculations[(calculations['subclass']=='rice')&(calculations['date']==thursdays[i]-timedelta(days=1))].iloc[0]['CPI_general']
            calculations.loc[(calculations['date']==thursdays[i]-timedelta(days=1)),'CPI_general_lastthursday'] = rate
            if thursdays[i-1]-timedelta(days=1)<thursdays[i]-timedelta(days=1) and not calculations.loc[calculations['date']==thursdays[i],'CPI_general_lastthursday'].empty:
                prev_rate = calculations[(calculations['subclass']=='rice')&(calculations['date']==thursdays[i-1]-timedelta(days=1))].iloc[0]['CPI_general']
                calculations.loc[(calculations['date']==thursdays[i]-timedelta(days=1)),'monthly_inflation_lastthursday'] = round(100*(rate - prev_rate)/rate,4)
            else:
                calculations.loc[(calculations['date']==thursdays[i]),'monthly_inflation_lastthursday'] = None
             
        except IndexError:
            calculations.loc[(calculations['date']==thursdays[i]),'CPI_general_lastthursday'] = None
            
    else:
        rate = calculations[(calculations['subclass']=='rice')&(calculations['date']==thursdays[i])].iloc[0]['CPI_general']
        calculations.loc[(calculations['date']==thursdays[i]),'CPI_general_lastthursday'] = rate
        if thursdays[i-1]<thursdays[i] and not calculations.loc[calculations['date']==thursdays[i],'CPI_general_lastthursday'].empty:
            try:
                prev_rate = calculations[(calculations['subclass']=='rice')&(calculations['date']==thursdays[i-1])].iloc[0]['CPI_general']
            except IndexError:
                prev_rate = calculations[(calculations['subclass']=='rice')&(calculations['date']==thursdays[i-1]-timedelta(days=1))].iloc[0]['CPI_general']
            calculations.loc[(calculations['date']==thursdays[i]),'monthly_inflation_lastthursday'] = round(100*(rate - prev_rate)/rate,4)
        else:
            calculations.loc[(calculations['date']==thursdays[i]),'monthly_inflation_lastthursday'] = None
        
calculations.drop(columns=['date'], inplace=True)

#===============================================================================================================================================================
# Add the CPI Inflation official report results of CyStat
#===============================================================================================================================================================

url = 'https://www.cystat.gov.cy/en/SubthemeStatistics?id=47'
response = requests.get(url)
links_list = []
soup = BeautifulSoup(response.content, 'html.parser')
target_links = soup.find_all('a', href=lambda href: href and '/PressRelease?id=' in href)

#remove numbers from string
def strip_numbers(input_string):
    return re.sub(r'\d+', '', input_string)

#create the new columns/this step is only needed when one does calculations over again for all dates
#calculations['CPI_general_cystat']= None
#calculations['CPI_monthly_inflation_cystat'] = None

calculations['month'] = calculations['datetime.calculated'].dt.strftime('%B')
calculations['month'] = calculations['month'].astype(str)

for link in target_links:
    links_list.append(link['href'])

for link in links_list:
    url_pdf = 'https://www.cystat.gov.cy/en' + link

    response = requests.get(url_pdf)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        iframes = soup.find_all('iframe')
    if iframes:
        pdf = re.findall("https.+pdf",str(iframes[0]))
        pdf = pdf[0]

    if 'Consumer_Price_Index' in pdf:
        cpi = tb.read_pdf(pdf, pages = '2',pandas_options={'header': None}, stream=True)
        cpi_general_cystat = cpi[2].iloc[12][2]
        cpi_monthly_cystat = cpi[2].iloc[12][4]
        month = strip_numbers(re.findall('-.+\d\d-',pdf)[0]).strip('-')
        if calculations.loc[calculations['month'].str.contains(month),'CPI_general_cystat'].isna().any(): 
            calculations.loc[calculations['month'].str.contains(month),'CPI_general_cystat'] = float(cpi_general_cystat.replace(',','.'))
            calculations.loc[calculations['month'].str.contains(month),'CPI_monthly_inflation_cystat'] = float(cpi_monthly_cystat.replace(',','.'))

calculations.drop(columns=['month'], inplace=True)

calculations.to_csv("Calculations.csv")
