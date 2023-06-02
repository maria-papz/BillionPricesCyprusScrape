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
import urllib.request
import json
import PyPDF2
from lxml import etree
from tabula import read_pdf


#read from csv not to lose past records
df = pd.read_csv("BillionPricesProject_ProductList.csv")

# XPath for supermarketCy has a repeating pattern (may have the same pattern for other categories of the website as well)
# We create a function so that there is no need to find the XPath for every bread added
# Accepts name of bread and page the bread is found
# Returns scraped data



def supermarketCy(item):
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

def SupermarketCyScrape():
    scy_data = pd.read_csv("SupermarketCy.csv")
    for index, row in scy_data.iterrows():
        scrape=supermarketCy(row)
        if(scrape==None):
            next
        else:
            df.loc[len(df)] = scrape


#put all the endings of the urls in lists based on the class they belong along
# with the descriptions of the products that should be scrapped
urls_bread = [['/psomi','/psomi?page=2','/psomi?page=3'],['ΣίφουναςΟλικήςΨωμίΚομμένο780g', 'ΣίφουναςΜαύροΜικρόΨωμίΚομμένο500g', 'ΣίφουναςΚοινόΨωμίΚομμένο560g', 
'ΣίφουναςΚοινόΨωμίΚομμένο970g', 'ΣίφουναςΆσπροΨωμί560g', 'ΣίφουναςΚοινόΨωμί970g']]

urls_bakery=[["/pites","/tost","/psomakia","/almyra","/keik","/glyka-1","/glyka-1?page=2","/krakers","/krakers?page=2","/kritsinia","/kritsinia?page=2",
"/kroutons","/fryganies","/paximadia","/paximadia?page=2","/paximadia?page=3","/paximadia?page=4","/koulourakia"],
['ΣίφουναςΠίττεςΆσπρεςΜεγάλες5Τεμ550g', 'ΣίφουναςΨωμίΦέτεςΤόστΆσπροΜικρό700g', 'ΣίφουναςΦραντζολάκιαΣτρογγυλά4Τεμ', 'ΣίφουναςΦραντζολάκιαΜακρόστεναΜεγάλα4Τεμ', 
'ΣίφουναςΚρουασάνΒουτύρου1Τεμ', 'ΣίφουναςΛουκανικόπιτα1Τεμ', 'ΣίφουναςΠίταΣάτζιηςΜεΜέλι1Τεμ', 'ΣίφουναςΕλιόπιταΣφολιάτα1Τεμ', 'ΣίφουναςΚέικΓεωγραφίας750g', 'ΣίφουναςMixΣιροπιαστά410g',
"7DaysMiniBakeRollsΠίτσα80g","BakandysΧωριάτικαΚριτσίνιαΣιταρένια275g","ΜαρίαςΠαξιμάδιαΓλυκανίσου300g","JohnsofΚρουτόνιαΟλικήςΆλεσης320g",
"EliteΦρυγανιέςΜεΣίκαλη360g3+1Δώρο","EliteΦρυγανιέςΟλικήςΆλεσης360g3+1Δώρο","BakandysΠαξιμάδιαΣικάλεως250g","JohnsofNapolitanoΣταφίδαςΑμυγδάλου240g"]]

urls_cereals=[["/dimitriaka?page=1","/dimitriaka?page=2","/dimitriaka?page=3","/dimitriaka?page=4","/dimitriaka?page=5","/dimitriaka?page=6","/dimitriaka?page=7","/dimitriaka?page=8","/dimitriaka?page=9"],
['QuakerΝιφάδεςΒρώμης500g', 'QuakerΤραγανέςΜπουκιέςΒρώμηΣοκολάτα450g','OreoO&#039;sCereal350g','KelloggsCornFlakes375g', 'KelloggsCocoPopsChocos375g',
 'KelloggsCocoPops500g', 'KelloggsSpecialK500g','KelloggsMielPopsLoops330g']]

urls_pastas=[["/makaronia","/makaronia?page=2","/makaronia?page=3","/makaronia?page=4","/penes","/penes?page=2",
"/kritharaki"],['BarillaΣπαγγέτιNo5500g', 'ΜέλισσαPrimoGustoΣπαγγέτιNo6500g', 'ΜέλισσαPrimoGustoΚριθαράκι500g',
'ΜιτσίδηΣπαγέττι500g','ΜιτσίδηΚριθαράκι500g','ΜιτσίδηΜακαρόνιαΑ500g','ΜιτσίδηΧωριάτικαΜακαρόνια500g','ΘίιαμβοςΣπαγέττο500g']]

