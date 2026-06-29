# Important libraries
import pandas as pd 
import warnings
import matplotlib.pyplot as plt
import time

from datetime import datetime
from datetime import datetime, timedelta

# Ignore specific warning
warnings.simplefilter("ignore")

# Date
today = datetime.today().strftime("%Y-%m-%d")
#today = '2026-06-25'

# Read necessary data 
#raw_data_26q3 = pd.read_csv("ECOICOPv2/Datasets/Raw-Data/Raw-Data-2-2026Q3.csv", parse_dates = ['Date'], date_parser = lambda x:pd.to_datetime(x, format = '%Y-%m-%d'))
#raw_data_26q4 = pd.read_csv("ECOICOPv2/Datasets/Raw-Data/Raw-Data-2-2026Q4.csv", parse_dates = ['Date'], date_parser = lambda x:pd.to_datetime(x, format = '%Y-%m-%d'))

# Concatenate/combine by rows the quarterly subsets into a full raw data set
#raw_data = pd.concat([raw_data_26q3, raw_data_26q4
#                     ], axis = 0) 

raw_data = pd.read_csv("ECOICOPv2/Datasets/Raw-Data/Raw-Data-2-2026Q3.csv", parse_dates = ['Date'], date_parser = lambda x:pd.to_datetime(x, format = '%Y-%m-%d'))

# Exclude the data of the following retailers
#raw_data = raw_data[~ ( (raw_data["Retailer"] == "Opa") | (raw_data["Retailer"] == "Cheap Basket") )]  

df_daily_general = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-General-Inflation.csv")
df_daily_division = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-Division.csv")
df_daily_subclass_division = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-Subclass-Division.csv")

weight_ = pd.read_csv("ECOICOPv2/Datasets/ECOICOP2-Matched-Weights.csv")
index_ = pd.read_csv("ECOICOPv2/Datasets/Reference-Values-2.csv")

#Initialization of the computational time
start_time = time.time()

# DIVISION CPI
raw_data_today = raw_data[raw_data["Date"] == today]
raw_data_1 = raw_data_today[["Subclass", "Price"]]
group = raw_data_1.groupby("Subclass").mean()
group.reset_index(inplace = True)
group_df = pd.DataFrame(group)

group_df = group_df[group_df["Subclass"] != "Electricity"] #don't take into account this subclass
group_df = group_df[group_df["Subclass"] != "Water supply delivered through network systems"] #don't take into account this subclass
group_df = group_df[group_df["Subclass"] != "Sewage collection through sewer systems"] #don't take into account this subclass
group_df = group_df.reset_index(drop=True) #Reset index of the above three subclasses

#Electricity
electricity = raw_data_today[raw_data_today["Subclass"] == "Electricity"]
ele_price_ = electricity["Price"].sum()
new_row = []
new_row.append("Electricity")
new_row.append(ele_price_)
group_df.loc[len(group_df)] = new_row
group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)

#Water supply delivered through network systems
waterboard = raw_data_today[raw_data_today["Subclass"] == "Water supply delivered through network systems"]

larnaca_ = 0
larnaca_count = 0
nicosia_ = 0
nicosia_count = 0
limassol_ = 0
limassol_count = 0

for i in range(0, len(waterboard)):
    if "Larnaca" in waterboard.iloc[i]["Name"]:
        larnaca_ += waterboard.iloc[i]["Price"]
        larnaca_count = 1
    if "Nicosia" in waterboard.iloc[i]["Name"]:
        nicosia_ += waterboard.iloc[i]["Price"]
        nicosia_count = 1
    if "Limassol" in waterboard.iloc[i]["Name"]:
        limassol_ += waterboard.iloc[i]["Price"]
        limassol_count = 1
        
wat_price_ = (larnaca_ + nicosia_ + limassol_) / (larnaca_count + nicosia_count + limassol_count)
new_row = []
new_row.append("Water supply delivered through network systems")
new_row.append(wat_price_)
group_df.loc[len(group_df)] = new_row
group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)

#Sewage collection through sewer systems
sewagecollection = raw_data_today[raw_data_today["Subclass"] == "Sewage collection through sewer systems"]

larnaca_ = 0
larnaca_count = 0
nicosia_ = 0
nicosia_count = 0
limassol_ = 0
limassol_count = 0

