


#  Before running install libraries
# pip install "lxml"
# pip install "requests"

# Import libraries
import pandas as pd 
import re
from lxml import html
import requests
from datetime import datetime
import time
import xlsxwriter
from urllib.request import urlopen
from bs4 import BeautifulSoup

# XPath for breads in supermarketCy has a repeating pattern (may have the same pattern for other categories of the website as well)
# We create a function so that there is no need to find the XPath for every bread added
# Accepts name of bread and page the bread is found
# Returns scraped data
def supermarketCy_bread(item):
    p=[]

    for pages in range(1,11):
        flag=0
        ## retailer 
        retailer='SupermarketCy'

        ## product class
        # product_class=item['product_class']

        ## product type
        product_subclass=item['product_subclass']
        # Request the page
        page = requests.get('https://www.supermarketcy.com.cy/'+item['webpage']+'?page='+str(pages))

        # Parsing the page
        # (We need to use page.content rather than
        # page.text because html.fromstring implicitly
        # expects bytes as input.)
        tree = html.fromstring(page.content) 

        ## product name
        product_name=tree.xpath('//div[@data-title=\''+item['names']+'\']/a/h5/text()')

        # convert to string and remove whitespace
        product_name = (''.join(product_name)).replace(' ','').strip()
 
        if(product_name==''):
            flag=1
        else:
            ## product price
            #print(product_name)
            product_price = tree.xpath('//div[contains(@data-title,\''+item['names']+'\')]/div[@class="flex-col sm:flex-row"]/div[@class=\'sm:mr-10 flex justify-between\']//div/div[@class=\'text-primary text-h4 font-medium mb-8\']/text()')
            product_price=float((''.join(product_price)).replace(' ','').replace('€','').replace(',','.').strip())

            ## scraping time
            now = datetime.now()
            date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")

            # returning list resembling row of dataframe
            new_row=[product_name, product_price,date_time_scraped,product_subclass,retailer,0]
            flag=0
            return new_row
    return 




# ##########Andriani#######################
# #Defining a function that takes all the urls for the bakery goods and scrape them into two lists
# #the product_final and the prices_final. These two are also global defined
# def bakery_goods(urls:list):
#     #create lists for the products and the prices repsectively
#     global products 
#     global prices 
#     products =[]
#     prices = []

#     #final list for the products and the prices
#     global products_final 
#     global prices_final
#     products_final =[]
#     prices_final =[]

#     #for the different urls, putting the prices and the description of the 
#     # products in the two lists
#     for url in urls:
#         page = urlopen(url)
#         html = page.read().decode("utf-8")
#         bs = BeautifulSoup(html, "html.parser")
    
#         scripts = bs.find_all('script',string=True)

#         #get the strings for the names and the prices of the products using regular expressions
#         for script in scripts:
#             product= re.findall(r"'name':.*",str(script))
#             price= re.findall(r"'price':.*",str(script))
#             if len(product)> 0:
#                 products.append(product)
#                 prices.append(price)
            
#     #get the description of the items, by removing the ':',',' and the additional quotation marks
#     for j in range(len(products)):
#         for i in range(len(products[j])):
#             products_final.append(products[j][i].split(':')[1].replace(",", "").replace(" ","").strip('\''))
        
#     #get the price of the items, by removing the ':',',' and the additional quotation marks
#     for j in range(len(prices)):
#         for i in range(len(prices[j])):
#             prices_final.append(prices[j][i].split(':')[1].replace(",", "").replace(" ","").strip('\''))



# #the urls for the bakery goods
# urls=["https://www.supermarketcy.com.cy/pites","https://www.supermarketcy.com.cy/tost"
#      ,"https://www.supermarketcy.com.cy/psomakia","https://www.supermarketcy.com.cy/almyra","https://www.supermarketcy.com.cy/keik"
#      ,"https://www.supermarketcy.com.cy/glyka-1"]


# #apply the urls on the function
# bakery_goods(urls)

# #products already stored in the excel file
# products_excel=['ΣίφουναςΠίττεςΆσπρεςΜεγάλες5Τεμ550g','ΣίφουναςΨωμίΦέτεςΤόστΆσπροΜικρό700g'
# ,'ΣίφουναςΦραντζολάκιαΣτρογγυλά4Τεμ','ΣίφουναςΦραντζολάκιαΜακρόστεναΜεγάλα4Τεμ','ΣίφουναςΚρουασάνΒουτύρου1Τεμ','ΣίφουναςΛουκανικόπιτα1Τεμ'
# ,'ΣίφουναςΠίταΣάτζιηςΜεΜέλι1Τεμ','ΣίφουναςΕλιόπιταΣφολιάτα1Τεμ','ΣίφουναςΚέικΓεωγραφίας750g','ΣίφουναςMixΣιροπιαστά410g']

# #create the list to store only the prices that we care about based on products_excel
# prices_excel =[]

# #to see which items in prodcuts_final match with the list products_excel
# for item in products_excel:
#     for product in products_final:
#         index = products_final.index(product)
#         if item==product:
#             prices_excel.append(prices_final[index])

# #round the prices to only two decimal points
# prices_excel = [ round(float(i),2) for i in prices_excel]

# df_bakery=pd.DataFrame()
# date = [datetime.now()]*len(prices_excel)
# retailer=['SupermarketCy']*len(prices_excel)
# product_class=['food']*len(prices_excel)
# product_subclass= ['bakery goods']*len(prices_excel)

# #store in an excel file
# df_bakery = pd.DataFrame({'product_name':products_excel,'product_price':prices_excel,'date_time_scraped':date,'product_class':product_class,'product_subclass':product_subclass,'Retailer':retailer,}) 

# ##########Andriani#######################
 
urls_bakery=[["/pites","/tost","/psomakia","/almyra","/keik","/glyka-1","/glyka-1?page=2","/krakers","/krakers?page=2","/kritsinia","/kritsinia?page=2",
"/kroutons","/fryganies","/paximadia","/paximadia?page=2","/koulourakia"],
['ΣίφουναςΠίττεςΆσπρεςΜεγάλες5Τεμ550g', 'ΣίφουναςΨωμίΦέτεςΤόστΆσπροΜικρό700g', 'ΣίφουναςΦραντζολάκιαΣτρογγυλά4Τεμ', 'ΣίφουναςΦραντζολάκιαΜακρόστεναΜεγάλα4Τεμ', 
'ΣίφουναςΚρουασάνΒουτύρου1Τεμ', 'ΣίφουναςΛουκανικόπιτα1Τεμ', 'ΣίφουναςΠίταΣάτζιηςΜεΜέλι1Τεμ', 'ΣίφουναςΕλιόπιταΣφολιάτα1Τεμ', 'ΣίφουναςΚέικΓεωγραφίας750g', 'ΣίφουναςMixΣιροπιαστά410g',
"7DaysMiniBakeRollsΠίτσα80g","BakandysΧωριάτικαΚριτσίνιαΣιταρένια275g","ΜαρίαςΠαξιμάδιαΓλυκανίσου300g","JohnsofΚρουτόνιαΟλικήςΆλεσης320g",
"EliteΦρυγανιέςΜεΣίκαλη360g3+1Δώρο","EliteΦρυγανιέςΟλικήςΆλεσης360g3+1Δώρο","BakandysΠαξιμάδιαΣικάλεως250g","Johnsof NapolitanoΣταφίδαςΑμυγδάλου240g"]]