urls_rice = [["/parmpoil", "/parmpoil?page=2","/mpasmati","/karolina","/glase","/pourgouri","/diafora-ryzia"],
['3ΑΡύζιΠάρποιλτ1kg', 'BensOriginalΡύζιΜακρύκοκκο10Λεπτά1kg', 'TildaΡυζιΜπασματι1kg', '3ΑΡύζιΜπασμάτι1kg',
 '3ΑΡύζιJasmine1kg', 'ΑφοίΑ.ΚεπόλαΠουργούρι1kg','ΑφοίΑ.ΚεπόλαΠουργούρι500g', 'ΜιτσίδηΠουργούρι500g', 'ΜιτσίδηΠουργούρι1kg',
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

urls_sauces=[["/ntomatas","/ntomatas?page=2","/ntomatas?page=3","/zomoi","/zomoi?page=2","/zomoi?page=3"],['PelargosΚλασικό3X250g', 
'ΜιτσίδηΠάσταΝτομάτας4X70g', 'BlossomΠάσταΝτομάτας4X70g', 'KeanPomiloriΠεραστήΝτομάτα690g', 'SwsΠάσταΝτομάτας425g','ΜιτσίδηΠεραστήΝτομάτα3x500g', 
'MaggiΖωμόςΚότας12Τεμ','MaggiΖωμόςΛαχανικών16Τεμ','MaggiΖωμόςΓιαΖυμαρικά12Τεμ','KnorrΖωμόςΚότας12Τεμ','KnorrΖωμόςΛαχανικών12Τεμ']]

urls_oil=[["/elaiolado","/elaiolado?page=2"],['ΆγιοςΓεώργιοςΚυπριακόΠαρθένοΕλαιόλαδο1L','ΕλιοχώριΠαρθένοΕλαιόλαδο2L', 'ΣεκέπΠαρθένοΕλαιόλαδο1L']]

urls_otheroil=[["/ilianthelaio"],['LesieurΗλιανθέλαιο3L', 'AmbrosiaΗλιανθέλαιο3L','FloraΗλιανθέλαιο3L', 'AmbrosiaΗλιανθέλαιο4L']]

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
 'ΜιτσίδηΑλεύριΧωριάτικο1kg','ΜιτσίδηΑλεύριΦαρίναΖαχαροπλαστικής1kg','ΑδελφοίΚαζάζηΑλεύριΦαρίνα001kg','ΑδελφοίΚαζάζηΑλεύριΧωριάτικο1kg']]

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

urls_lowfatmilk= [["/ageladino","/ageladino?page=2"],['ΛανίτηςΕλαφρύΓάλα2L',  'ΛανίτηςΕλαφρύΓάλα1,5L','ΧαραλαμπίδηςΚρίστηςDelactΓάλα1L', 'ΧαραλαμπίδηςΚρίστηςΕλαφρύΓάλα2L',
 'ΧαραλαμπίδηςΚρίστηςΕλαφρύΓάλα1L','ΧαραλαμπίδηςΚρίστηςΕλαφρύΓάλα1,5L']]

urls_wholemilk = [["/ageladino","/ageladino?page=2"],['ΛανίτηςΠλήρεςΓάλα2L','ΧαραλαμπίδηςΚρίστηςΠλήρεςΓάλα2L']]

urls_yogurt= [["/ageladino-giaourti", "/ageladino-giaourti?page=2","/proveio-giaourti"],['ΧαραλαμπίδηςΚρίστηςΣτραγγάτο1kg',
 'ZitaΣτραγγιστό1kg', 'ZitaΣτραγγιστόΆπαχο0%1kg', 'ΧαραλαμπίδηςΚρίστηςΣτραγγάτοΆπαχο0%1kg', 'ΑλάμπραΠρόβειοΓιαούρτιΗΓιαγιά700g']]

urls_butter= [["/voutyro"],['LurpakΑνάλατοΒούτυρο250g', 'KerrygoldΑλατισμένοΒούτυρο250g', 'LurpakΑλατισμένοΒούτυρο250g']]

urls_margarine= [["/margarines","/margarines?page=2"],['VitaliteLightΜαργαρίνη500g', 'ΧαραλαμπίδηςΚρίστηςOriginalΜαργαρίνη500g', 'ΧαραλαμπίδηςΚρίστηςLightΜαργαρίνη500g','FloraOriginal100%Φυτικό450g', 
'FloraLight100%Φυτικό450g', 'ΜινέρβαΦαστSoft250g']]

urls_eggs= [["/avga"],['VasilicoEggsΑυγάΜεσσαία15Τεμ']]

