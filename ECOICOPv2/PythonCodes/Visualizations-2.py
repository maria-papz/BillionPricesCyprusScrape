#Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from datetime import datetime, timedelta 

#Import data
df_daily = pd.read_csv("Results/Daily/Daily-CPI-General-Inflation.csv")

plt.figure(figsize=(10, 6))
plt.plot(df_daily['Date'], df_daily['Inflation (%)'], linestyle='-', marker='o', color='b', label='Inflation')

## Plot the time evolution of the daily CPI Inflation

# Show on the horizontal x-axis only the date of the first day per month 
df_daily['Date'] = pd.to_datetime(df_daily['Date'])
plt.figure(figsize=(12,6))
plt.plot(df_daily['Date'], df_daily['Inflation (%)'], marker='o')

for date, cpi in zip(df_daily['Date'], df_daily['Inflation (%)']):
    if date.day == 1:
        plt.annotate(f'{cpi:.2f}', (date, cpi), textcoords="offset points", xytext=(0,10), ha='center')

locator = mdates.DayLocator(bymonthday=1)
formatter = mdates.DateFormatter('%d-%m-%Y')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title("Daily Evolution of CPI Inflation in Cyprus", fontsize=18)
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily/Daily-Inflation.png')
plt.show()

'''
# Show on the horizontal x-axis all the dates
for i, txt in enumerate(df_daily['Inflation (%)']):
    plt.annotate(f'{txt:.2f}', (df_daily['Date'][i], df_daily['Inflation (%)'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title("Daily Evolution of CPI Inflation in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily/Daily-Inflation.png')
plt.show()
plt.figure(figsize=(10,6))
plt.plot(df_daily['Date'], df_daily['Inflation (%)'], linestyle='-', marker='o', color='b', label='CPI General')
'''

## Plot the time evolution of the daily General CPI

# Show on the horizontal x-axis only the date of the first day per month
df_daily['Date'] = pd.to_datetime(df_daily['Date'])
plt.figure(figsize=(12,6))
plt.plot(df_daily['Date'], df_daily['CPI General'], marker='o')

for date, cpi in zip(df_daily['Date'], df_daily['CPI General']):
    if date.day == 1:
        plt.annotate(f'{cpi:.2f}', (date, cpi), textcoords="offset points", xytext=(0,10), ha='center')

locator = mdates.DayLocator(bymonthday=1)
formatter = mdates.DateFormatter('%d-%m-%Y')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel('Date')
plt.ylabel('CPI General (27/06/2024 = base = 77.89)')
plt.title("Daily Evolution of General CPI in Cyprus", fontsize=18)
plt.xticks(rotation=90)
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily/Daily-CPI-General.png')
plt.show()

'''
# Show on the horizontal x-axis all the dates
for i, txt in enumerate(df_daily['CPI General']):
    plt.annotate(f'{txt:.2f}', (df_daily['Date'][i], df_daily['CPI General'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('CPI General (27/06/2024 = base)')
plt.title("Daily Evolution of General CPI in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('Results/Daily/Daily-CPI-General.png')
plt.show()
plt.figure(figsize=(10,6))
plt.plot(df_daily['Date'], df_daily['CPI General'], linestyle='-', marker='o', color='b', label='CPI General')
'''

#========================================================================================================================
# LAST THURSDAY (*this corresponds to the monthly observation*)
#========================================================================================================================

#Current date
current_date = datetime.today().strftime("%Y-%m-%d")
#current_date = '2026-04-30' #*set manually the date of the last Thursday of the month

#Read data
df_monthly = pd.read_csv("Results/Monthly/Monthly-CPI-General-Inflation.csv")

#Function to run every last Thursday per month
def is_last_thursday(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    if weekday == 3 and date.month != (date + timedelta(days=7)).month:
        return True
    return False

if is_last_thursday(current_date):
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_monthly['Date'], df_monthly['Inflation (%)'], linestyle='-', marker='o', color='b', label='Inflation')

    #Plot the time evolution of the monthly CPI Inflation
    for i, txt in enumerate(df_monthly['Inflation (%)']):
        plt.annotate(f'{txt:.2f}', (df_monthly['Date'][i], df_monthly['Inflation (%)'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
    plt.xlabel('Date')
    plt.ylabel('Inflation (%)')
    plt.title("Monthly Evolution of CPI Inflation in Cyprus", fontsize=18)
    plt.xticks(rotation=90) 
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Results/Monthly/Monthly-Inflation.png')
    plt.show()
    
    plt.figure(figsize=(10, 6))
    plt.plot(df_monthly['Date'], df_monthly['CPI General'], linestyle='-', marker='o', color='b', label='CPI General')

    #Plot the time evolution of the monthly General CPI 
    for i, txt in enumerate(df_monthly['CPI General']):
        plt.annotate(f'{txt:.2f}', (df_monthly['Date'][i], df_monthly['CPI General'][i]), textcoords="offset points", xytext=(0,10), ha='center')
        
    plt.xlabel('Date')
    plt.ylabel('CPI General (27/06/2024 = base)')
    plt.title("Monthly Evolution of General CPI in Cyprus", fontsize=18)
    plt.xticks(rotation=90) 
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('Results/Monthly/Monthly-CPI-General.png')
    plt.show()
else:
    pass