urls_cereals=[["/dimitriaka?page=1","/dimitriaka?page=2","/dimitriaka?page=3","/dimitriaka?page=4","/dimitriaka?page=5","/dimitriaka?page=6","/dimitriaka?page=7","/dimitriaka?page=8","/dimitriaka?page=9"],
['QuakerΝιφάδεςΒρώμης500g', 'QuakerΤραγανέςΜπουκιέςΒρώμηΣοκολάτα450g',"OreoO'sCereal350g",'KelloggsCornFlakes375g', 'KelloggsCocoPopsChocos375g',
 'KelloggsCocoPops500g', 'KelloggsSpecialK500g','KelloggsMielPopsLoops330g']]

urls_pastas=[["/makaronia","/makaronia?page=2","/makaronia?page=3","/makaronia?page=4","/penes","/penes?page=2",
"/kritharaki"],['BarillaΣπαγγέτιNo5500g', 'ΜέλισσαPrimoGustoΣπαγγέτιNo6500g', 'ΜέλισσαPrimoGustoΚριθαράκι500g',
'ΜιτσίδηΣπαγέττι500g','ΜιτσίδηΚριθαράκι500g','ΜιτσίδηΜακαρόνιαΑ500g','ΜιτσίδηΧωριάτικαΜακαρόνια500g','ΘίιαμβοςΣπαγέττο500g']]

urls_rice = [["/parmpoil", "/parmpoil?page=2","/mpasmati","/karolina","/glase","/pourgouri"],
['3ΑΡύζιΠάρποιλτ1kg', 'BensOriginalΡύζιΜακρύκοκκο10Λεπτά1kg', 'TildaΡυζιΜπασματι1kg', '3ΑΡύζιΜπασμάτι1kg',
 '3ΑΡύζιΓλασσέ1kg', 'ΑφοίΑ.ΚεπόλαΠουργούρι1kg','ΑφοίΑ.ΚεπόλαΠουργούρι500g', 'ΜιτσίδηΠουργούρι500g', 'ΜιτσίδηΠουργούρι1kg',
'3ΑΠουργούρι500g','NaturalLifeΑποφλειωμένοΠουργούριΠιλάφι500g']]

urls_saltspices = [["/alati","/piperi","/mpacharika","/meigmata","/aromatika"],['SailorΑλάτι250g', 'CarnationSpicesΠιπέριΜαύροΑλεσμένο34g', 
'CarnationSpicesΚανέλαΑλεσμένη34g', 'CarnationSpicesΠάπρικαΓλυκιά30g', 'CarnationSpicesΚουρκουμάςΚιτρινόριζα30g', 'KnorrAromatΜείγμαΛαχανικών&amp;Μυρωδικών90g', 
'CarnationSpicesΔιάφοραΒότανα12g', 'CarnationSpicesΣκόρδοΣκόνη40g', 'CarnationSpicesΡίγανη30g', 'CarnationSpicesΘυμάρι10g', 'CarnationSpicesΚόλιανδροςΣκόνη20g', 
'CarnationSpicesΜαϊδανός10g', 'CarnationSpicesΒασιλικός10g', 'CarnationSpicesΆνηθος10g', 'CarnationSpicesΔεντρολίβανοΛάσμαρι10g']]

urls_nuts = [["/xiroi-karpoi","/xiroi-karpoi?page=2","/xiroi-karpoi?page=3","/xiroi-karpoi?page=4","/xiroi-karpoi?page=5","/apoxiramena-frouta",
"/apoxiramena-frouta?page=2","/apoxiramena-frouta?page=3","/apoxiramena-frouta?page=4"],['ΛειβαδιώτηΠράσινηΣφραγίδαΑμύγδαλα120g', 'SeranoΚάσιους140g', 
'ΛειβαδιώτηΚαρυδόψιχα140g', 'SeranoEconomyPackΦουντούκιαΩμά350g', 'SeranoΦυστικόψιχαΚαβουρδισμένηΑλατισμένη175g','ΕποχέςΑποξηραμέναΣύκα350g', 
'ΑμαλίαΧρυσόμηλαΑποξηραμένα250g', 'SeranoSnackin&#039;GoodΑποξηραμέναΔαμάσκηναΧωρίςΠρόσθετηΖάχαρη275g', 'ΚαρπόςΑπόΤηΓηΜαςΑποξηραμέναΒερίκοκα400g', 'ΑμαλίαΦοινίκιαΤυνησίας250g', 'SeranoΣταφίδες350g']]

urls_jams = [["/meli","/meli?page=2","/meli?page=3","/marmelades","/pralines","/fystikovoutyro","/diafora-aleimmata"],['RoyalBeeΜέλι475g', 'MavroudesΜέλι380g',
 'ΤοΤζιβέρτιΜέλιΑνθέωνSqueeze485g', 'BonapiΜέλιΑνθέων450g','BlossomΜαρμελάδαΜερίδες6x30g', 'Nutella200g', 'ΌλυμποςSuperSpreadΦυστικοβούτυροΤραγανό350g', 'DfΤαχίνι250g']]

urls_crisps = [["/patatakia"],['ΧαραλάμπουςΓαριδάκιαΜεΤυρί10X22g']]

urls_sauces=[["/ntomatas","/ntomatas?page=2","/ntomatas?page=3","/ketsap","/ketsap?page=2","/magionezes","/magionezes?page=2",
"/zomoi","/zomoi?page=2","/zomoi?page=3"],['PelargosΚλασικό3X250g', 'ΜιτσίδηΠάσταΝτομάτας4X70g', 'BlossomΠάσταΝτομάτας4X70g', 
'KeanPomiloriΠεραστήΝτομάτα690g', 'SwsΠάσταΝτομάτας425g','ΜιτσίδηΠεραστήΝτομάτα3x500g', 'HeinzΚέτσαπ700g-0,50€',
 'HeinzΜαγιονέζα395g-0.50cents', 'MaggiΖωμόςΚότας12Τεμ','MaggiΖωμόςΛαχανικών16Τεμ','MaggiΖωμόςΓιαΖυμαρικά12Τεμ','KnorrΖωμόςΚότας12Τεμ',
 'KnorrΖωμόςΛαχανικών12Τεμ']]