#put all the different lists in one
urls_all = [urls_bread,urls_bakery,urls_cereals,urls_pastas,urls_rice,urls_saltspices,urls_nuts,urls_jams,urls_crisps,urls_sauces,urls_oil,urls_otheroil,
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

    #mean value of the prices of the products
    global mean_price
    mean_price = 0

    #for the different urls, putting the prices and the description of the 
    # products in the two initial lists
    url_supermarket = "https://www.supermarketcy.com.cy"
    for url in urls:
        try:
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
        except urllib.error.HTTPError as e:
            print(f"HTTP error: {e.code}")
            continue

            
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

    #calculate the mean value of the products
    if len(price_excelfinal)>0:
        mean_price = round(sum(price_excelfinal)/len(price_excelfinal),2)
    else:
        mean_price = 0

    # for products that can not be found in the website put a nan value by the price in the list
    for product in products:
        if product not in product_excelfinal:
            product_excelfinal.append(product)
            price_excelfinal.append("NaN")  
    
#scrap all the websites and assign for each product the price,date, label class and retailer
all_items_supermarketcy = []
for url,i,label in zip(urls_all,range(len(urls_all)),class_labels):
    scrapper_supermarketcy(url[0],url[1])
    for product,price in zip(product_excelfinal,price_excelfinal):
        all_items_supermarketcy.append([product,price,datetime.now(),label,'SupermarketCy',mean_price])
            

#initialize a dataframe
df_supermarketcy=pd.DataFrame(columns=('item.name','item.price','date.time','item.subclass','retailer','average price'))

#assign the values to each column
for i in range(len(all_items_supermarketcy)):
    df.loc[len(df)] = (all_items_supermarketcy[i][0],all_items_supermarketcy[i][1],all_items_supermarketcy[i][2],all_items_supermarketcy[i][3],all_items_supermarketcy[i][4],0)



def AlphaMega():
    data_alphaMega = pd.read_csv("AlphaMega.csv")
    for index, am in data_alphaMega.iterrows():
        page = requests.get(am['website'].strip())
        st=page.content.decode('utf-8')
        tree = html.fromstring(st)
        product_name = (''.join(am['product_name'])).replace(' ','').strip() 
        product_price=tree.xpath("//div[@class='grid grid--align-content-start']/script[@type='application/ld+json']/text()")[0]
        product_price = json.loads(product_price)['offers']['price']
        now = datetime.now()
        date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
        product_subclass=am['product_subclass']
        retailer= am['retailer']
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


SupermarketCyScrape()



urls_phone1 = [['https://www.cyta.com.cy/upgraded-telephony/el'],['Κλήσειςπροςσταθερό']]
urls_phone2 = [['https://www.cyta.com.cy/upgraded-telephony/el'],['Κλήσειςπροςκινητό']]
urls_internet = [['https://www.cyta.com.cy/mobile-internet'],['MobileInternetHome1']]
urls_freedom = [['https://www.cyta.com.cy/freedom-plans'],['FREEDOM']]

urls_all_phones = [ urls_phone1,urls_phone2,urls_internet,urls_freedom]

class_labels_phones = ['Wired telephone services','Wireless telephone services','Internet access provision services','Bundled telecommunication services']

#scrapper functions for phone services
def scrappe_page(url,str_inurl,regex_exp):
    global prices_phoneservices
    prices_phoneservices = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
    scripts = bs.find_all(str_inurl)
    #get the strings for the names and the prices of the products using regular expressions
    prices_phoneservices= re.findall(regex_exp,str(scripts))

def scrapper_phoneservices_cyta(urls:list):
    #final list with prices
    global prices_final_phone
    prices_final_phone = []
    for url in urls:
        if url=='https://www.cyta.com.cy/upgraded-telephony/el':
            scrappe_page(url,'td',r"\€\d.\d*\s\/")
            prices_final_phone.append(float(prices_phoneservices[0].strip('\€').strip('\/').replace(',', '.')))
            prices_final_phone.append(float(prices_phoneservices[1].strip('\€').strip('\/').replace(',', '.')))

        if url=='https://www.cyta.com.cy/mobile-internet':
            scrappe_page(url,'strong',r"\€\d\d.\d\d")
            prices_final_phone.append(float(prices_phoneservices[0].strip('\€').replace(',', '.')))

        if url == 'https://www.cyta.com.cy/freedom-plans':
            scrappe_page(url,'span',r"\€\d\d.\d\d")
            prices_final_phone.append(float(prices_phoneservices[0].strip('\€').replace(',', '.')))

#put the rows in a list
all_items_cyta = []
for url,i,label in zip(urls_all_phones,range(len(urls_all_phones)),class_labels_phones):
    scrapper_phoneservices_cyta(url[0])
    for product,price in zip(url[1],prices_final_phone):
        all_items_cyta.append([product,price,datetime.now(),label,'CYTA',price])
            
#initialize a dataframe
df_cyta=pd.DataFrame(columns=('item.name','item.price','date.time','item.subclass','retailer','average price'))

#assign the values to each column
for i in range(len(all_items_cyta)):
    df.loc[len(df)] = (all_items_cyta[i][0],all_items_cyta[i][1],all_items_cyta[i][2],all_items_cyta[i][3],all_items_cyta[i][4],all_items_cyta[i][5])

urls_internet = [['https://primetel.com.cy/home-fiber-plans-en'],['HomeFiber60MBPS','HomeFiber150MBPS','Fiber200MBPS']]
urls_freedom = [['https://primetel.com.cy/giga-unlimited-en'],['GIGAUnlimited','GIGAUnlimitedPlus','GIGAUnlimitedMax']]

urls_all_phones = [ urls_internet,urls_freedom]

class_labels_phones = ['Internet access provision services','Bundled telecommunication services']

def scrappe_page(url,regex_exp):
    global prices_phoneservices
    prices_phoneservices = []
    page = urlopen(url)
    html = page.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
    scripts = bs.find_all('p',{'class':'price'})
    #get the strings for the names and the prices of the products using regular expressions
    prices_phoneservices= re.findall(regex_exp,str(scripts))


def scrapper_phoneservices_primetel(urls:list):
    #final list with prices
    global prices_final_phone
    prices_final_phone = []
    for url in urls:
        if url=='https://primetel.com.cy/home-fiber-plans-en':
            scrappe_page(url, r"\€\d\d.\d\d\<\/p")
            prices_final_phone.append(float(prices_phoneservices[0].strip('\€\<\/p').replace(',', '.')))
            prices_final_phone.append(float(prices_phoneservices[1].strip('\€\<\/p').replace(',', '.')))
            prices_final_phone.append(float(prices_phoneservices[2].strip('\€\<\/p').replace(',', '.')))

        if url=='https://primetel.com.cy/giga-unlimited-en':
            scrappe_page(url,r"\€\d.*" )
            prices_final_phone.append(float(prices_phoneservices[1].strip('\€')))
            prices_final_phone.append(float(prices_phoneservices[3].strip('\€')))
            prices_final_phone.append(float(prices_phoneservices[5].strip('\€')))

 # read csv file with product description, class and urls
products_urls = pd.read_excel('products_bpp.xlsx')

#put the rows in a list
all_items_primetel = []
for url,label in zip(urls_all_phones,class_labels_phones):
    scrapper_phoneservices_primetel(url[0])
    for product,price in zip(url[1],prices_final_phone):
        all_items_primetel.append([product,price,datetime.now(),label,'Primetel'])
            
#initialize a dataframe
df_primetel=pd.DataFrame(columns=('item.name','item.price','date.time','item.subclass','retailer'))

#assign the values to each column
for i in range(len(all_items_primetel)):
    df.loc[len(df)] = (all_items_primetel[i][0],all_items_primetel[i][1],all_items_primetel[i][2],all_items_primetel[i][3],all_items_primetel[i][4],0)



marksspencerdf = products_urls.iloc[209:227,]
marksspencerdf.head()

#the scrapper function
prices_final_marksspencer = []

def scrapper_marksspencer(urls:list):
    #for the different urls, putting the prices in a list
    url_marksspencer = 'https://www.marksandspencer.com/cy'
    for url in urls:
        try:
            url_new = url_marksspencer+url
            page = urlopen(url_new)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
    
            scripts = bs.find_all('span',{'class':"value"},string=True)
            #initial price list and the value of the final price scrapped
            price_ini=[]
            price_final = 0

            #get the strings for the prices of the products using regular expressions
            price_ini = re.findall(r'content=".+\>',str(scripts))

            #get only the first element
            price_final = float(price_ini[0].strip('content="">'))

            #add the price in the list    
            prices_final_marksspencer.append(price_final)
            
        except urllib.error.HTTPError as err:
            prices_final_marksspencer.append('NaN')

#columns urls,products,labels into lists
urls = marksspencerdf['item.url'].values.tolist()
products = marksspencerdf['item.name'].values.tolist()
labels = marksspencerdf['item.subclass'].values.tolist()

#scrap the prices
scrapper_marksspencer(urls)

#put the rows in a list
all_items_marksspencer = []
for product,price,label in zip(products,prices_final_marksspencer,labels):
    all_items_marksspencer.append([product,price,datetime.now(),label,'Marks&Spencer'])

#initialize a dataframe
df_marksspencer=pd.DataFrame(columns=('item.name','item.price','date.time','item.subclass','retailer'))

#assign the values to each column
for i in range(len(all_items_marksspencer)):
    df.loc[len(df)] = (all_items_marksspencer[i][0],all_items_marksspencer[i][1],all_items_marksspencer[i][2],all_items_marksspencer[i][3],all_items_marksspencer[i][4],0)

#change type of the item.price column
df_marksspencer['item.price'] = df_marksspencer['item.price'].astype('float32')




# internsportsdf = products_urls.iloc[226:243,]
# internsportsdf.head()

# #the scrapper function
# prices_final_internsports = []

# def scrapper_intersports(urls:list):
#     #for the different urls, putting the prices in a list
#     url_internsports = 'https://www.intersport.com.cy'
#     for url in urls:
#         try:
#             url_new = url_internsports+url
#             page = urlopen(url_new)
#             html = page.read().decode("utf-8")
#             bs = BeautifulSoup(html, "html.parser")
    
#             scripts = bs.find_all('span',{'itemprop':"price"},string=True)
#             #initialize the value of the final price scrapped
#             price_final = 0

#             #get only the first element
#             price_final = round(float(str(scripts[0]).strip('<span class="current-price" itemprop="price">€ </span>').replace(',', '.')),2)

#             #add the price in the list    
#             prices_final_internsports.append(price_final)
            
#         except urllib.error.HTTPError as err:
#             prices_final_internsports.append('NaN')

# #columns urls,products,labels into lists
# urls = internsportsdf['item.url'].values.tolist()
# products = internsportsdf['item.name'].values.tolist()
# labels = internsportsdf['item.subclass'].values.tolist()

# #scrap the prices
# scrapper_intersports(urls)

# #put the rows in a list
# all_items_internsports = []
# for product,price,label in zip(products,prices_final_internsports,labels):
#     all_items_internsports.append([product,price,datetime.now(),label,'InternSports'])

# #initialize a dataframe
# df_internsports=pd.DataFrame(columns=('item.name','item.price','date.time','item.subclass','retailer'))

# #assign the values to each column
# for i in range(len(all_items_internsports)):
#     df_internsports.loc[i] = (all_items_internsports[i][0],all_items_internsports[i][1],all_items_internsports[i][2],all_items_internsports[i][3],all_items_internsports[i][4])

# #change type of the item.price column
# df_internsports['item.price'] = df_internsports['item.price'].astype('float32')



famoussportsdf = products_urls.iloc[243:262,]
famoussportsdf.tail()

#the scrapper function
prices_final_famoussports = []

def scrapper_famoussports(urls:list):
    #for the different urls, putting the prices in a list
    url_famoussports = 'https://www.famousports.com/en'
    for url in urls:
        try:
            url_new = url_famoussports+url
            page = urlopen(url_new)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
    
            scripts = bs.find_all('strong',string=True)
            #initial price list and the value of the final price scrapped
            price_ini=[]
            price_final = 0

            #get the strings for the prices of the products using regular expressions
            price_ini = re.findall(r'\>\d.*\€',str(scripts))

            #get only the first element
            price_final = round(float(str(price_ini[0]).strip('>€').replace(',','.')),2)

            #add the price in the list    
            prices_final_famoussports.append(price_final)
            
        except urllib.error.HTTPError as err:
            prices_final_famoussports.append('NaN')

#columns urls,products,labels into lists
urls = famoussportsdf['item.url'].values.tolist()
products = famoussportsdf['item.name'].values.tolist()
labels = famoussportsdf['item.subclass'].values.tolist()

#scrap the prices
scrapper_famoussports(urls)

#put the rows in a list
all_items_famoussports = []
for product,price,label in zip(products,prices_final_famoussports,labels):
    all_items_famoussports.append([product,price,datetime.now(),label,'FamousSports'])

#initialize a dataframe
df_famoussports=pd.DataFrame(columns=('item.name','item.price','date.time','item.subclass','retailer'))

#assign the values to each column
for i in range(len(all_items_famoussports)):
    df.loc[len(df)] = (all_items_famoussports[i][0],all_items_famoussports[i][1],all_items_famoussports[i][2],all_items_famoussports[i][3],all_items_famoussports[i][4],0)

#change type of the item.price column
df_famoussports['item.price'] = df_famoussports['item.price'].astype('float32')


def garments():
    headers = {'User-agent': 'Mozilla/5.0'}  
    data_garmets = pd.read_csv("Garmets.csv")
    for index, am in data_garmets.iterrows():
        page = requests.get(am['website'].strip(),headers=headers)
        st=page.content.decode('utf-8')
        tree = html.fromstring(st)
        product_name = (''.join(am['product_name'])).replace(' ','').strip() 
        product_price=tree.xpath("//script[@type='application/ld+json']/text()")[0]
        if am['retailer'] == 'Bershka':
            product_price = json.loads(product_price)['offers'][0]['price']
        else:
            product_price = json.loads(product_price)['offers']['price']
        print(product_price)
        now = datetime.now()
        date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
        product_subclass=am['product_subclass']
        retailer= am['retailer']
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

garments()

def mazda():
    url = "https://www.mazda.com.cy/Portals/7/adam/Contents/dDx4iz_W80eqne0jNZvsdA/Link/Mazda2_DEC22.pdf"  # Replace with the URL of the PDF file
    response = requests.get(url)
    with open("file.pdf", "wb") as f:
        f.write(response.content)
    pdf_file = open("file.pdf", "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    page=pdf_reader.pages[0]
    prices = re.findall(r"€ (\d+\,\d{3}).*?", page.extract_text())
    prices[0] = prices[0].replace(',', '')
    product_price=int(prices[0])
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    product_name="New Mazda 2"
    product_subclass="New motor cars"
    retailer="Mazda"
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    pdf_file.close()
mazda()

def nissan():
        # Define the URL for the Booking.com page for hotel X
    url = "https://www.nissan.com.cy/vehicles/new-vehicles/juke-2022/prices-specifications.html#-"

    # Define the headers for the HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.content)
    # Use XPath to extract the price value
    price_xpath = '//iframe[@id="individualVehiclePriceJSON"]/text()'
    price_json = tree.xpath(price_xpath)[0]

    # Extract the price of 23500 from the JSON string
    import json
    price_data = json.loads(price_json)
    product_price = price_data['juke_2019']['default']['grades']['LVL001']['gradePrice']
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    product_name="Nissan Juke"
    product_subclass="New motor cars"
    retailer="Nissan"
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
nissan()

def Wolt():
    retailer="Wolt"
    product_subclass="Restaurants, cafes and dancing establishments"
    # Define the URL for the Booking.com page for hotel X
    url = "https://wolt.com/en/cyp/nicosia/restaurant/costanicosia"

    # Define the headers for the HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    url = 'https://wolt.com/en/cyp/nicosia/restaurant/costanicosia'
    response = requests.get(url)
    html_content = response.text

    tree = etree.HTML(html_content)

    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Cappuccino"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_cappuccino = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_cappuccino)[0].replace('€', ''))

    product_name="Costa Coffee Cappuccino Medio"
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


    # Find the button element containing the cappuccino information
    product_name="Costa Coffee Espresso Single"
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    button_xpath = '//button[descendant::h3[text()="Espresso"]]'
    button_element= tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_espresso = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_espresso)[0].replace('€', ''))

    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_name="Costa Coffee Freddo Cappuccino Medio"
    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Freddo Cappuccino"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_fcappuccino = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_fcappuccino)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_name="Costa Coffee Freddo Espresso Medio"
    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Freddo Espresso"]]'
    button_element= tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_fespresso = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    price_fespresso = float(button_element.xpath(price_xpath_fespresso)[0].replace('€', ''))
    product_price = float(button_element.xpath(price_xpath_fcappuccino)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    ###PIATSA GOUROUNAKI

    product_name="Piatsa Gourounaki, Meat platter for 2 persons  (Nicosia)"
    url = 'https://wolt.com/en/cyp/nicosia/restaurant/piatsa-gourounaki-mall-of-egkomi'
    response = requests.get(url)
    html_content = response.text

    tree = etree.HTML(html_content)

    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Ποικιλία Κρεάτων Για Δυο"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_pk2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_pk2)[0].replace('€', ''))

    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    ####PIXIDA  
    # Define the URL for the Booking.com page for hotel X
    product_name="Pixida, Fish meze for each guest with minimum 2 guests (Nicosia)"
    url = 'https://wolt.com/en/cyp/nicosia/restaurant/pyxida'
    response = requests.get(url)
    html_content = response.text

    tree = etree.HTML(html_content)

    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Meze Platter for 2"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_mp2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_mp2)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


    ###LIMASSOL
    product_name="Kofini Tavern Mix Grill for 2"
    url = 'https://wolt.com/en/cyp/limassol/restaurant/kofini-tavern#mix-grills-platters-6'
    response = requests.get(url)
    html_content = response.text

    tree = etree.HTML(html_content)

    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Mix Grill For 2"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_mg2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_mg2)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_name="Kofini Tavern, Seafood Platter"
    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Seafood Platter"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_sfp = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price= float(button_element.xpath(price_xpath_sfp)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    ## LARNACA VLACHOS
    product_name="Vlachos Taverna, Ποικιλία Σχάρας Για 2 Άτομα"
    url = 'https://wolt.com/en/cyp/larnaca/restaurant/vlachos-taverna#itemcategory-3'
    response = requests.get(url)
    html_content = response.text

    tree = etree.HTML(html_content)

    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Ποικιλία Σχάρας Για 2 Άτομα"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_mg2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_mg2)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


    ### Larnaca ZAKOS
    product_name="Zakos Beach Restaurant, Ψαρομεζέδες Ζάκος (Για 2 Άτομα)"
    url = 'https://wolt.com/en/cyp/larnaca/restaurant/zakos-beach-restaurant'
    response = requests.get(url)
    html_content = response.text

    tree = etree.HTML(html_content)

    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Ψαρομεζέδες Ζάκος (Για 2 Άτομα)"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_psz2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_psz2)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


    ### Paphos Tavernaki
    product_name="Paphos Tavernaki, Ποικιλία Σχάρας Για 2 Άτομα"
    url = 'https://wolt.com/en/cyp/paphos/restaurant/tavernaki-paphos#itemcategory-3'
    response = requests.get(url)
    html_content = response.text

    tree = etree.HTML(html_content)

    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Ποικιλία Σχάρας Για 2 Άτομα"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_ps2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_ps2)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


    ### Paphos Ocean Basket
    product_name="Ocean Basket, Platter for 2"
    url = 'https://wolt.com/en/cyp/paphos/restaurant/ocean-basket-paphos'
    response = requests.get(url)
    html_content = response.text

    tree = etree.HTML(html_content)

    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Platter For 2"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_p2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_p2)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_subclass="Fast food and take away food services"

    ###MACCIES

    url = 'https://wolt.com/en/cyp/limassol/restaurant/mcdonalds-oldport'
    response = requests.get(url)
    html_content = response.text

    tree = etree.HTML(html_content)

    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Share Box"]]'
    button_element = tree.xpath(button_xpath)[0]
    product_name="McDonald's Sharebox"
    # Extract the price from the button element
    price_xpath_sb = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_sb)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_name="McDonald's Big Mac"
    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="Big Mac"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_bm = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_bm)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_name="McDonald's McChicken"
    # Find the button element containing the cappuccino information
    button_xpath = '//button[descendant::h3[text()="McChicken"]]'
    button_element = tree.xpath(button_xpath)[0]

    # Extract the price from the button element
    price_xpath_mc = './/span[@data-test-id="horizontal-item-card-price"]/text()'
    product_price = float(button_element.xpath(price_xpath_mc)[0].replace('€', ''))
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
Wolt()

