#Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from datetime import datetime, timedelta 

#Import data
df_daily_general = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-General-Inflation.csv")

plt.figure(figsize = (10, 6))
plt.plot(df_daily_general['Date'], df_daily_general['Inflation (%)'], linestyle = '-', marker = 'o', color = 'b', label = 'Inflation')

## Plot the time evolution of the daily CPI Inflation

# Show on the horizontal x-axis only the date of the first day per month 
df_daily_general['Date'] = pd.to_datetime(df_daily_general['Date'])
plt.figure(figsize = (12,6))
plt.plot(df_daily_general['Date'], df_daily_general['Inflation (%)'], marker = 'o')

for date, cpi in zip(df_daily_general['Date'], df_daily_general['Inflation (%)']):
    if date.day == 1:
        plt.annotate(f'{cpi:.2f}', (date, cpi), textcoords = "offset points", xytext = (0,10), ha = 'center')

locator = mdates.DayLocator(bymonthday = 1)
formatter = mdates.DateFormatter('%d-%m-%Y')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title("Daily Evolution of CPI Inflation in Cyprus", fontsize = 18)
plt.xticks(rotation = 90)
plt.grid(True)
plt.tight_layout()
plt.savefig('ECOICOPv2/Results/Daily/Daily-Inflation.png')
plt.show()

'''
# Show on the horizontal x-axis all the dates
for i, txt in enumerate(df_daily_general['Inflation (%)']):
    plt.annotate(f'{txt:.2f}', (df_daily_general['Date'][i], df_daily_general['Inflation (%)'][i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.xlabel('Date')
plt.ylabel('Inflation (%)')
plt.title("Daily Evolution of CPI Inflation in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('ECOICOPv2/Results/Daily/Daily-Inflation.png')
plt.show()
plt.figure(figsize=(10,6))
plt.plot(df_daily_general['Date'], df_daily_general['Inflation (%)'], linestyle='-', marker='o', color='b', label='CPI General')
'''

## Plot the time evolution of the daily General CPI

# Show on the horizontal x-axis only the date of the first day per month
df_daily_general['Date'] = pd.to_datetime(df_daily_general['Date'])
plt.figure(figsize = (12,6))
plt.plot(df_daily_general['Date'], df_daily_general['CPI General'], marker = 'o')

for date, cpi in zip(df_daily_general['Date'], df_daily_general['CPI General']):
    if date.day == 1:
        plt.annotate(f'{cpi:.2f}', (date, cpi), textcoords = "offset points", xytext = (0,10), ha = 'center')

locator = mdates.DayLocator(bymonthday = 1)
formatter = mdates.DateFormatter('%d-%m-%Y')
plt.gca().xaxis.set_major_locator(locator)
plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel('Date')
plt.ylabel('General CPI (2025=100)')
plt.title("Daily Evolution of General CPI in Cyprus", fontsize = 18)
plt.xticks(rotation = 90)
plt.grid(True)
plt.tight_layout()
plt.savefig('ECOICOPv2/Results/Daily/Daily-CPI-General.png')
plt.show()

'''
# Show on the horizontal x-axis all the dates
for i, txt in enumerate(df_daily_general['CPI General']):
    plt.annotate(f'{txt:.2f}', (df_daily_general['Date'][i], df_daily_general['CPI General'][i]), textcoords = "offset points", xytext = (0,10), ha = 'center')

plt.xlabel('Date')
plt.ylabel('General CPI (2025=100)')
plt.title("Daily Evolution of General CPI in Cyprus", fontsize=18)
plt.xticks(rotation=90) 
plt.grid(True)
plt.tight_layout()
plt.savefig('ECOICOPv2/Results/Daily/Daily-CPI-General.png')
plt.show()
plt.figure(figsize=(10,6))
plt.plot(df_daily_general['Date'], df_daily_general['CPI General'], linestyle='-', marker='o', color='b', label='CPI General')
'''

## Plot the time evolution of the daily CPI per Division

#Import data
df_daily_division = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-Division.csv")

df_daily_division["Date"] = pd.to_datetime(df_daily_division["Date"])
df_daily_division = df_daily_division.sort_values("Date")
plt.figure(figsize = (16,8))

for division in df_daily_division["Division"].unique():
    temp = df_daily_division[df_daily_division["Division"] == division]
    plt.plot(temp["Date"], temp["CPI Division"], label = division, linewidth = 2)

plt.title("Evolution of Daily CPI per Division in Cyprus")
plt.xlabel("Date")
plt.ylabel("Division CPI (2025=100)")
plt.legend(title = "Division", bbox_to_anchor = (1.02, 1), loc = "upper left")
plt.grid(True)
plt.tight_layout()
plt.savefig("ECOICOPv2/Results/Daily/Daily-CPI-Division.png", dpi = 300, bbox_inches = "tight")
plt.show()

#========================================================================================================================
# LAST THURSDAY (*this corresponds to the monthly observation*)
#========================================================================================================================

#Current date
current_date = datetime.today().strftime("%Y-%m-%d")
#current_date = '2026-07-30' #*set manually the date of the last Thursday of the month

#Read data
df_monthly_general = pd.read_csv("ECOICOPv2/Results/Monthly/Monthly-CPI-General-Inflation.csv")

#Function to run every last Thursday per month
def is_last_thursday(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    if weekday == 3 and date.month != (date + timedelta(days = 7)).month:
        return True
    return False

if is_last_thursday(current_date):
    
    plt.figure(figsize = (10, 6))
    plt.plot(df_monthly_general['Date'], df_monthly_general['Inflation (%)'], linestyle = '-', marker = 'o', color = 'b', label = 'Inflation')

    #Plot the time evolution of the monthly CPI Inflation
    for i, txt in enumerate(df_monthly_general['Inflation (%)']):
        plt.annotate(f'{txt:.2f}', (df_monthly_general['Date'][i], df_monthly_general['Inflation (%)'][i]), textcoords = "offset points", xytext = (0,10), ha = 'center')
        
    plt.xlabel('Date')
    plt.ylabel('Inflation (%)')
    plt.title("Monthly Evolution of CPI Inflation in Cyprus", fontsize = 18)
    plt.xticks(rotation = 90) 
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('ECOICOPv2/Results/Monthly/Monthly-Inflation.png')
    plt.show()
    
    plt.figure(figsize = (10, 6))
    plt.plot(df_monthly_general['Date'], df_monthly_general['CPI General'], linestyle = '-', marker = 'o', color = 'b', label = 'CPI General')

    #Plot the time evolution of the monthly General CPI 
    for i, txt in enumerate(df_monthly_general['CPI General']):
        plt.annotate(f'{txt:.2f}', (df_monthly_general['Date'][i], df_monthly_general['CPI General'][i]), textcoords = "offset points", xytext = (0,10), ha = 'center')
        
    plt.xlabel('Date')
    plt.ylabel('General CPI (2025=100)')
    plt.title("Monthly Evolution of General CPI in Cyprus", fontsize = 18)
    plt.xticks(rotation=90) 
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('ECOICOPv2/Results/Monthly/Monthly-CPI-General.png')
    plt.show()
else:
    pass