urls_oil=[["/elaiolado","/elaiolado?page=2"],['ΆγιοςΓεώργιοςΚυπριακόΠαρθένοΕλαιόλαδο1L',
'ΕλιοχώριΠαρθένοΕλαιόλαδο2L', 'ΣεκέπΠαρθένοΕλαιόλαδο1L']]

urls_otheroil=[["/ilianthelaio"],
['LesieurΗλιανθέλαιο3L', 'AmbrosiaΗλιανθέλαιο3L','FloraΗλιανθέλαιο3L', 'AmbrosiaΗλιανθέλαιο4L']]

urls_preservedfish=[["/tonou","/tonou?page=2","/tonou?page=3"],['SevycoΆσπροςΤόνοςΣεΕλαιόλαδο4X95g', 'SevycoΤόνοςΣεΝερό4X200g',
 'RioMareΤόνοςΣεΕλαιόλαδο160g2+1Δωρεάν', 'RioMareΤόνοςΣεΕλαιόλαδο80g3+1Δωρεάν','RioMareΤόνοςΣεΕλαιόλαδο80g3+1Δωρεάν']]

urls_driedfish = [["/psariou-1"],['ΚαμήλαΣαρδελάκιαΣεΝερό120g', 'TrataΡέγγαΚαπνιστή160g', 'FlokosΦιλέτοΣκουμπρίΚαπνιστόΣεΦυτικόΛάδι160g',
 'ΚαμήλαΑντζιούγες50g']]

urls_preservedmeat = [["/kreatos","/kreatos?page=2"],['KarlaCornedBeef340g','TulipPorkLuncheonMeat200g',
 'TulipChoppedHam200g','ZwanLuncheonMeat200g', 'ZwanChoppedHamAndPork200g','ZwanChickenLuncheonMeat200g']]

urls_preservedvegetable = [["/lachanikon"],['ΜεσόγειοςΡεβύθια400g', 'ΜεσόγειοςΦασόλιαΚόκκινα400g', 
'ΜεσόγειοςΦασόλιαΆσπρα400g', 'ΜεσόγειοςΣιταροπούλα340g', 'ΜεσόγειοςΜανιτάριαΦέτες400g', 'ΜεσόγειοςΦασόλιαΣεΣάλτσαΝτομάτας400g']]

urls_othermilk = [["/kremes-galaktos","/galaktos","/galaktos?page=2"],
['ΝουνούLight400g', 'Νουνού400g', 'NestleMilkmaidΓάλαΖαχαρούχο397g','ΝουνούΓάλαΖαχαρούχο397g','ΝουνούLight10X15g',
'ΧαραλαμπίδηςΚρίστηςΚρέμαΓάλακτος250ml']]

urls_otherfood = [["/soupes","/diafores-sokolates","/diafores-sokolates?page=2","/mpiskota","/mpiskota?page=2","/mpiskota?page=3","/mpiskota?page=4",
"/mpiskota?page=5","/mpiskota?page=6","/mpiskota?page=7","/mpiskota?page=8","/mpiskota?page=9","/mpiskota?page=10","/mpiskota?page=11","/mpiskota?page=12"],
['HeinzΣούπαΜανιταριών400g', 'HeinzΣούπαΝτομάτας400g',"ΦρουΦρουJoker9Τεμ9+3Δωρεάν","ΦρουΦρουMorningCoffee150g","KinderCards5Τεμ128g",
"Oreo154g","ΠαπαδοπούλουΓεμιστάΣοκολάτα200g"]]

urls_sugar = [["/aspri"],['SweetFamilyΛευκήΚρυσταλλικήΖάχαρη1kg']]

urls_flour= [["/alevri","/alevri?page=2"],['ΜιτσίδηΑλεύριΓιαΌλεςΤιςΧρήσεις1kg','ΜιτσίδηΑλεύριΦαρίνα&#039;&#039;00&#039;&#039;1kg',
 'ΜιτσίδηΑλεύριΧωριάτικο1kg','ΑδελφοίΚαζάζηΑλεύριΦαρίνα001kg','ΑδελφοίΚαζάζηΑλεύριΧωριάτικο1kg']]

urls_chocolate = [["/mavri-sokolata","/lefki-sokolata"],['BakandysΣοκολάταΓάλακτοςΚουβερτούρα4X37.5g', 
'BakandysΆσπρηΣοκολάταΚουβερτούρα4x37.5g']]

urls_confectionary= [["/diafora-alla-eidi", "/diafora-alla-eidi?page=2","/diafora-alla-eidi?page=3"],['ΜοναμίΜαγειρικήΣόδα10X7g', 
'RoyalBakingPowder226g', 'ΣτέλλαΑνθόνεροΚιτρόμηλο500ml', 'ΑμαλίαΝησιαστέ400g', 'CarltonaΆμυλοΑραβοσίτου450g', 'BakandysΣαβουαγιάρ200g', 
'ΓιώτηςΜαγιάΣτιγμής3x8g', 'SeranoΙνδοκάρυδοΑλεσμένο140g1+1Δωρεάν', 'SpryΦυτικόΜαγειρικόΠροιόν350g', 'ΑγρούΡοδόσταγμα500ml']]

urls_freshvegetables= [[ "/freska-lachanika","/freska-lachanika?page=2","/freska-lachanika?page=3","/freska-lachanika?page=4","/freska-lachanika?page=5","/freska-lachanika?page=6"],
['Ντομάτες1kg', 'ΑγγουράκιαΧωραφιού1kg', 'Λεμόνια1kg', 'ΚρεμμύδιαΑκαθάριστα1kg', 'Αγγουράκια1kg', 'ΝτοματίνιαΜίνιΦοινικωτά500g',
 'ΚαρόταΑκαθάριστα1kg', 'Αβοκάντο1kg', 'ΜαρούλιΡομάναΔέσμη1Τεμ', 'ΠιπεριέςΧρωματιστές4Τεμ', 'Σκόρδος1Τεμ', 'ΜπανάνεςΕισαγωγής1kg']]

urls_potatoes =[["/freska-lachanika"],['ΦρέσκεςΠατάτεςΚυπριακέςΝέαςΣoδειάς2kg']]

urls_fruit = [["/freska-frouta","/freska-frouta?page=2","/freska-frouta?page=3"],['ΜπανάνεςΕισαγωγής1kg','ΜήλαPinkLady1kg', 'ΠράσινοΣταφύλι750g', 'ΜήλαGrannySmith1kg', 'ΑχλάδιαConference1kg', 
'ΜήλαΚόκκιναDelicious1kg', 'Μύρτιλα125g', 'ΜήλαΚίτριναDelicious1kg', 'Ακτινίδια500g', 'ΠορτοκάλιαMerlinAAA1kg', 'ΜήλαRoyalGala1kg', 'ΠορτοκάλιαΓιαΧυμό2kg']]