def PizzaHut():
    url = "https://www.pizzahut.com.cy/delivery-menu-mar.pdf?v=1"  # Replace with the URL of the PDF file
    response = requests.get(url)
    retailer="Pizza Hut"
    with open("file.pdf", "wb") as f:
        f.write(response.content)

    pdf_file = open("file.pdf", "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    product_subclass="Fast food and take away food services"
    # extracting price for margherita
    product_name="Pizza Hut Margherita Large"
    #assuming that text stays the same and prices change
    page=pdf_reader.pages[1]
    prices = re.findall(r"\b(\d+\.\d{2}).*?\b", page.extract_text())
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    product_price= prices[4]
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    product_name="Pizza Hut Classic Large"
    product_price=prices[8]
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    product_name="Pizza Hut Special Large"
    product_price=prices[16]
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    pdf_file.close()

PizzaHut()

def cera():
    url = "https://www.cera.org.cy/Templates/00001/data/hlektrismos/kostos_xrisis.pdf"  # Replace with the URL of the PDF file
    response = requests.get(url)
    retailer="Cyprus Energy Regulatory Authority"
    product_subclass="Electricity"
    with open("file.pdf", "wb") as f:
        f.write(response.content)

    cdf = read_pdf("file.pdf",pages="all")[0]
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    product_name="Καταναλωτές συνδεδεμένοι στο δίκτυο Χαμηλής Τάσης"
    product_price=cdf.loc[9][1]
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    product_name="Καταναλωτές συνδεδεμένοι στο δίκτυο Μέσης Τάσης"
    product_price=cdf.loc[9][2]
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    product_name="Καταναλωτές συνδεδεμένοι στο δίκτυο Υψηλής Τάσης"
    product_price=cdf.loc[9][3]
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

cera()

def water_board():
    url = "https://www.wbn.org.cy/καταναλωτής/διατιμήσεις/#content-d7d0c04646186e03a770"
    retailer="Water Board of Nicosia"
    product_subclass="Water supply"
    product_name='Water Board of Nicosia, Οικιακό Πάγιο Τέλος Νερού ανά διμηνία (Διατίμηση "Α" από 1 Σεπ 2017)'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    # Send the HTTP request and get the HTML content of the page
    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.content)
    price=tree.xpath("(//table[@id='ekit-table-container-9f0855a']/tbody/tr/td)[2]/div/text()")
    product_price=float((''.join(price)).replace(' ','').replace('€','').replace(',','.').strip())
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