for i in range(0, len(sewagecollection)):
    if "Larnaca" in sewagecollection.iloc[i]["Name"]:
        larnaca_ += sewagecollection.iloc[i]["Price"]
        larnaca_count = 1
    if "Nicosia" in sewagecollection.iloc[i]["Name"]:
        nicosia_ += sewagecollection.iloc[i]["Price"]
        nicosia_count = 1
    if "Limassol" in sewagecollection.iloc[i]["Name"]:
        limassol_ += sewagecollection.iloc[i]["Price"]
        limassol_count = 1
        
sew_price_ = (larnaca_ + nicosia_ + limassol_) / (larnaca_count + nicosia_count + limassol_count)
new_row = []
new_row.append("Sewage collection through sewer systems")
new_row.append(sew_price_)
group_df.loc[len(group_df)] = new_row
group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)

# ECOICOP weights and weighted average prices per Subclass
df_1 = pd.merge(group_df, weight_, on = 'Subclass')
df_1["Weight_Price_Subclass"] = df_1["Price"] * df_1["Weight"]

df_2 = df_1.groupby("Subclass").sum()
df_2.reset_index(inplace = True)

df_3 = pd.merge(df_2, weight_, on = 'Subclass')
df_3 = df_3[["Subclass", "Division_x", "Price", "Weight_Price_Subclass", "Weight_x"]]
df_3.rename(columns = {'Weight_x':'Weight', 'Division_x':'Division'}, inplace = True)

# Weighted average price per Division
df_4 = df_3.groupby("Division").sum()
df_4.reset_index(inplace = True)
df_4.rename(columns = {'Weight_Price_Subclass': 'Weight_Price_Division_today'}, inplace = True)

# Daily CPI per Division 
df_5 = pd.merge(index_, df_4, on = 'Division')
df_5["CPI Division"] = round(100 * df_5["Weight_Price_Division_today"] / df_5["Weight_Price_Division_reference"], 4)
df_5 = df_5[["Division", "CPI Division", "Weight_Price_Division_today"]]
df_5.rename(columns = {'Weight_Price_Division_today': 'Weight_Price_Division'}, inplace = True)
df_5["Date"] = today

cols = list(df_5.columns)
cols.insert(0, cols.pop(cols.index('Date')))
df_5 = df_5[cols]
df_5['Date'] = pd.to_datetime(df_5['Date']) 

df_5a = pd.concat([df_5, df_daily_division])
df_5a['Date'] = pd.to_datetime(df_5a['Date'])
#df_5a = df_5a.sort_values(by='Date').reset_index(drop=True)
df_5a = df_5a.sort_values(['Date', 'Division']).reset_index(drop = True)
df_5a.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-Division.csv", index = False)

del df_5["Date"]

df_6 = pd.merge(df_1, df_5, on = 'Division')
df_6["Date"] = None
df_6 = df_6[["Date", "Subclass", "Division", "Price", "Weight", "Weight_Price_Subclass", "Weight_Price_Division", "CPI Division"]]
df_6["Date"] = today

combined_df = pd.concat([df_daily_subclass_division, df_6], axis = 0)
combined_df.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-Subclass-Division.csv", index = False)

# Total weighted average price
df_7 = index_[["Division", "Weight"]]

# Drop duplicates
df_8 = df_6[["Division", "CPI Division"]]
df_9 = df_8.drop_duplicates()

# General CPI 
df_10 = pd.merge(df_9, df_7, on = 'Division')
df_10["New"] = df_10["CPI Division"] * df_10["Weight"]
CPI_general = round(df_10["New"].sum(), 4)

# Create a new list and add information
new_row = []
new_row.append(today)
new_row.append(CPI_general)
new_row.append(None)

# General CPI Inflation
df_11 = pd.DataFrame([new_row], columns = ['Date', 'CPI General', 'Inflation (%)'])
df_12 = pd.concat([df_daily_general, df_11], ignore_index = True)
df_12['Inflation (%)'] = 100 * (df_12['CPI General'] - df_12['CPI General'].shift(1)) / df_12['CPI General'].shift(1)
df_12.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-General-Inflation.csv", index = False)

