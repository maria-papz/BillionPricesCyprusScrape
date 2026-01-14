
# Billion Prices Cyprus Scrape Project

## Overview

The Billion Prices Cyprus Scrape project involves scraping prices of around 2500 products from 40 retailers on a daily basis. The scraped data is then used to calculate the Consumer Price Index (CPI) against a reference basket.

*An improved and updated version of this repository is found here:* https://github.com/kvitalis/CyBPP/tree/main 

## Scraping Process

The scraping process is handled by the scrape_tool.py script. It collects information such as product name, price, subclass, retailers, and subclass average. This data is written to the BillionPricesProject_ProductList.csv file. To add supermarket products for scraping without coding, one can directly modify the AlphaMega.csv file.

## Calculation Process

The calculation of mean prices and CPI measures is performed by the calculations.py script. It reads the Ref_weights.csv file, which contains subclass and division weights, names, and means of the reference basket. The script calculates the mean prices (including division and total) for the scraped products of the day and generates the CPI measures. The results are written to the Calculations.csv file, along with the date and time of calculation.

## Scraped Websites

- Adventure Without Limits (AWOL)	https://www.awol.com.cy/ 

- Alphamega	https://www.alphamega.com.cy/ 

- Alter Vape	https://altervape.eu/ 

- Athlokinisi	https://athlokinisi.com.cy/ 

- Bwell Pharmacy	https://bwell.com.cy/ 

- Cablenet	https://cablenet.com.cy/ 

- Consumer Protection Service	https://consumer.gov.cy/gr/ 

- Cyprus Energy Regulation Authority (CERA)	https://www.cera.org.cy/Templates/00001/data/hlektrismos/kostos_xrisis.pdf 

- Cyprus Ministry of Education, Sport and Youth	https://www.moec.gov.cy/idiotiki_ekpaidefsi/didaktra.html 

- Cyprus Post	https://www.cypruspost.post/uploads/2cf9ec4f5a.pdf 

- Cyprus Telecommunications Authority (CYTA)	https://www.cyta.com.cy/personal 

- Epic	https://www.epic.com.cy/en/page/start/home 

- E-WHOLESALE	https://www.ewsale.com/tsigaro 

- Electroline	https://electroline.com.cy/ 

- European University Cyprus	https://syllabus.euc.ac.cy/tuitions/euc-tuition-fees-c.pdf 

- Famous Sports	https://www.famousports.com/en 

- FuelDaddy (Agip, EKO, Eni, Esso, Fill n GO, Petrolina, Shell, Staroil, Total Plus)	https://www.fueldaddy.com.cy/en 

- IKEA	https://www.ikea.com.cy/

- Marks & Spencer	https://www.marksandspencer.com/cy/ 

- Mazda	https://www.mazda.com.cy/home 

- Moto Race	https://www.motorace.com.cy/ 

- Nissan	https://www.nissan.com.cy/ 

- Novella Hair Salon	https://novella.com.cy/ 

- NUMBEO	https://www.numbeo.com/cost-of-living/country_price_rankings?itemId=17&displayCurrency=EUR 

- Pizza Hut	https://www.pizzahut.com.cy/ 

- Primetel	https://primetel.com.cy/en 

- Rio Cinemas	http://www.riocinemas.com.cy/ 

- Sewerage Board of Limassol-Amathus (SBLA)	https://www.sbla.com.cy/Sewage-Charges 

- Sewerage Board of Nicosia (SBN)	https://www.sbn.org.cy/el/apoxeteftika-teli 

- Sewerage and Drainage Board of Larnaca (LSDB)	https://www.lsdb.org.cy/en/services/financial-information/sewage-charges/ 

- Stephanis	https://www.stephanis.com.cy/en 

- Stradivarius	https://www.stradivarius.com/cy/ 

- SupermarketCy	https://www.supermarketcy.com.cy/ 

- The CYgar Shop	https://www.thecygarshop.com/ 

- The Royal Cigars 	https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos 

- Water Board of Nicosia (WBN)	https://www.wbn.org.cy/%CE%BA%CE%B1%CF%84%CE%B1%CE%BD%CE%B1%CE%BB%CF%89%CF%84%CE%AE%CF%82/%CE%B4%CE%B9%CE%B1%CF%84%CE%B9%CE%BC%CE%AE%CF%83%CE%B5%CE%B9%CF%82/ 

- Water Board of Larnaca (LWB)	https://www.lwb.org.cy/en/charges-and-fees.html 

- Water Board of Limassol (WBL)	https://www.wbl.com.cy/el/water-rates 

- Wolt (Costa Coffee, Piatsa Gourounaki Nicosia, Pixida Nicosia, Kofini Tavern Limassol, Vlachos Taverna Larnaca, Zakos Beach Restaurant Larnaca, Paphos Tavernaki, Ocean Basket Paphos, McDonald’s)	https://wolt.com/en/cyp 

## GitHub Actions

The project utilizes GitHub Actions to automate the scraping process. The repository contains the following YAML files within the ./github/workflows directory:

### run-daily-scraping-and-calculations.yml: 
This file schedules the execution of the scrape_tool.py and calculations.py scripts on a daily basis.
### initialise-clear-csv.yml: 
Whenever a pull request is made targeting the initialise or initialize branch, this file runs initial.py to reset the BillionPricesProject_ProductList.csv file.
### initialise_clear_calculations.yml: 
Whenever a pull request is made targeting the initialise_c or initialize_c branch, this file runs initialise_calculations.py to reset the Calculations.csv file.