urls_pork= [["/klasikes-kopes-choirinou","/klasikes-kopes-choirinou?page=2"],['ΧοιρινόΚιμάςΜερί500g', 'ΧοιρινόΜπριζόλαΛαιμός4Τεμ1,200kg', 'ΧοιρινόΣούβλαΛαιμόςΛαπάςΜεΚόκκαλο1,1kg']]

urls_othermeat= [["/paraskeuasmata-choirinou"],['ΧοιρινόΣεφταλιές850g', 'ΛουκάνικαΧωριάτικα550g']]

urls_poultry = [["/kotopoulo","/kotopoulo?page=2"],['ΚοτόπουλοΦιλέτο850g', 'ΚοτόπουλοΟλόκληρο2,8kg']]

urls_lamb = [["/arni"],['ΑρνίΓιαΣούβλα1kg']]

urls_beaf= [["/vodino"],['ΒοδινόΚιμάς500g']]

urls_fish= [["/psaria"],['ΤσιπούραΦρέσκιαΚαθαρισμένη3ΤεμMax1,500kg']]

urls_preservedmilk= [["/makras-diarkeias"],['MlekovitaΠλήρες3.5%ΓάλαΜακράςΔιαρκείας1L', 'LauraΕλαφρύΓάλαΜακράςΔιαρκείας1,5%1L']]

urls_lowfatmilk= [["/ageladino","/ageladino?page=2"],['ΛανίτηςΕλαφρύΓάλα2L', 'ΧαραλαμπίδηςΚρίστηςDelactΓάλα1L', 'ΧαραλαμπίδηςΚρίστηςΕλαφρύΓάλα2L', 'ΛανίτηςΕλαφρύΓάλα1,5L',
 'ΧαραλαμπίδηςΚρίστηςΕλαφρύΓάλα1L','ΧαραλαμπίδηςΚρίστηςΕλαφρύΓάλα1,5L']]

urls_wholemilk = [["/ageladino","/ageladino?page=2"],['ΛανίτηςΠλήρεςΓάλα2L','ΧαραλαμπίδηςΚρίστηςΠλήρεςΓάλα2L']]

urls_yogurt= [["/ageladino-giaourti", "/ageladino-giaourti?page=2","/proveio-giaourti"],['ΧαραλαμπίδηςΚρίστηςΣτραγγάτο1kg',
 'ZitaΣτραγγιστό1kg', 'ZitaΣτραγγιστόΆπαχο0%1kg', 'ΧαραλαμπίδηςΚρίστηςΣτραγγάτοΆπαχο0%1kg', 'ΑλάμπραΠρόβειοΓιαούρτιΗΓιαγιά700g']]

urls_butter= [["/voutyro"],['LurpakΑνάλατοΒούτυρο250g', 'KerrygoldΑλατισμένοΒούτυρο250g', 'LurpakΑλατισμένοΒούτυρο250g']]

urls_margarine= [["/margarines","/margarines?page=2"],['VitaliteLightΜαργαρίνη500g', 'ΧαραλαμπίδηςΚρίστηςOriginalΜαργαρίνη500g', 'ΧαραλαμπίδηςΚρίστηςLightΜαργαρίνη500g','FloraOriginal100%Φυτικό450g', 
'FloraLight100%Φυτικό450g', 'ΜινέρβαΦαστSoft250g']]

urls_eggs= [["/avga"],['VasilicoEggsΑυγάΜεσσαία15Τεμ']]

#put all the different lists in one
urls_all = [urls_bakery,urls_cereals,urls_pastas,urls_rice,urls_saltspices,urls_nuts,urls_jams,urls_crisps,urls_sauces,urls_oil,urls_otheroil,
urls_preservedfish,urls_driedfish,urls_preservedmeat,urls_preservedvegetable,urls_othermilk,urls_otherfood,urls_sugar,urls_flour,
urls_chocolate,urls_confectionary,urls_freshvegetables,urls_potatoes,urls_fruit,urls_pork,urls_othermeat,urls_poultry,urls_lamb,urls_beaf
,urls_fish,urls_preservedmilk,urls_lowfatmilk,urls_wholemilk,urls_yogurt,urls_butter,urls_margarine,urls_eggs]

#the class labels must represent the list category in urls_all, same length wiht the urls_all
class_labels = ['Bread','Other bakery products','Breakfast Cereals','Pasta products and couscous','Rice','Salt, spices and culinary herbs',
'Dried fruit and nuts','Jams, marmalades and honey','Crisps','Sauces, condiments','Olive Oil', 'Other edible oils','Other preserved or processed fish and seafood-based preparations',
'Dried, smoked or salted fish and seafood','Other meat preparations','Dried vegetables, other preserved or processed vegetables','Other milk products',
'Other food products n.e.c.','Sugar','Flours and other cereals','Chocolate','Confectionery products','Fresh or chilled vegetables other than potatoes and other tubers',
'Potatoes','Fresh or chilled fruit','Pork','Other meat','Poultry','Lamb and goat','Beef and veal','Fresh or chilled fish','Preserved milk','Low fat Milk',
'Whole Milk','Yogurt','Butter','Margarine and other vegetable fats','Eggs']

#the scrapper function
def scrapper_supermarketcy(urls:list,products:list):
    #create lists for the products and the prices repsectively
    products_ini =[]
    prices_ini = []

    #final list for the products and the prices, the text is cleaned up
    products_final =[]
    prices_final =[]

    #lists for the excel file, store only the necessary elements that can be found in the list given in the function
    price_excel = []
    product_excel = []

    #final lists for the not duplicated values
    global price_excelfinal
    global product_excelfinal
    price_excelfinal = []
    product_excelfinal = []

    #for the different urls, putting the prices and the description of the 
    # products in the two initial lists
    url_supermarket = "https://www.supermarketcy.com.cy"
    for url in urls:
        url_new = url_supermarket+url
        page = urlopen(url_new)
        html = page.read().decode("utf-8")
        bs = BeautifulSoup(html, "html.parser")
    
        scripts = bs.find_all('script',string=True)

        #get the strings for the names and the prices of the products using regular expressions
        for script in scripts:
            product= re.findall(r"'name':.*\'",str(script))
            price= re.findall(r"'price':.*\'",str(script))
            if len(product)> 0:
                products_ini.append(product)
                prices_ini.append(price)
            
    #get the description of the items, by removing the ':' and the additional quotation marks
    for j in range(len(products_ini)):
        for i in range(len(products_ini[j])):
            products_final.append(products_ini[j][i].split(':')[1].replace(" ","").strip('\''))
        
    #get the price of the items, by removing the ':' and the additional quotation marks
    for j in range(len(prices_ini)):
        for i in range(len(prices_ini[j])):
            prices_final.append(prices_ini[j][i].split(':')[1].replace(" ","").strip('\''))
        

    #check for the items if they belong in the list given in the function and store price/product in the new lists
    for item in products:
        for product in products_final:
            index = products_final.index(product)
            if item==product:
                price_excel.append(prices_final[index])
                product_excel.append(products_final[index])
                
    #round the prices to only two decimal points
    price_excel = [round(float(i),2) for i in price_excel]

    #check for duplicated values
    for item in product_excel:
        index = product_excel.index(item)
        if item not in product_excelfinal:
            price_excelfinal.append(price_excel[index])
            product_excelfinal.append(product_excel[index])

    # for products that can not be found in the website put a nan value by the price in the list
    for product in products:
        if product not in product_excelfinal:
            product_excelfinal.append(product)
            price_excelfinal.append("NaN")