# Daily change (%) of the CPI per Division 
current_day_obj = datetime.strptime(today, "%Y-%m-%d")
current_day_str = current_day_obj.strftime("%Y-%m-%d")
previous_day_obj = current_day_obj - timedelta(days = 1)
previous_day_str = previous_day_obj.strftime("%Y-%m-%d")

# Daily-CPI-Division.csv file
df_daily_cpi_division = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-Division.csv")
prior_df = df_daily_cpi_division[df_daily_cpi_division["Date"] == previous_day_str]
current_df = df_daily_cpi_division[df_daily_cpi_division["Date"] == current_day_str]
unique_divisions = current_df['Division'].unique()

for unique_ in unique_divisions:
    df_13 = float(prior_df[prior_df["Division"] == unique_]["CPI Division"])
    df_14 = float(current_df[current_df["Division"] == unique_]["CPI Division"])
    #df_13 = prior_df[prior_df["Division"] == unique_]["CPI Division"]
    #df_14 = current_df[current_df["Division"] == unique_]["CPI Division"]
    percentage_change = 100 * (df_14 - df_13) / df_13
    
    index_list = current_df[current_df["Division"] == unique_]["CPI Division"].index.tolist()
    float_index_list = [int(i) for i in index_list]
    df_daily_cpi_division.loc[float_index_list, "Daily Change (%)"] = round(percentage_change, 4)

df_daily_cpi_division.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-Division.csv", index = False)

# Daily-CPI-Subclass-Division.csv file
df_daily_cpi_subclass_division = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-Subclass-Division.csv")
prior_df = df_daily_cpi_subclass_division[df_daily_cpi_subclass_division["Date"] == previous_day_str]
current_df = df_daily_cpi_subclass_division[df_daily_cpi_subclass_division["Date"] == current_day_str]
unique_divisions = current_df['Subclass'].unique()

for unique_ in unique_divisions:
    df_15 = float(prior_df[prior_df["Subclass"] == unique_]["CPI Division"])
    df_16 = float(current_df[current_df["Subclass"] == unique_]["CPI Division"])
    #df_15 = prior_df[prior_df["Subclass"] == unique_]["CPI Division"]
    #df_16 = current_df[current_df["Subclass"] == unique_]["CPI Division"]
    percentage_change = 100 * (df_16 - df_15) / df_15            
    
    index_list = current_df[current_df["Subclass"] == unique_]["CPI Division"].index.tolist()
    float_index_list = [int(i) for i in index_list]
    df_daily_cpi_subclass_division.loc[float_index_list, "Daily Change (%)"] = round(percentage_change, 4)

df_daily_cpi_subclass_division.sort_values(["Date","Division"])
df_daily_cpi_subclass_division.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-Subclass-Division.csv", index = False)

#========================================================================================================================
# LAST THURSDAY (*this corresponds to the monthly observation*)
#========================================================================================================================

# Current date
current_date_obj = datetime.strptime(today, "%Y-%m-%d")
current_date_str = current_date_obj.strftime("%Y-%m-%d")

# Read important files
df_monthly_general = pd.read_csv("ECOICOPv2/Results/Monthly/Monthly-CPI-General-Inflation.csv")
df_monthly_division = pd.read_csv("ECOICOPv2/Results/Monthly/Monthly-CPI-Division.csv")
df_daily_general = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-General-Inflation.csv")