water_board()

def sewage():
    url = "https://www.sbn.org.cy/el/apoxeteftika-teli"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send the HTTP request and get the HTML content of the page
    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.content)
    retailer="Sewerage Board of Nicosia"
    product_subclass="Sewage Collection"

    text_list=tree.xpath("/html/body/main/div[2]/div/div/ol/li[1]/text()")
    text1 = "".join(text_list)
    text_list2=tree.xpath("/html/body/main/div[2]/div/div/ol/li[2]/b[2]/text()")
    text2 = "".join(text_list2)

    product_name="Sewerage Board of Nicosia, Ετήσιο Τέλος Αποχέτευσης 2022 (€ για κάθε €1000 εκτιμημένης αξίας)"
    price_match = re.search(r"€([\d,\.]+) για κάθε €1000 εκτιμημένης αξίας", text1)
    if price_match:
        product_price = float(price_match.group(1).replace(",", "."))
        now = datetime.now()
        date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    else:
        print("Price not found in text.")

    # Extract the price from the text using a regular expression
    product_name="Sewerage Board of Nicosia, Τέλος Χρήσης Αποχέτευσης (€ ανά κυβικό μέτρο καταναλισκόμενου νερού)"
    price_match = re.search(r'(\d+(?:\.\d+)?)(?: σεντ)? ανά κυβικό μέτρο καταναλισκόμενου νερού', text2)

    # Check if the match was successful
    if price_match:
        # Get the matched string (including the optional " σεντ")
        price_str = price_match.group(1)

        # Convert the price to a float, accounting for cents if necessary
        if 'σεντ' in text2:
            product_price = float(price_str) / 100
        else:
            product_price = float(price_str)
        now = datetime.now()
        date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
        
    else:
        print('No price found in text')