#scrap all the websites and assign for each product the price,date, label class and retailer
all_items = []
for url,i,label in zip(urls_all,range(len(urls_all)),class_labels):
    scrapper_supermarketcy(url[0],url[1])
    for product,price in zip(product_excelfinal,price_excelfinal):
        all_items.append([product,price,datetime.now(),label,'SupermarketCy'])
###########################

###########################################
# Retrieving data from CSV
df = pd.read_csv("BillionPricesProject_ProductList.csv")



# SupermarketCy breads to scrape

data = {        "names": [
'Σίφουνας Μαύρο Μικρό Ψωμί Κομμένο 500g', 
'Σίφουνας Ολικής Ψωμί Κομμένο 780g',
'Σίφουνας Κοινό Ψωμί Κομμένο 560g', 
'Σίφουνας Κοινό Ψωμί Κομμένο 970g', 
'Σίφουνας Άσπρο Ψωμί 560g', #
'Σίφουνας Κοινό Ψωμί 970g', #
'3Α Απλή Ζωοτροφή Μίλλετ Κεχρί Κίτρινο 800g',
'Whiskas Adult Κλασσικά Επιλεγμένα Σε Σάλτσα 4X100g',
'Pedigree Με Μοσχάρι 400g',
'Κουτάλια Symphony 12Τεμ',
'Crown Αντικολλητικό Κατσαρολάκι Με Λαβή 18cm',
'Crown Αντικολλητικό Τηγάνι 30cm',
'Marob Μαχαίρια 12Τεμ',
'Crown Μπρίκι 9cm',
'Πιρουνάκια Στάχης 12Τεμ',
'Klemex Σακούλες Μπλέ Με Κορδόνι 75X80 59L 20Τεμ',
'Lordos Σακούλες Ανακύκλωσης Πλαστικό 75X80 20Τεμ',
'Lordos Σακούλες Ανακύκλωσης Χαρτί 60X73 20Τεμ',
'Klemex Μεγάλα Σακούλια Για Τρόφιμα 100Τεμ',
'Scotch Brite Πράσινο Σφουγγάρι Κουζίνας 2+1 Δώρο',
'Vileda Σφουγγάρι Για Μπάνιο 1Τεμ',
'Sanitas Ανοξείδωτο Σύρμα 2Τεμ',
'Wettex Σπογγοπετσέτα 26cmx20cm',
'Vileda Ξεσκονόπανα Γενικού Καθαρισμού 3Τεμ',
'Sanitas Πανάκια Στεγνού Καθαρισμού Για Δάπεδα 20Τεμ',
'Stadio Σκούπα 1Τεμ',
'Vileda Σκούπα Standard 1Τεμ',
'Pola Σκούπα 1Τεμ',
'Vileda Φαράσι Σκουπίσματος Και Σκουπάκι 1Τεμ',
'Vileda Σφουγγαρίστρα Standard 1Τεμ',
'Myreon Σφουγγαρίστρα Yellow Strips 1Τεμ',
'Scotch Brite Σφουγγαρίστρα Clik Clak 1Τεμ',
'Vileda Universal Κοντάρι 1Τεμ',
'Swipe Κοντάρι Ασημί 1Τεμ',
'Myreon Aluminium Κοντάρι 1Τεμ',
'Κουβάς Σφουγγαρίσματος Μπλέ 15L 1Τεμ',
'Dettol 500ml',
'Cif Classic Κρέμα Γενικού Καθαρισμού 750ml',
'Roklin Spray Antibacterial Πολυκαθαριστικό 750ml -1€',
'Klinex Χλωρίνη Spray Πολλαπλών Χρήσεων 750ml',
'Ajax Σπρέι Πολυκαθαριστικό 4 Σε 1 500ml',
'Dixan Deep Clean Σκόνη 70 Πλύσεις 3,85kg', #
'Εύρηκα Active Care Σκόνη Τριαντάφυλλο & Γιασεμί 61 Πλύσεις 4kg -5€', #
'Dixan Σκόνη 46 Πλύσεις 2,53kg',
'Ariel Aqua Poudre Alpine Σκόνη 50 Πλύσεις 3.250k',
'Εύρηκα Μασσαλίας Classic Υγρό 48 Πλύσεις 2,4L -4€', #
'Ariel Power Mountain Spring Υγρό 56 Πλύσεις 3,080L', #
'Dixan Deep Clean Υγρό Multicolor 42 Πλύσεις 2,1L', #
'Comfort Pure Μαλακτικό Ρούχων 2L',
'Secrets Λεβάντα & Ylang Ylang Μαλακτικό Ρούχων 2L -1€',
'Soupline Complete Care So Fresh Συμπυκνωμένο Μαλακτικό 1,2L',
'Lenor La Collection Love Συμπυκνωμένο Μαλακτικό 60 Πλύσεις 1.38L',
'Fairy Ultra Original Υγρό Πιάτων 900ml',
'Palmolive Delicious Orchid Υγρό Πιάτων 500ml',
'Εύρηκα Υγρό Πιάτων Λεμόνι 750ml',
'Ajax Excel Υγρό Πιάτων Λεμόνι 750ml -0,50€',
'Νουνού Φαρίν Λακτέ 300g -0.40€', #
'Humana 5 Δημητριακα Με Μπανάνα Χωρίς Προσθήκη Ζάχαρης 200g',
'Neutro Roberts Deodorant Powder Fresh Roll On 50ml',
'Nivea Men Deodorant Fresh Dry Spray 150ml',
'Pom Pon Μαντηλάκια Ντεμακιγιάζ Με Υαλουρονικό Οξύ Για Όλους Τους Τύπους Δέρματος 20Τεμ 1+1',
'Garnier Skin Active Moisture Bomb Tissue Mask 1Τεμ 28g',
'Nivea Sun Protect & Moisture Sun Lotion 50Spf 200ml',
'Johnsons Μπατονέτες 200Τεμ',
'Rex Βαμβάκι 200g',
'Tippys Δίσκοι Ντεμακιγιάζ 80Τεμ',
'Greco Drug Οινόπνευμα 96% 350ml',
'Alokozay Ιατρικές Μάσκες Προσώπου 10Τεμ',
'Aspro Clear 18Τεμ',
'Hansaplast Universal Διάφορα Μεγέθη 40Τεμ',
'Palmolive Silky Shine Effect Σαμπουάν Με Αλόε Βέρα 350ml',
'Wellaflex Hairspray Έχτρα Δυνατό Κράτημα 250ml',
'Dermomed Argan Oil Κρεμοσάπουνο 1000ml',
'Palmolive Naturals Σαπουνάκια Χαμομήλι 125g 4+2 Δώρο',
'Dermomed Αλόε Βέρα Κρεμοσάπουνο 1000ml',
'Colgate Max White Crystal Mint 75ml 1+1 Δώρο',
'Colgate Οδοντόβουρτσα Extra Clean Medium 1+1Δωρεάν',
'Listerine Cool Mint Mild Taste 500ml 1+1',
'Colgate Total Pro Gum Health Οδοντικό Νήμα 50m',
'Gillette Blue Ii Plus Slalom Ξυραφάκια 10Τεμ',
'Gillette Αφρός Regular 200ml',
'Nivea Men Fresh Kick After Shave Balm 100ml',
'Always Ultra Secure Night 12Τεμ', #
'Kopparberg Strawberry & Lime Cider 500ml',
'Somersby Apple Cider 330ml',
'Κεο Vsop Brandy 1L',
'Gordons Dry Gin 700ml',
'Baileys Original Liqueur 700ml',
'Aperol Aperitivo 1L',
'Bacardi Superior Rum 700ml',
'Κεο 8X330ml',
'Carlsberg 8X330ml',
'Κεο Λευκό Ξηρό Κρασί 1L',
'Mateus Rose Κρασί 750ml',
'Κεο Ερυθρό Ξηρό Κρασί 1L',
'Nescafe Classic 200g', #
'Nescafe Classic 100g', #
'Jacobs Gold Επιλεγμένο Χαρμάνι 100g',
'Jacobs Εκλεκτός 100g', #
'Celest Cafe Classic 200g', #
'Nescafe Azera Espresso 100g', #
'Douwe Egberts Καφές Espresso Brazil 95g',
'Λαϊκού Κυπριακός Καφές Χρυσός 200g', #
'Χαραλάμπους Κυπριακός Καφές 200g', #
'Λαϊκού Κυπριακός Καφές Χρυσός 500g', #
'Χαραλάμπους Κυπριακός Καφές 500g', #
'Lipton Yellow Label Τσάι 20Τεμ',
'Ahmad Tea Πράσινο Τσάι 25Τεμ',
'Natural Life Τσάι Χαμομήλι 20Τεμ',
'Ahmad Tea Αγγλικό Πρόγευμα 20Τεμ',
'Cadbury Ρόφημα Σοκολάτας 500g',
'Cadbury Κακάο 125g','Άγιος Νικόλαος 6X1,5L',
'Αγρός 12X500ml', #
'Αγρός 6X1,5L', #
'Άγιος Νικόλαος 12X500ml', #
'Κύκκος 12Χ500ml', #
'Κύκκος 6Χ1,5L', #
'Kean Χυμός Πορτοκάλι 1L', #
'Λανίτης Χυμός Πορτοκάλι 1L',
'Κεανίτα Χυμός Πορτοκάλι 9X250ml', #
'Κεο Χυμός Πορτοκάλι 1L','Ένα Χυμός Πορτοκάλι 1L',
'Kean Χυμός Μήλο 9X250ml',
'Kean Χυμός Μήλο 1L',
'Λανίτης Χυμός Μήλο 1L',
'Κεο Χυμός Μήλο 1L',
'Pfanner Φρουτοποτό Πράσινο Μήλο 1L',
'Pfanner Χυμός Μήλο 1L',
'Kean Χυμός 5 Φρούτα 1L',
'Kean Χυμός Πορτοκάλι Μήλο & Καρότο 1L', #
'Kean Χυμός Ντομάτας 1L',
'Κεο Χυμός Τομάτα 1L',
'Coca Cola 8X330ml', #
'Sprite 6X330ml',
'Schweppes Pink Grapefruit 6X330ml',
'Fanta 6X330ml',
'Pepsi Max 8X330ml', #
'7Up 8X330ml', #
'Schweppes Lemonade 6X330ml',
'Regis Παγωτό Agrino Χωνάκια Βανίλια Σοκολάτα 4Χ135ml',
'Παπαφιλίπου N-ice Παγάκια 4,5kg',
'Παπαφιλίπου N-ice Παγάκια 2,7kg',
'Παπαφιλίπου N-ice Παγάκια 1,5kg',
'7Seas Φασόλια Ξεκούνια Άσπρα 900g',
'7Seas Ανάμικτα Μπρόκολο Καρότο Κουνουπίδι 900g',
'7Seas Μπιζέλι 900g',
'7Seas Ανάμικτα Μπιζέλι Καρότο Αγκινάρες 900g',
'7Seas Χρωματιστές Πιπεριές 900g',
'Findus Σολωμός Φιλέτο 500g',
'Foodpax Φιλέτο Μπαρμπούνι Ειρηνικού 400g',
'Blue Green Wave Μπακαλιάρος Φιλέτο 800g',
'7Seas Μαρίδα 950g',
'7Seas Γόππα 900g',
'Blue Green Wave Χταπόδια Ολόκληρα Καθαρισμένα 1kg', #
'Foodpax Μικρό Χταπόδι Ινδοειρηνικού Καθαρισμένο 400g',
'Redda Θράψαλα Ειρηνικού Ροδέλες 1kg',
'Blue Green Wave Καλαμάρι Ροδέλες 1kg', #
'Edesma Καβουρόψιχα 250g',
'Birds Eye Breaded Cod Large Fillets 4Τεμ', #
'Nordsea Τραγανιστά Φιλέτα Ψαριού 4Τεμ 300g', #
'Regina Μακαρόνια Παστίτσιο 425g',
'Regina Μουσακάς 425g',
'Regina Κανελόνια 400g',
'Edesma Μπουκιές Κοτόπουλο 900g', #
'Γρηγορίου Μπιφτέκια Γαλοπούλας 6Τεμ 480g', #
'Γρηγορίου Μπιφτέκια Βοδινά 4Τεμ 600g', #
'Μιτσίδη Ραβιόλες 375g', #
'Regina Πίτσα Πεπερόνι 1Τεμ 300g',
'Buitoni Piccolinis Prosciutto 9x30g',
'Regina Πίτσα Σπέσιαλ 1Τεμ 330g',
'Regina Πίτσα Τυρί & Ντομάτα 1Τεμ 300g',
'Aviko Pommes Frites Πατάτες 1kg',
'Χαραλαμπίδης Κρίστης Ραβιόλες Με Πισσουρκώτικο Χαλλούμι 400g', #
'Hercules Ραβιόλες Με Χαλλούμι & Αναρή 400g', #
'Redda Γαρίδες Vannamei Αποφλοιωμένες Προβρασμένες 500g', #
'Royal Blue Σολομός Φιλέτο Μερίδες 500g', #
'7Seas Κοκκινόψαρο Ακέφαλο 900g', #
'Σολωμός Φρέσκος 2Τεμ Max 600g', #
'Blue Green Wave Μπακαλιάρος Φιλέτο 800g', #
'7Seas Ψάρι Φιλέτο Με Καπήρα 400g', #
'Nordsea Fish Sticks 10Τεμ 300g', #
'Edesma Μπουκιές Κοτόπουλου 24Τεμ 500g', #
'Bgw Σνίτσελ Κοτόπουλου 400g', #
'Κιτρομηλίδη Σπιτο Γεύματα Κεφτέδες 500g', #
'7Seas Κοτομπουκιές Πανέ 900g', #
'Nescafe Classic Decaf 100g', #
'Nescafe Gold Blend Roastery Collection Dark Roast 95g', #
'7Up Diet 8X330ml', #
'Coca Cola Zero 8X330ml', #
'Άγιος Νικόλαος 6X1,5L', #
'Kean Χυμός Μάνγκο Ρόδι 1L', #
'Σίφουνας Ψωμί Φέτες Τόστ Άσπρο Μεγάλο 925g', #
'Σίφουνας Ψωμί Φέτες Τόστ Άσπρο Μικρό 700g', #
'Σίφουνας Ψωμί Φέτες Τόστ Μαύρο Πιτυρούχο Μεγάλο 700g', #
'Σίφουνας Ψωμί Φέτες Τόστ Πολύσπορο Μικρό 1Τεμ', #
'Etosha Κάρβουνα 5kg', #
'Πυρσός Κάρβουνα 5kg', #
'Εύρηκα Μασσαλίας Ylang Ylang & Λεβάντα Υγρό 48 Πλύσεις 2,4L -4€', #
'Comfort Gold Lilies & Wild Berries Μαλακτικό Ρούχων 4L', #
'Comfort Gold Wild Orchid & Sandalwood Μαλακτικό Ρούχων 4L', #
'Comfort Pure Μαλακτικό Ρούχων 4L', #
'Always Ultra Long Με Φτερά 16Τεμ', #
'Always Dailies Normal To Go 20Τεμ', #
'Every Day Hyperdry Normal Ultra Plus 18Τεμ 1+1', #
'Elite Χαρτοπετσέτες Πολυτελείας Άσπρο 3Φύλλα 40X40cm 25Τεμ', #
'Kleenex Scottonelle Pure Clean Double Roll Χαρτί Τουαλέτας 16Τεμ -2€', #
'Elda Χαρτί Τουαλέτας 24Τεμ', #
'Nannys Sensitive 5 Junior 44Τεμ', #
'Nannys Sensitive 6 Junior Plus 40Τεμ', #
'Nannys Sensitive 3 Midi 56Τεμ', #
'Pampers Active Baby 7 40Τεμ', #
'Pampers Premium Care 1 52Τεμ', #
'Hipp Organic Baby Cereal 100% Ρυζάλευρο 200g', #
'Nestle Φαρίν Λακτέ Με Γάλα 300g', #
'Νουνού Φρουτόκρεμα 5 Φρούτα & Γάλα 300g -0.50€', #
'Νουνού Φαρίν Λακτέ Μπισκότο 300g -0.40€', #
'Γιώτης Φαρίν Λακτέ 300g -0,50€', #
'Νουνού Frisogrow 3 800g', #
'Νουνού Frisogrow Plus+ 4 800g', #
'Nan Optipro HM- 0 4 400g', #
'S 26 Progress Gold 3 400g', #
'Edesma Μπιφτέκια Λαχανικών 4Τεμ', #
'Γρηγορίου Μπιφτέκια 6Τεμ 480g', #
'Kyprianou Μπιφτέκια Κοτόπουλου 6Τεμ 700g' #
],
                "product_subclass": [u'bread', u'bread',u'bread',u'bread',u'bread',u'bread',u'Products for Pets',u'Products for Pets',u'Products for Pets',u'Non-electric kitchen utensils and articles',u'Non-electric kitchen utensils and articles',u'Non-electric kitchen utensils and articles',u'Cutlery, flatware and silverware',u'Cutlery, flatware and silverware',u'Cutlery, flatware and silverware',u'Cleaning equipment',u'Cleaning equipment',u'Cleaning equipment',u'Cleaning equipment',u'Cleaning equipment',u'Cleaning equipment',u'Cleaning equipment',u'Cleaning equipment',u'Cleaning equipment',u'Cleaning equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning Equipment',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Baby food',u'Baby food',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products', u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Pharmaceutical products',u'Pharmaceutical products',u'Pharmaceutical products',u'Pharmaceutical products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Personal grooming treatments',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Non-electrical appliances',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Non-electrical appliances',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Spirits and liqueurs',u'Spirits and liqueurs',u'Spirits and liqueurs',u'Spirits and liqueurs',u'Spirits and liqueurs',u'Spirits and liqueurs',u'Spirits and liqueurs',u'Lager beer',u'Lager beer',u'Wine from grapes',u'Wine from grapes',u'Wine from grapes',u'Coffee',u'Coffee',u'Coffee',u'Coffee',u'Coffee',u'Coffee',u'Coffee',u'Coffee',u'Coffee',u'Coffee',u'Coffee',u'Tea',u'Tea',u'Tea',u'Tea',u'Cocoa and powdered chocolate',u'Cocoa and powdered chocolate',u'Mineral or spring waters',u'Mineral or spring waters',u'Mineral or spring waters',u'Mineral or spring waters',u'Mineral or spring waters',u'Mineral or spring waters',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Fruit and vegetable juices',u'Soft drinks',u'Soft drinks',u'Soft drinks',u'Soft drinks',u'Soft drinks',u'Soft drinks',u'Soft drinks',u'Edible ices and ice cream',u'Edible ices and ice cream',u'Edible ices and ice cream',u'Edible ices and ice cream',u'Frozen vegetables other than potatoes and other tubers',u'Frozen vegetables other than potatoes and other tubers',u'Frozen vegetables other than potatoes and other tubers',u'Frozen vegetables other than potatoes and other tubers',u'Frozen vegetables other than potatoes and other tubers',u'Frozen fish',u'Frozen fish',u'Frozen fish',u'Frozen Fish',u'Frozen Fish',u'Frozen seafood',u'Frozen Seafood',u'Frozen Seafood',u'Frozen Seafood',u'Frozen Seafood',u'Frozen seafood',u'Frozen Seafood',u'Ready-made meals',u'Ready-made meals',u'Ready-made meals',u'Other meat preparations',u'Other meat preparations',u'Other meat preparations',u'Pasta products and couscous',u'Pizza and quiche',u'Pizza and quiche',u'Pizza and quiche',u'Pizza and quiche',u'Crisps',u'Pasta products and couscous',u'Pasta products and couscous',u'Frozen Seafood',u'Frozen Fish',u'Frozen Fish',u'Frozen Fish',u'Frozen Fish',u'Frozen Seafood',u'Frozen Seafood',u'Other meat preparations',u'Other meat preparations',u'Other meat preparations',u'Other meat preparations',u'Coffee',u'Coffee',u'Soft drinks',u'Soft drinks',u'Mineral or spring waters',u'Fruit and vegetable juices',u'bread',u'bread',u'bread',u'bread',u'Other Products',u'Other Products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Cleaning and maintenance products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Articles for personal hygiene and wellness, esoteric products and beauty products',u'Baby Care',u'Baby Care',u'Baby Care',u'Baby Care',u'Baby Care',u'Baby food',u'Baby food',u'Baby food',u'Baby food',u'Baby food',u'Baby food',u'Baby food',u'Baby food',u'Baby food',u'Ready-made meals',u'Other meat preparations',u'Other meat preparations'],
                # "product_class" : [u'food',u'food',u'food',u'food',u'food',u'food',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'home',u'food',u'food',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'drinks',u'food',u'food',u'food',u'food',u'other',u'other',u'home',u'home',u'home',u'home',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'personal care',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food',u'food'],
                "webpage": [u'psomi',u'psomi',u'psomi',u'psomi',u'psomi',u'psomi',u'frontida-katoikidion',u'frontida-katoikidion',u'frontida-katoikidion',u'oikiaka-skevi',u'oikiaka-skevi',u'oikiaka-skevi',u'oikiaka-skevi',u'oikiaka-skevi',u'oikiaka-skevi',u'sakoules',u'sakoules',u'sakoules',u'sakoules',u'sfouggaria-spoggopetsetes-kouz',u'sfouggaria-spoggopetsetes-kouz',u'sfouggaria-spoggopetsetes-kouz',u'sfouggaria-spoggopetsetes-kouz',u'sfouggaria-spoggopetsetes-kouz',u'sfouggaria-spoggopetsetes-kouz',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'skoupes-sfouggaristres',u'frontida-spitiou',u'frontida-spitiou',u'frontida-spitiou',u'frontida-spitiou',u'frontida-spitiou',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'frontida-rouchon',u'katharistika-piaton',u'katharistika-piaton',u'katharistika-piaton',u'vrefikes-kremes',u'vrefikes-kremes',u'aposmitika',u'aposmitika',u'kallyntika',u'kallyntika',u'kallyntika',u'alla-eidi',u'alla-eidi',u'alla-eidi',u'farmakeio',u'farmakeio',u'farmakeio',u'farmakeio',u'sampouan',u'peripoiisi-mallion',u'kremosapouna',u'sapounia',u'kremosapouna',u'odontokremes',u'odontovourtses',u'dialymata',u'diafora-eidi-stomatikis-ygieinis',u'xyrafakia',u'afroi-xyrismatos-after-shave',u'afroi-xyrismatos-after-shave',u'servietes-panes-akrateias',u'diafora-alkooloucha',u'diafora-alkooloucha',u'diafora-alkooloucha',u'diafora-alkooloucha',u'diafora-alkooloucha',u'diafora-alkooloucha',u'diafora-alkooloucha',u'mpyres',u'mpyres',u'krasia',u'krasia',u'krasia',u'kafes',u'kafes',u'kafes',u'kafes',u'kafes',u'kafes',u'kafes',u'kafes',u'kafes',u'kafes',u'kafes',u'mavro-tsai',u'prasino-tsai',u'afepsimata',u'tsai-diafora',u'sokolata-kakao',u'sokolata-kakao',u'nero',u'nero',u'nero',u'nero',u'nero',u'nero',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'chymoi',u'anapsyktika',u'anapsyktika',u'anapsyktika',u'anapsyktika',u'anapsyktika',u'anapsyktika',u'anapsyktika',u'pagota',u'pagakia',u'pagakia',u'pagakia',u'ospria-1',u'lachanika',u'lachanika-frouta',u'lachanika-frouta',u'lachanika-frouta',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'apo-thalassina',u'apo-thalassina',u'etoima-gevmata',u'etoima-gevmata',u'etoima-gevmata',u'etoima-gevmata',u'mpiftekia',u'mpiftekia',u'zymarika-1',u'pitses',u'pitses',u'pitses',u'pitses',u'klasikes',u'zymarika-1',u'zymarika-1',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'eidi-ichthyopoleiou',u'psaria',u'eidi-ichthyopoleiou',u'apo-thalassina',u'apo-thalassina',u'apo-kreatika',u'apo-kreatika',u'etoima-gevmata',u'apo-kreatika',u'kafes',u'kafes',u'anapsyktika',u'anapsyktika',u'nero',u'chymoi',u'tost',u'tost',u'tost',u'tost',u'eidi-psistarias',u'eidi-psistarias',u'ygra-plyntiriou',u'malaktika-1',u'malaktika-1',u'malaktika-1',u'servietes-panes-akrateias',u'servietes-panes-akrateias',u'servietes-panes-akrateias',u'chartopetsetes',u'charti-toualetas',u'charti-toualetas',u'panes',u'panes',u'panes',u'panes',u'panes',u'vrefikes-kremes',u'vrefikes-kremes',u'vrefikes-kremes',u'vrefikes-kremes',u'vrefikes-kremes',u'vrefiko-gala',u'vrefiko-gala',u'vrefiko-gala',u'vrefiko-gala',u'apo-lachanika',u'mpiftekia',u'mpiftekia']
                 }

#print(str(len(data['names']))+' '+str(len(data['product_subclass']))+' '+str(len(data['product_class']))+' '+str(len(data['webpage'])))
supermarketCy=pd.DataFrame(data)
# for i in range(len(data['names'])):
#     print(str(data['names'][i])+'|'+str(data['product_subclass'][i]))
for i in range(len(data['names'])):
    bread=supermarketCy_bread(supermarketCy.loc[i])
    if(bread==None):
        next
    else:
        df.loc[len(df)] = bread
#print(df)

for i in range(len(all_items)):
    df.loc[len(df)] = (all_items[i][0],all_items[i][1],all_items[i][2],all_items[i][3],all_items[i][4],0)

#df.append(df_bakery)



df.to_csv("BillionPricesProject_ProductList.csv", index=False)