# Function for the calculations to be performed every last Thursday per month
def is_last_thursday(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    weekday = date.weekday()
    if weekday == 3 and date.month != (date + timedelta(days = 7)).month:
        return True
    return False

# Call the function
if is_last_thursday(current_date_str):
    df_current_date = df_daily_general.tail(1)
    
    # Monthly CPI per Division
    df_5b = df_5[["Division", "CPI Division"]]
    df_5b["Date"] = current_date_str
    df_monthly_division = pd.concat([df_5b, df_monthly_division], ignore_index = True)
    #df_monthly_division = df_monthly_division.sort_values(by = 'Date')
    df_monthly_division = df_monthly_division.sort_values(['Date', 'Division'])
    cols = list(df_monthly_division.columns)
    cols.insert(0, cols.pop(cols.index('Date')))
    df_monthly_division = df_monthly_division[cols]

    prior_df = df_monthly_division[len(df_monthly_division) - 24 : len(df_monthly_division) - 12]
    current_df = df_monthly_division[len(df_monthly_division) - 12 : len(df_monthly_division)]
    unique_divisions = df_monthly_division['Division'].unique()
    
    for unique_ in unique_divisions:
        df_17 = float(prior_df[prior_df["Division"] == unique_]["CPI Division"])
        df_18 = float(current_df[current_df["Division"] == unique_]["CPI Division"])
        #df_17 = prior_df[prior_df["Division"] == unique_]["CPI Division"]
        #df_18 = current_df[current_df["Division"] == unique_]["CPI Division"]
        percentage_change = 100 * (df_18 - df_17) / df_17
    
        index_list = current_df[current_df["Division"] == unique_]["CPI Division"].index.tolist()
        float_index_list = [int(i) for i in index_list]
        df_monthly_division.loc[float_index_list, "Monthly Change (%)"] = round(percentage_change, 4)

    df_monthly_division.to_csv("ECOICOPv2/Results/Monthly/Monthly-CPI-Division.csv", index=False)

    # Monthly CPI General Inflation
    df_monthly_general = pd.concat([df_current_date, df_monthly_general], ignore_index = True)
    df_monthly_general = df_monthly_general.sort_values(by = 'Date')
    df_monthly_general["Inflation (%)"] = round(100 * (df_monthly_general['CPI General'] - df_monthly_general['CPI General'].shift(1)) / df_monthly_general['CPI General'].shift(1), 4)   
    df_monthly_general.to_csv("ECOICOPv2/Results/Monthly/Monthly-CPI-General-Inflation.csv", index = False)
else:
    pass

# Total computational/processing time
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time / 60, "minutes")