sewage()

def fuel():

# Define the URL for the Booking.com page for hotel X
    url = "https://cyprusfuelguide.com/station?id=LU029"

    retailer="R.A.M. OIL CYPRUS LIMITED, Paphos"
    product_subclass="Petrol"

    product_name="Αμόλυβδη 95, Paphos"
    # Define the headers for the HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.content)
    price_paf95 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[1]/text()")
    product_price = price_paf95[0].replace('€', '')
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
 
    product_name="Αμόλυβδη 98, Paphos"
    price_paf98 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[2]/text()")
    product_price = price_paf98[0].replace('€', '')

    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
 
    retailer="R.A.M. OIL CYPRUS LIMITED, Nicosia"
    response = requests.get('https://cyprusfuelguide.com/station?id=EK008', headers=headers)
    tree = html.fromstring(response.content)
    product_name="Αμόλυβδη 95, Nicosia"
    price_nic95 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[1]/text()")
    product_price = price_nic95[0].replace('€', '')
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
 
    product_name="Αμόλυβδη 98, Nicosia"
    price_nic98 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[2]/text()")
    product_price = price_nic98[0].replace('€', '')
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    retailer="CORAL ENERGY PRODUCTS CYPRUS LTD, Limassol"
    response = requests.get('https://cyprusfuelguide.com/station?id=LU038', headers=headers)
    tree = html.fromstring(response.content)
    product_name="Αμόλυβδη 95, Limassol"
    price_lim95 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[1]/text()")
    product_price = price_lim95[0].replace('€', '')
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_name="Αμόλυβδη 98, Limassol"
    price_lim98 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[2]/text()")
    product_price = price_lim98[0].replace('€', '')
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


    retailer="R.A.M. OIL CYPRUS LIMITED, Larnaka"
    response = requests.get('https://cyprusfuelguide.com/station?id=EK027', headers=headers)
    tree = html.fromstring(response.content)
    product_name="Αμόλυβδη 95, Larnaka"
    price_lar95 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[1]/text()")
    product_price = price_lar95[0].replace('€', '')
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    product_name="Αμόλυβδη 98, Larnaka"
    price_lar98 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[2]/text()")
    product_price = price_lar98[0].replace('€', '')
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    retailer="ΝΙΚΟΛΑΟΥ Α. ΠΑΝΙΚΟΣ, Famagusta"
    response = requests.get('https://cyprusfuelguide.com/station?id=PE081', headers=headers)
    tree = html.fromstring(response.content)
    price_fam95 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[1]/text()")
    product_name="Αμόλυβδη 95, Famagusta"
    product_price = price_fam95[0].replace('€', '')
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    price_fam98 = tree.xpath("//table[@class='rmdl-data-table mdl-js-data-table mdl-shadow--2dp']/tbody/tr/td[2]/text()")
    product_price = price_fam98[0].replace('€', '')
    product_name="Αμόλυβδη 98, Famagusta"
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

