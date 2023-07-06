import pandas as pd 

# Creating initial dataframe 
df = pd.DataFrame(columns=['division',	'subclass',	'weight.division',	'weight.subclass',	'matching',	'reference.mean.price',	'reference.weighted.mean.price',	'reference.weighted.mean.price.division',	'reference.weighted.mean.price.total',	'subclass_average',	'weighted.mean.price',	'weighted.mean.price.division',	'weighted.mean.price.total',	'weight.matched',	'weight.matched.division',	'weight.matched.total','datetime.calculated','CPI_total','CPI_division','weighted_CPI_division','CPI_general','CPI_total_inflation','CPI_general_inflation'])

# Create csv file to store our date
df.to_csv("Calculations.csv",index=False)
#

