
# Billion Prices Cyprus Scrape Project

## Overview

The Billion Prices Cyprus Scrape project involves scraping prices of around 2500 products from 40 retailers on a daily basis. The scraped data is then used to calculate the Consumer Price Index (CPI) against a reference basket.

*An improved and updated version of this repository is found here:* https://github.com/kvitalis/CyBPP/tree/main 

## Scraping Process

The scraping process is handled by the scrape_tool.py script. It collects information such as product name, price, subclass, retailers, and subclass average. This data is written to the BillionPricesProject_ProductList.csv file. To add supermarket products for scraping without coding, one can directly modify the AlphaMega.csv file.

## Calculation Process

The calculation of mean prices and CPI measures is performed by the calculations.py script. It reads the Ref_weights.csv file, which contains subclass and division weights, names, and means of the reference basket. The script calculates the mean prices (including division and total) for the scraped products of the day and generates the CPI measures. The results are written to the Calculations.csv file, along with the date and time of calculation.

## GitHub Actions

The project utilizes GitHub Actions to automate the scraping process. The repository contains the following YAML files within the ./github/workflows directory:

### run-daily-scraping-and-calculations.yml: 
This file schedules the execution of the scrape_tool.py and calculations.py scripts on a daily basis.
### initialise-clear-csv.yml: 
Whenever a pull request is made targeting the initialise or initialize branch, this file runs initial.py to reset the BillionPricesProject_ProductList.csv file.
### initialise_clear_calculations.yml: 
Whenever a pull request is made targeting the initialise_c or initialize_c branch, this file runs initialise_calculations.py to reset the Calculations.csv file.