fuel()

def Booking():

    retailer="Booking"
    product_subclass="Hotels, motels, inns and similar accommodation services"
   
# Define the URL for the Booking.com page for hotel X
    url = "https://www.booking.com/hotel/cy/frangiorgio-apartments.el.html"

    product_name="Frangiorgio Hotel, Τιμή για Δίκλινο για 1 βράδυ (Larnaca)"

    # Define the current month and year
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    # Find the last weekend of the current month
    last_day_of_month = datetime.date(year, month+1, 1) - datetime.timedelta(days=1)
    last_weekend = [d for d in range(26, 32) if datetime.date(year, month, d).weekday() == 5][0]

    # Define the date range and room type for the last weekend of the current month
    check_in_date = f"{year}-{month}-{last_weekend}"
    check_out_date = f"{year}-{month}-{last_weekend+1}"
    room_type_id = "4936308" 

    # Define the headers for the HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send the HTTP request and get the HTML content of the page
    params = {'checkin': check_in_date, 'checkout': check_out_date, 'room_id': room_type_id,'group_adult': 2}
    response = requests.get(url, headers=headers, params=params)
    tree = html.fromstring(response.content)



    # Check if the room type is available for the specified date range
    not_available = tree.xpath(f"//div[@id='{room_type_id}' and @class='room js-soldout-room-rate']")
    if not_available:
        print(f"Room type '{room_type_id}' is not available for the date range {check_in_date} - {check_out_date}")
    else:
        # Extract the relevant information from the HTML using XPath
        product_price = tree.xpath(f"(//tr[contains(@data-block-id,'{room_type_id}')])[1]/@data-hotel-rounded-price")
        now = datetime.now()
        date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_name="Navarria Blue Hotel, Τιμή για Δίκλινο για 1 βράδυ (Λεμεσός)"
    # Define the URL for the Booking.com page for hotel X
    url = "https://www.booking.com/hotel/cy/navarria-ag-tychonas.el.html"
    #  Δίκλινο Δωμάτιο με 1 Διπλό ή 2 Μονά Κρεβάτια 

    # Define the current month and year
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    # Find the last weekend of the current month
    last_day_of_month = datetime.date(year, month+1, 1) - datetime.timedelta(days=1)
    last_weekend = [d for d in range(26, 32) if datetime.date(year, month, d).weekday() == 5][0]

    # Define the date range and room type for the last weekend of the current month
    check_in_date = f"{year}-{month}-{last_weekend}"
    check_out_date = f"{year}-{month}-{last_weekend+1}"
    room_type_id = "23971501" 

    # Define the headers for the HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send the HTTP request and get the HTML content of the page
    params = {'checkin': check_in_date, 'checkout': check_out_date, 'room_id': room_type_id,'group_adult': 2}
    response = requests.get(url, headers=headers, params=params)
    tree = html.fromstring(response.content)

    # Check if the room type is available for the specified date range
    not_available = tree.xpath(f"//div[@id='{room_type_id}' and @class='room js-soldout-room-rate']")
    if not_available:
        print(f"Room type '{room_type_id}' is not available for the date range {check_in_date} - {check_out_date}")
    else:
        # Extract the relevant information from the HTML using XPath
        product_price = tree.xpath(f"(//tr[contains(@data-block-id,'{room_type_id}')])[1]/@data-hotel-rounded-price")
        now = datetime.now()
        date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    room_type_id = "105656305" 
    url="https://www.booking.com/hotel/cy/new-famagusta.el.html"
    product_name="New Famagusta Hotel & Suites, Τιμή για Δίκλινο για 1 βράδυ (Αγία Νάπα)"

    # Define the headers for the HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send the HTTP request and get the HTML content of the page
    params = {'checkin': check_in_date, 'checkout': check_out_date, 'room_id': room_type_id,'group_adult': 2}
    response = requests.get(url, headers=headers, params=params)
    tree = html.fromstring(response.content)

    # Check if the room type is available for the specified date range
    not_available = tree.xpath(f"//div[@id='{room_type_id}' and @class='room js-soldout-room-rate']")
    if not_available:
        print(f"Room type '{room_type_id}' is not available for the date range {check_in_date} - {check_out_date}")
    else:
        # Extract the relevant information from the HTML using XPath
        product_price = tree.xpath(f"(//tr[contains(@data-block-id,'{room_type_id}')])[1]/@data-hotel-rounded-price")
        now = datetime.now()
        date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


    room_type_id = "43130601" 
    url="https://www.booking.com/hotel/cy/flokkas-apartments.el.html"
    product_name="Flokkas Hotel Apartments, Τιμή για Δίκλινο για 1 βράδυ (Πρωταράς)"

    # Define the headers for the HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send the HTTP request and get the HTML content of the page
    params = {'checkin': check_in_date, 'checkout': check_out_date, 'room_id': room_type_id,'group_adult': 2}
    response = requests.get(url, headers=headers, params=params)
    tree = html.fromstring(response.content)

    # Check if the room type is available for the specified date range
    not_available = tree.xpath(f"//div[@id='{room_type_id}' and @class='room js-soldout-room-rate']")
    if not_available:
        print(f"Room type '{room_type_id}' is not available for the date range {check_in_date} - {check_out_date}")
    else:
        # Extract the relevant information from the HTML using XPath
        product_price = tree.xpath(f"(//tr[contains(@data-block-id,'{room_type_id}')])[1]/@data-hotel-rounded-price")
        now = datetime.now()
        date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


    room_type_id = "28716002" 
    url="https://www.booking.com/hotel/cy/asty-nicosia.el.html"
    product_name="Ξενοδοχείο Άστυ, Τιμή για Δίκλινο για 1 βράδυ (Λευκωσία)"

    # Define the headers for the HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send the HTTP request and get the HTML content of the page
    params = {'checkin': check_in_date, 'checkout': check_out_date, 'room_id': room_type_id,'group_adult': 2}
    response = requests.get(url, headers=headers, params=params)
    tree = html.fromstring(response.content)

    # Check if the room type is available for the specified date range
    not_available = tree.xpath(f"//div[@id='{room_type_id}' and @class='room js-soldout-room-rate']")
    if not_available:
        print(f"Room type '{room_type_id}' is not available for the date range {check_in_date} - {check_out_date}")
    else:
        # Extract the relevant information from the HTML using XPath
        product_price = tree.xpath(f"(//tr[contains(@data-block-id,'{room_type_id}')])[1]/@data-hotel-rounded-price")
        now = datetime.now()
        date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

