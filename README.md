
# Billion Prices Cyprus Scrape Project

## Overview

The Billion Prices Cyprus Scrape project involves scraping prices of around 1000 products from 40 retailers on a daily basis. The scraped data is then used to calculate the Consumer Price Index (CPI) against a reference basket.

## Scraping Process

The scraping process is handled by the scrape_tool.py script. It collects information such as product name, price, subclass, retailers, and subclass average. This data is written to the BillionPricesProject_ProductList.csv file. To add supermarket products for scraping without coding, one can directly modify the AlphaMega.csv file.

## Calculation Process

The calculation of mean prices and CPI measures is performed by the calculations.py script. It reads the Ref_weights.csv file, which contains subclass and division weights, names, and means of the reference basket. The script calculates the mean prices (including division and total) for the scraped products of the day and generates the CPI measures. The results are written to the Calculations.csv file, along with the date and time of calculation.

## Scraped Websites

- SupermarketCy -> https://www.supermarketcy.com.cy/  

- Alphamega -> https://www.alphamega.com.cy 

- Marks & Spencer -> https://www.marksandspencer.com/cy  

- Athlokinisi -> https://athlokinisi.com.cy/  

- FamousSport -> [Famous Sports - Sportswear, Footwear, Swimwear, Sports Apparel (famousports.com) ](https://www.famousports.com/en)

- Berska -> [Select gender | Bershka ](https://www.bershka.com/cy/h-man.html)

- Stradivarious -> [Stradivarius Cyprus - New Collection Summer 2023 | Cyprus ](https://www.stradivarius.com/cy/)

- The CYgar Shop -> https://www.thecygarshop.com/ 

- NUMBEO -> https://www.numbeo.com/cost-of-living/country_price_rankings?itemId=17&displayCurrency=EUR

- E-WHOLESALE -> https://www.ewsale.com/tsigaro   

- Altervape -> https://altervape.eu

- The Royal Cigars Strovolos -> https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos

- Primetel -> [PrimeTel for Home: Internet, Telephony, Mobile, Television](https://primetel.com.cy/en) 

- CYTA -> [Ιδιώτες | Cyta ](https://www.cyta.com.cy/personal)

- Epic -> [Epic | Mobile, Internet, Fixed, TV | www.epic.com.cy ](https://www.epic.com.cy/en/page/start/home)

- Stephanis -> https://www.stephanis.com.cy/en  

- Electroline -> https://www.electroline.com.cy  

- Cablenet -> Cablenet: TV, Mobile & the Fastest Internet in Cyprus 

- IKEA -> https://www.ikea.com.cy  

- AWOL -> [ADVENTURE WITHOUT LIMITS (awol.com.cy) ](https://www.awol.com.cy)

- Moto Race -> https://www.motorace.com.cy/  

- Mazda -> https://www.mazda.com.cy/home  

- Nissan -> https://www.nissan.com.cy/   

- Bwell Pharmacy -> https://bwell.com.cy/  

- Novella Hair Salon -> [Novella Hair Mode | Hair and Beauty Salon in Nicosia Cyprus](https://cablenet.com.cy/en/) 

- Tripadvisor -> https://www.tripadvisor.com.gr/Restaurants-g190372-Cyprus.html  

- Wolt (PizzaHut, Costa Coffee, Piazza Gourounaki Nicosia, Pixida Nicosia, Kofini Tavern Limassol, Vlachos Taverna Larnaca, Zakos Beach Restaurant Larnaca, Pafos Tavernaki Pafos, Ocean Basket Pafos, Mcdonalds )à 

- PizzaHut -> [Order Your Favorite Pizza for Delivery from Pizza Hut Cyprus ](https://www.pizzahut.com.cy)

- Cera -> https://www.cera.org.cy/Templates/00001/data/hlektrismos/kostos_xrisis.pdf 

- Cyprus Post -> https://www.cypruspost.post/uploads/2cf9ec4f5a.pdf                    

- Water Board of Nicosia (Nicosia +Larnaca) -> https://www.wbn.org.cy/%CE%BA%CE%B1%CF%84%CE%B1%CE%BD%CE%B1%CE%BB%CF%89%CF%84%CE%AE%CF%82/%CE%B4%CE%B9%CE%B1%CF%84%CE%B9%CE%BC%CE%AE%CF%83%CE%B5%CE%B9%CF%82/   

https://www.lwb.org.cy/en/charges-and-fees.html 

- Sewerage Board of Nicosia -> https://www.sbn.org.cy/el/apoxeteftika-teli  

- Sewerage Board of Limassol -> https://www.sbla.com.cy/en/ 

- Sewerage Board of Larnaca -> https://www.lsdb.org.cy/en/services/financial-information/sewage-charges/ 

- Petrol Prices -> https://www.fueldaddy.com.cy/en

- Booking -> https://www.booking.com/  

- Rio Cinemas -> [Rio Cinemas – Movie Theaters in Cyprus](http://www.riocinemas.com.cy) 

- University of Nicosia -> https://www.unic.ac.cy/sites/tuition_fees/UNIC-CY-EU-Tuition%20Fees%202022-2023.pdf   

- European University Cyprus -> https://syllabus.euc.ac.cy/tuitions/euc-tuition-fees-c.pdf  

- Cyprus Ministry of Education, Sport & Youth -> http://www.moec.gov.cy/idiotiki_ekpaidefsi/didaktra.html  

 
 

## GitHub Actions

The project utilizes GitHub Actions to automate the scraping process. The repository contains the following YAML files within the ./github/workflows directory:

### run-daily-scrape.yml: 
This file schedules the execution of scrape_tool.py and calculations.py scripts on a daily basis.
### initialise-clear-csv.yml: 
Whenever a pull request is made targeting the initialise or initialize branch, this file runs initial.py to reset the BillionPricesProject_ProductList.csv file.
### initialise_clear_calculations.yml: 
Whenever a pull request is made targeting the initialise_c or initialize_c branch, this file runs initialise_calculations.py to reset the Calculations.csv file.