'''
############################################################################################################################################

# If you want to re-calculate everything between two specific dates, then run the following while-loop :

############################################################################################################################################

start_date = datetime.strptime("2026-06-17", "%Y-%m-%d")
end_date   = datetime.strptime("2026-06-19", "%Y-%m-%d")

today_p = start_date

# Initialization of the computational/processing time
start_time = time.time()

## While loop 

while today_p <= end_date:
    today_f = today_p.strftime("%Y-%m-%d")
    print(today_f)
    
    # Read necessary data: 
    #raw_data_26q3 = pd.read_csv("ECOICOPv2/Datasets/Raw-Data/Raw-Data-2-2026Q3.csv", parse_dates = ['Date'], date_parser = lambda x:pd.to_datetime(x, format = '%Y-%m-%d'))
    #raw_data_26q4 = pd.read_csv("ECOICOPv2/Datasets/Raw-Data/Raw-Data-2-2026Q4.csv", parse_dates = ['Date'], date_parser = lambda x:pd.to_datetime(x, format = '%Y-%m-%d'))

    # Concatenate/combine by rows the quarterly subsets into a full raw data set:
    #raw_data = pd.concat([raw_data_26q3, raw_data_26q4
    #                     ], axis=0) 
    
    raw_data = pd.read_csv("ECOICOPv2/Datasets/Raw-Data/Raw-Data-2-2026Q3.csv", parse_dates = ['Date'], date_parser = lambda x:pd.to_datetime(x, format = '%Y-%m-%d'))

    # Exclude the data of the following retailers: 
    #raw_data = raw_data[~ ( (raw_data["Retailer"] == "Opa") | (raw_data["Retailer"] == "Cheap Basket") )] 
    
    df_daily_general = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-General-Inflation.csv")
    df_daily_division = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-Division.csv")
    df_daily_subclass_division = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-Subclass-Division.csv")
    
    weight_ = pd.read_csv("ECOICOPv2/Datasets/ECOICOP2-Matched-Weights.csv")
    index_ = pd.read_csv("ECOICOPv2/Datasets/Reference-Values-2.csv")
    
    # DIVISION CPI:
    raw_data_today = raw_data[raw_data["Date"] == today_p]
    raw_data_1 = raw_data_today[["Subclass", "Price"]]
    group = raw_data_1.groupby("Subclass").mean()
    group.reset_index(inplace = True)
    group_df = pd.DataFrame(group)
    
    group_df = group_df[group_df["Subclass"] != "Electricity"] #don't take into account this subclass
    group_df = group_df[group_df["Subclass"] != "Water supply delivered through network systems"] #don't take into account this subclass
    group_df = group_df[group_df["Subclass"] != "Sewage collection through sewer systems"] #don't take into account this subclass
    group_df = group_df.reset_index(drop=True) #Reset index of the above three subclasses
    
    #Electricity
    electricity = raw_data_today[raw_data_today["Subclass"] == "Electricity"]
    ele_price_ = electricity["Price"].sum()
    new_row = []
    new_row.append("Electricity")
    new_row.append(ele_price_)
    group_df.loc[len(group_df)] = new_row
    group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)
    
    #Water supply delivered through network systems
    waterboard = raw_data_today[raw_data_today["Subclass"] == "Water supply delivered through network systems"]
    
    larnaca_ = 0
    larnaca_count = 0
    nicosia_ = 0
    nicosia_count = 0
    limassol_ = 0
    limassol_count = 0
    
    for i in range(0, len(waterboard)):
        if "Larnaca" in waterboard.iloc[i]["Name"]:
            larnaca_ += waterboard.iloc[i]["Price"]
            larnaca_count=1
        if "Nicosia" in waterboard.iloc[i]["Name"]:
            nicosia_ += waterboard.iloc[i]["Price"]
            nicosia_count = 1
        if "Limassol" in waterboard.iloc[i]["Name"]:
            limassol_ += waterboard.iloc[i]["Price"]
            limassol_count = 1
            
    wat_price_= (larnaca_ + nicosia_ + limassol_) / (larnaca_count + nicosia_count + limassol_count)
    new_row = []
    new_row.append("Water supply delivered through network systems")
    new_row.append(wat_price_)
    group_df.loc[len(group_df)] = new_row
    group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)
    
    #Sewage collection through sewer systems
    sewagecollection = raw_data_today[raw_data_today["Subclass"] == "Sewage collection through sewer systems"]
    
    larnaca_ = 0
    larnaca_count = 0
    nicosia_ = 0
    nicosia_count = 0
    limassol_ = 0
    limassol_count = 0
    
    for i in range(0, len(sewagecollection)):
        if "Larnaca" in sewagecollection.iloc[i]["Name"]:
            larnaca_ += sewagecollection.iloc[i]["Price"]
            larnaca_count = 1
        if "Nicosia" in sewagecollection.iloc[i]["Name"]:
            nicosia_ += sewagecollection.iloc[i]["Price"]
            nicosia_count = 1
        if "Limassol" in sewagecollection.iloc[i]["Name"]:
            limassol_ += sewagecollection.iloc[i]["Price"]
            limassol_count = 1
            
    sew_price_= (larnaca_ + nicosia_ + limassol_) / (larnaca_count + nicosia_count + limassol_count)
    new_row = []
    new_row.append("Sewage collection through sewer systems")
    new_row.append(sew_price_)
    group_df.loc[len(group_df)] = new_row
    group_df['Subclass'] = group_df['Subclass'].apply(lambda x:x)
    
    # ECOICOP weights and weighted average prices per Subclass:
    df_1 = pd.merge(group_df, weight_, on = 'Subclass')
    df_1["Weight_Price_Subclass"] = df_1["Price"] * df_1["Weight"]
    
    df_2 = df_1.groupby("Subclass").sum()
    df_2.reset_index(inplace = True)
    
    df_3 = pd.merge(df_2, weight_, on = 'Subclass')
    df_3 = df_3[["Subclass", "Division_x", "Price", "Weight_Price_Subclass", "Weight_x"]]
    df_3.rename(columns = {'Weight_x':'Weight', 'Division_x':'Division'}, inplace = True)
    
    # Weighted average price per Division
    df_4 = df_3.groupby("Division").sum()
    df_4.reset_index(inplace = True)
    df_4.rename(columns = {'Weight_Price_Subclass':'Weight_Price_Division_today'}, inplace = True)
    
    # Daily CPI per Division 
    df_5 = pd.merge(index_, df_4, on = 'Division')
    df_5["CPI Division"] = round(100 * df_5["Weight_Price_Division_today"] / df_5["Weight_Price_Division_reference"], 4)
    df_5 = df_5[["Division", "CPI Division", "Weight_Price_Division_today"]]
    df_5.rename(columns = {'Weight_Price_Division_today':'Weight_Price_Division'}, inplace = True)
    df_5["Date"] = today_f
    
    cols = list(df_5.columns)
    cols.insert(0, cols.pop(cols.index('Date')))
    df_5 = df_5[cols]
    df_5['Date'] = pd.to_datetime(df_5['Date']) 
    
    df_5a = pd.concat([df_5, df_daily_division])
    df_5a['Date'] = pd.to_datetime(df_5a['Date'])
    #df_5a = df_5a.sort_values(by = 'Date').reset_index(drop = True)
    df_5a = df_5a.sort_values(['Date', 'Division']).reset_index(drop = True)
    df_5a.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-Division.csv", index = False)
    
    del df_5["Date"]
    
    df_6 = pd.merge(df_1, df_5, on = 'Division')
    df_6["Date"] = None
    df_6 = df_6[["Date", "Subclass", "Division", "Price", "Weight", "Weight_Price_Subclass", "Weight_Price_Division", "CPI Division"]]
    df_6["Date"] = today_f
    
    combined_df = pd.concat([df_daily_subclass_division, df_6], axis = 0)
    combined_df.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-Subclass-Division.csv", index = False)
    
    # Total weighted average price
    df_7 = index_[["Division", "Weight"]]
    
    # Drop duplicates
    df_8 = df_6[["Division", "CPI Division"]]
    df_9 = df_8.drop_duplicates()
    
    # General CPI 
    df_10 = pd.merge(df_9, df_7, on = 'Division')
    df_10["New"] = df_10["CPI Division"] * df_10["Weight"]
    CPI_general = round(df_10["New"].sum(), 4)
    
    # Create a new list and add information
    new_row = []
    new_row.append(today_f)
    new_row.append(CPI_general)
    new_row.append(None)
    
    # General CPI Inflation
    df_11 = pd.DataFrame([new_row], columns = ['Date', 'CPI General', 'Inflation (%)'])
    df_12 = pd.concat([df_daily_general, df_11], ignore_index = True)
    df_12['Inflation (%)'] = 100 * (df_12['CPI General'] - df_12['CPI General'].shift(1)) / df_12['CPI General'].shift(1)
    df_12.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-General-Inflation.csv", index = False)
    
    # Daily change (%) of the CPI per Division 
    previous_day_obj =  today_p - timedelta(days = 1)
    previous_day_str = previous_day_obj.strftime("%Y-%m-%d")
    
    # Daily-CPI-Division.csv file
    df_daily_cpi_division = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-Division.csv")
    prior_df = df_daily_cpi_division[df_daily_cpi_division["Date"] == previous_day_str]
    current_df = df_daily_cpi_division[df_daily_cpi_division["Date"] == today_f]
    unique_divisions = current_df['Division'].unique()
    
    for unique_ in unique_divisions:
        df_13 = float(prior_df[prior_df["Division"] == unique_]["CPI Division"])
        df_14 = float(current_df[current_df["Division"] == unique_]["CPI Division"])
        #df_13 = prior_df[prior_df["Division"] == unique_]["CPI Division"]
        #df_14 = current_df[current_df["Division"] == unique_]["CPI Division"]
        percentage_change = 100 * (df_14 - df_13) / df_13
        
        index_list = current_df[current_df["Division"] == unique_]["CPI Division"].index.tolist()
        float_index_list = [int(i) for i in index_list]
        df_daily_cpi_division.loc[float_index_list, "Daily Change (%)"] = round(percentage_change, 4)
    
    df_daily_cpi_division.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-Division.csv", index=False)
    
    # Daily-CPI-Subclass-Division.csv file
    df_daily_cpi_subclass_division = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-Subclass-Division.csv")
    prior_df = df_daily_cpi_subclass_division[df_daily_cpi_subclass_division["Date"] == previous_day_str]
    current_df = df_daily_cpi_subclass_division[df_daily_cpi_subclass_division["Date"] == today_p]
    unique_divisions = current_df['Subclass'].unique()
    
    for unique_ in unique_divisions:
        df_15 = float(prior_df[prior_df["Subclass"] == unique_]["CPI Division"])
        df_16 = float(current_df[current_df["Subclass"] == unique_]["CPI Division"])
        #df_15 = prior_df[prior_df["Subclass"] == unique_]["CPI Division"]
        #df_16 = current_df[current_df["Subclass"] == unique_]["CPI Division"]
        percentage_change = 100 * (df_16 - df_15) / df_15            
        
        index_list = current_df[current_df["Subclass"] == unique_]["CPI Division"].index.tolist()
        float_index_list = [int(i) for i in index_list]
        df_daily_cpi_subclass_division.loc[float_index_list, "Daily Change (%)"] = round(percentage_change, 4)

    df_daily_cpi_subclass_division.sort_values(["Date","Division"])
    df_daily_cpi_subclass_division.to_csv("ECOICOPv2/Results/Daily/Daily-CPI-Subclass-Division.csv", index = False)
    
    #========================================================================================================================
    # LAST THURSDAY (*this corresponds to the monthly observation*)
    #========================================================================================================================
    
    # Read important files
    today_date = datetime.strptime(today_f, "%Y-%m-%d")
    current_date = today_date.strftime("%Y-%m-%d")
    
    # Read important files
    df_monthly_general = pd.read_csv("ECOICOPv2/Results/Monthly/Monthly-CPI-General-Inflation.csv")
    df_monthly_division = pd.read_csv("ECOICOPv2/Results/Monthly/Monthly-CPI-Division.csv")
    df_daily_general = pd.read_csv("ECOICOPv2/Results/Daily/Daily-CPI-General-Inflation.csv")
    
    # Function for the calculations to be performed every last Thursday per month
    def is_last_thursday(date):
        date = datetime.strptime(date, "%Y-%m-%d")
        weekday = date.weekday()
        if weekday == 3 and date.month != (date + timedelta(days=7)).month:
            return True
        return False
    
    # Call the function
    if is_last_thursday(current_date):
        df_current_date = df_daily_general.tail(1)
        
        # Monthly CPI per Division
        df_5b = df_5[["Division", "CPI Division"]]
        df_5b["Date"] = current_date
        df_monthly_division = pd.concat([df_5b, df_monthly_division], ignore_index = True)
        #df_monthly_division = df_monthly_division.sort_values(by = 'Date')
        df_monthly_division = df_monthly_division.sort_values(['Date', 'Division'])
        cols = list(df_monthly_division.columns)
        cols.insert(0, cols.pop(cols.index('Date')))
        df_monthly_division = df_monthly_division[cols]
    
        prior_df = df_monthly_division[len(df_monthly_division) - 24 : len(df_monthly_division) - 12]
        current_df = df_monthly_division[len(df_monthly_division) - 12 : len(df_monthly_division)]
        unique_divisions = df_monthly_division['Division'].unique()
        
        for unique_ in unique_divisions:
            df_17 = float(prior_df[prior_df["Division"] == unique_]["CPI Division"])
            df_18 = float(current_df[current_df["Division"] == unique_]["CPI Division"])
            #df_17 = prior_df[prior_df["Division"] == unique_]["CPI Division"]
            #df_18 = current_df[current_df["Division"] == unique_]["CPI Division"]
            percentage_change = 100 * (df_18 - df_17) / df_17
        
            index_list = current_df[current_df["Division"] == unique_]["CPI Division"].index.tolist()
            float_index_list = [int(i) for i in index_list]
            df_monthly_division.loc[float_index_list, "Monthly Change (%)"] = round(percentage_change, 4)
    
        df_monthly_division.to_csv("ECOICOPv2/Results/Monthly/Monthly-CPI-Division.csv", index=False)
    
        # Monthly CPI General Inflation
        df_monthly_general = pd.concat([df_current_date, df_monthly_general], ignore_index = True)
        df_monthly_general = df_monthly_general.sort_values(by ='Date')
        df_monthly_general["Inflation (%)"] = round(100 * (df_monthly_general['CPI General'] - df_monthly_general['CPI General'].shift(1)) / df_monthly_general['CPI General'].shift(1), 4)   
        df_monthly_general.to_csv("ECOICOPv2/Results/Monthly/Monthly-CPI-General-Inflation.csv", index = False)
    else:
        pass
    
    today_p += timedelta(days=1)
    
    #####################################################    End of while-loop    ########################################################
 
 # Total computational/processing time
 end_time = time.time()
 elapsed_time = end_time - start_time
 print("Elapsed time:", elapsed_time / 60, "minutes")    

'''