Booking()

def extract_float_price(price_str):
    # Remove any non-digit characters except for the dot
    digits = ''.join(c for c in price_str if c.isdigit() or c == '.')
    # Convert the string to a float
    return float(digits)

def Rio():
    retailer="Rio Cinemas"
    product_subclass="Cinemas, theatres, concerts"
    url = 'https://www.riopremiercinemas.com.cy/price-policy/'
    response = requests.get(url)
    tree = html.fromstring(response.content)
    product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[2]/span/strong/text()")[0])
    product_name="Rio Cinemas, Adults ticket"
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[3]/span/strong/text()")[0])
    product_name="Rio Cinemas, Children (up to 11) ticket"
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[4]/span/strong/text()")[0])
    product_name="Rio Cinemas, Senior (64+)/ Student ticket"
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[6]/span/strong/text()")[0])
    product_name="Rio Cinemas, Adults 3D ticket"
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


    product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[7]/span/strong/text()")[0])
    product_name="Rio Cinemas, Children 3D ticket"
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[8]/span/strong/text()")[0])
    product_name="Rio Cinemas, Senior/Students 3D ticket"
    now = datetime.now()
    date_time_scraped = now.strftime("%d/%m/%Y %H:%M:%S")
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
   


df.to_csv("BillionPricesProject_ProductList.csv", index=False)



