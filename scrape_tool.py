# Import libraries
import pandas as pd 
import re
from lxml import html
import requests
from datetime import datetime
import time
import tabula as tb
import xlsxwriter

from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import json
from urllib.error import HTTPError


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
"/kritsinia?page=3","/kroutons","/fryganies","/paximadia","/paximadia?page=2","/paximadia?page=3","/paximadia?page=4","/koulourakia"],
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
 '3ΑΡύζιJasmine1kg', 'ΑφοίΑ.ΚεπόλαΠουργούρι1kg','ΑφοίΑ.ΚεπόλαΠουργούριΓιαΚούπες500g', 'ΜιτσίδηΠουργούρι500g', 'ΜιτσίδηΠουργούρι1kg',
'3ΑΠουργούρι500g','NaturalLifeΑποφλειωμένοΠουργούριΠιλάφι500g']]

urls_saltspices = [["/alati","/piperi","/mpacharika","/meigmata","/aromatika","/aromatika?page=2"],['SailorΑλάτι250g', 'CarnationSpicesΠιπέριΜαύροΑλεσμένο34g', 
'CarnationSpicesΚανέλαΑλεσμένη34g', 'CarnationSpicesΠάπρικαΓλυκιά30g', 'CarnationSpicesΚουρκουμάςΚιτρινόριζα30g', 'KnorrAromatΜείγμαΛαχανικών&amp;Μυρωδικών90g', 
'CarnationSpicesΔιάφοραΒότανα12g', 'CarnationSpicesΣκόρδοΣκόνη40g', 'CarnationSpicesΡίγανη30g', 'CarnationSpicesΘυμάρι10g', 'CarnationSpicesΚόλιανδροςΣκόνη20g', 
'CarnationSpicesΜαϊδανός10g', 'CarnationSpicesΒασιλικός10g', 'CarnationSpicesΆνηθος10g', 'CarnationSpicesΔεντρολίβανοΛάσμαρι10g']]

urls_nuts = [["/xiroi-karpoi","/xiroi-karpoi?page=2","/xiroi-karpoi?page=3","/xiroi-karpoi?page=4","/xiroi-karpoi?page=5","/apoxiramena-frouta",
"/apoxiramena-frouta?page=2","/apoxiramena-frouta?page=3","/apoxiramena-frouta?page=4"],['ΛειβαδιώτηΠράσινηΣφραγίδαΑμύγδαλα120g', 'SeranoΚάσιους140g', 
'ΛειβαδιώτηΚαρυδόψιχα140g', 'SeranoΦουντούκιαΩμά150g', 'SeranoΦυστικόψιχαΚαβουρδισμένηΑλατισμένη175g','ΕποχέςΑποξηραμέναΣύκα350g', 
'ΑμαλίαΧρυσόμηλαΑποξηραμένα250g', 'SeranoSnackin&#039;GoodΑποξηραμέναΔαμάσκηναΧωρίςΠρόσθετηΖάχαρη275g', 'ΚαρπόςΑπόΤηΓηΜαςΑποξηραμέναΒερίκοκα400g', 'ΑμαλίαΦοινίκιαΤυνησίας250g', 'SeranoΣταφίδες350g']]

urls_jams = [["/meli","/meli?page=2","/meli?page=3","/marmelades","/pralines","/fystikovoutyro","/diafora-aleimmata"],['RoyalBeeΜέλι475g', 'MavroudesΜέλι380g',
 'ΤοΤζιβέρτιΜέλιΑνθέωνSqueeze485g', 'BonapiΜέλιΑνθέων450g','BlossomΜαρμελάδαΜερίδες6x30g', 'Nutella200g', 'ΌλυμποςSuperSpreadΦυστικοβούτυροΤραγανό350g', 'DfΤαχίνι250g']]

urls_crisps = [["/patatakia"],['ΧαραλάμπουςΓαριδάκιαΜεΤυρί10X22g']]

urls_sauces=[["/ntomatas","/ntomatas?page=2","/ntomatas?page=3","/zomoi","/zomoi?page=2","/zomoi?page=3"],['PelargosΚλασικό3X250g', 
'ΜιτσίδηΠάσταΝτομάτας4X70g', 'BlossomΠάσταΝτομάτας4X70g', 'KeanPomiloriΠεραστήΝτομάτα690g', 'SwsΠάσταΝτομάτας425g','ΜιτσίδηΠεραστήΝτομάτα3x500g', 
'MaggiΖωμόςΚότας12Τεμ','MaggiΖωμόςΛαχανικών16Τεμ','MaggiΖωμόςΓιαΖυμαρικά12Τεμ','KnorrΖωμόςΚότας12Τεμ','KnorrΖωμόςΛαχανικών12Τεμ']]

urls_oil=[["/elaiolado","/elaiolado?page=2"],['ΆγιοςΓεώργιοςΚυπριακόΠαρθένοΕλαιόλαδο1L','ΕλιοχώριΠαρθένοΕλαιόλαδο2L', 'ΣεκέπΠαρθένοΕλαιόλαδο1L']]

urls_otheroil=[["/ilianthelaio"],['AlokozayΗλιανθέλαιο3L', 'AmbrosiaΗλιανθέλαιο3L','FloraΗλιανθέλαιο3L', 'AmbrosiaΗλιανθέλαιο4L']]

urls_preservedfish=[["/tonou","/tonou?page=2","/tonou?page=3"],['SevycoΆσπροςΤόνοςΣεΕλαιόλαδο4X95g', 'SevycoΤόνοςΣεΝερό4X200g',
 'RioMareΤόνοςΣεΕλαιόλαδο160g2+1Δωρεάν','RioMareΤόνοςΣεΕλαιόλαδο80g3+1Δωρεάν']]

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
['HeinzΣούπαΜινεστρόνι400g', 'HeinzΣούπαΝτομάτας400g',"ΦρουΦρουJoker9Τεμ9+3Δωρεάν","ΦρουΦρουMorningCoffee150g","KinderCards5Τεμ128g",
"Oreo154g","ΠαπαδοπούλουΓεμιστάΣοκολάτα200g"]]

urls_sugar = [["/aspri"],['SweetFamilyΛευκήΚρυσταλλικήΖάχαρη1kg']]

urls_flour= [["/alevri","/alevri?page=2"],['ΜιτσίδηΑλεύριΓιαΌλεςΤιςΧρήσεις1kg','ΜιτσίδηΑλεύριΦαρίνα001kg',
 'ΜιτσίδηΑλεύριΧωριάτικο1kg','ΜιτσίδηΑλεύριΦαρίναΖαχαροπλαστικής1kg','ΑδελφοίΚαζάζηΑλεύριΦαρίνα001kg','ΑδελφοίΚαζάζηΑλεύριΧωριάτικο1kg']]

urls_chocolate = [["/sokolata-galaktos","/lefki-sokolata"],['BakandysΣοκολάταΓάλακτοςΚουβερτούρα4X37.5g', 
'BakandysΆσπρηΣοκολάταΚουβερτούρα4x37.5g']]

urls_confectionary= [["/diafora-alla-eidi", "/diafora-alla-eidi?page=2","/diafora-alla-eidi?page=3"],['ΜοναμίΜαγειρικήΣόδα10X7g', 
'RoyalBakingPowder226g', 'ΣτέλλαΑνθόνεροΚιτρόμηλο500ml', 'ΑμαλίαΝησιαστέ400g', 'CarltonaΆμυλοΑραβοσίτου450g', 'BakandysΣαβουαγιάρ200g', 
'ΓιώτηςΜαγιάΣτιγμής3x8g', 'SeranoΙνδοκάρυδοΑλεσμένο140g1+1Δωρεάν', 'SpryΦυτικόΜαγειρικόΠροιόν350g', 'ΑγρούΡοδόσταγμα500ml']]

urls_freshvegetables= [[ "/freska-lachanika","/freska-lachanika?page=2","/freska-lachanika?page=3","/freska-lachanika?page=4",
"/freska-lachanika?page=5","/freska-lachanika?page=6","/freska-lachanika?page=7","/freska-lachanika?page=8","/freska-lachanika?page=9"],
['ΝτομάτεςΕλλάς1kg', 'ΑγγουράκιαΧωραφιού1kg', 'Λεμόνια1kg', 'ΚρεμμύδιαΑκαθάριστα1kg', 'Αγγουράκια1kg', 'ΝτοματίνιαΜίνιΦοινικωτά500g',
 'ΚαρόταΑκαθάριστα1kg', 'Αβοκάντο1kg', 'ΜαρούλιΡομάναΔέσμη1Τεμ', 'ΠιπεριέςΧρωματιστές4Τεμ', 'Σκόρδος1Τεμ']]

urls_potatoes =[["/freska-lachanika"],['ΦρέσκεςΠατάτεςΚυπριακέςΝέαςΣoδειάς2kg']]

urls_fruit = [["/freska-frouta","/freska-frouta?page=2","/freska-frouta?page=3"],['ΜπανάνεςΕισαγωγής1kg','ΜήλαPinkLady1kg', 'ΠράσινοΣταφύλι750g', 'ΜήλαGrannySmith1kg', 'ΑχλάδιαConference1kg', 
'ΜήλαΚόκκιναDelicious1kg', 'Μύρτιλα125g', 'ΜήλαΚίτριναDelicious1kg', 'Ακτινίδια500g', 'ΠορτοκάλιαMerlinAAA1kg', 'ΜήλαRoyalGala1kg', 'ΠορτοκάλιαΓιαΧυμό1kg']]

urls_pork= [["/klasikes-kopes-choirinou","/klasikes-kopes-choirinou?page=2"],['ΧοιρινόΚιμάςΜερί500g', 'ΧοιρινόΜπριζόλαΛαιμός4Τεμ1,200kg', 'ΧοιρινόΣούβλαΛαιμόςΛαπάςΜεΚόκκαλο1,1kg']]

urls_othermeat= [["/paraskeuasmata-choirinou"],['ΧοιρινόΣεφταλιές850g', 'ΛουκάνικαΧωριάτικα550g']]

urls_poultry = [["/kotopoulo","/kotopoulo?page=2"],['ΚοτόπουλοΦιλέτο850g', 'ΚοτόπουλοΟλόκληρο2,8kg']]

urls_lamb = [["/arni"],['ΑρνίΓιαΣούβλα1kg']]

urls_beaf= [["/vodino"],['ΒοδινόΚιμάς500g']]

urls_fish= [["/psaria"],['ΤσιπούραΦρέσκιαΚαθαρισμένη3ΤεμMax1,700kg']]

urls_preservedmilk= [["/makras-diarkeias"],['BertiΠλήρες3.5%ΓάλαΜακράςΔιαρκείας1L', 'BertiΕλαφρύ1.5%ΓάλαΜακράςΔιαρκείας1L']]

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
'Whole Milk','Yoghurt','Butter','Margarine and other vegetable fats','Eggs']



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



#put the rows in a list
all_items_primetel = []
for url,label in zip(urls_all_phones,class_labels_phones):
    scrapper_phoneservices_primetel(url[0])
    for product,price in zip(url[1],prices_final_phone):
        all_items_primetel.append([product,price,datetime.now(),label,'Primetel'])
            

#assign the values to each column
for i in range(len(all_items_primetel)):
    df.loc[len(df)] = (all_items_primetel[i][0],all_items_primetel[i][1],all_items_primetel[i][2],all_items_primetel[i][3],all_items_primetel[i][4],0)



# read csv file with product description, class and urls
products_urls = pd.read_excel('products_bpp.xlsx')
marksspencerdf = products_urls.iloc[209:227,]


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

all_items_marksspencer = []
for product,price,label in zip(products,prices_final_marksspencer,labels):
    all_items_marksspencer.append([product,price,datetime.now(),label,'Marks&Spencer'])

#assign the values to each column
for i in range(len(all_items_marksspencer)):
    df.loc[len(df)] = (all_items_marksspencer[i][0],all_items_marksspencer[i][1],all_items_marksspencer[i][2],all_items_marksspencer[i][3],all_items_marksspencer[i][4])






#Internsport
#the scrapper function
internsportsdf = products_urls.iloc[226:243,]

prices_final_internsports = []

def scrapper_intersports(urls:list):
    #for the different urls, putting the prices in a list
    url_internsports = 'https://www.intersport.com.cy'
    for url in urls:
        try:
            url_new = url_internsports+url
            page = urlopen(url_new)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
    
            scripts = bs.find_all('span',{'itemprop':"price"},string=True)
            #initialize the value of the final price scrapped
            price_final = 0

            #get only the first element
            price_final = round(float(str(scripts[0]).strip('<span class="current-price" itemprop="price">€ </span>').replace(',', '.')),2)

            #add the price in the list    
            prices_final_internsports.append(price_final)

        except ValueError as ve:
            #get only the first element
            price_final = round(float(str(scripts[0]).strip('<span class="current-price  price-with-discount   " itemprop="price">€ </span>').replace(',', '.')),2)

            #add the price in the list    
            prices_final_internsports.append(price_final)
            
        except urllib.error.HTTPError as err:
            prices_final_internsports.append('NaN')

        except IndexError:
            prices_final_internsports.append('NaN')

#columns urls,products,labels into lists
urls = internsportsdf['item.url'].values.tolist()
products = internsportsdf['item.name'].values.tolist()
labels = internsportsdf['item.subclass'].values.tolist()

#scrap the prices
scrapper_intersports(urls)

all_items_internsports = []
for product,price,label in zip(products,prices_final_internsports,labels):
    all_items_internsports.append([product,price,datetime.now(),label,'InternSports'])


#assign the values to each column
for i in range(len(all_items_internsports)):
    df.loc[len(df)] = (all_items_internsports[i][0],all_items_internsports[i][1],all_items_internsports[i][2],all_items_internsports[i][3],all_items_internsports[i][4])




famoussportsdf = products_urls.iloc[243:262,]


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

all_items_famoussports = []
for product,price,label in zip(products,prices_final_famoussports,labels):
    all_items_famoussports.append([product,price,datetime.now(),label,'FamousSports'])


#assign the values to each column
for i in range(len(all_items_famoussports)):
    df.loc[len(df)] = (all_items_famoussports[i][0],all_items_famoussports[i][1],all_items_famoussports[i][2],all_items_famoussports[i][3],all_items_famoussports[i][4])



#Athlokinisi
athlokinisidf = products_urls.iloc[262:280,]

#the scrapper function
prices_final_athlokinisi = []

def scrapper_athlokinisi(urls:list):
    #for the different urls, putting the prices in a list
    url_athlokinisi = 'https://athlokinisi.com.cy'
    for url in urls:
        try:
            url_new = url_athlokinisi+url
            page = urlopen(url_new)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
    
            scripts = bs.find_all('span',{'class':'ammount'},string=True)
            #get only the first element
            price_final = round(float(str(scripts[0]).strip('<span class="ammount">€ </span>')),2)

            #add the price in the list    
            prices_final_athlokinisi.append(price_final)
            
        except urllib.error.HTTPError as err:
            prices_final_athlokinisi.append('NaN')

        except IndexError:
            prices_final_athlokinisi.append('NaN')


#columns urls,products,labels into lists
urls = athlokinisidf['item.url'].values.tolist()
products = athlokinisidf['item.name'].values.tolist()
labels = athlokinisidf['item.subclass'].values.tolist()

#scrap the prices
scrapper_athlokinisi(urls)

all_items_athlokinisi = []
for product,price,label in zip(products,prices_final_athlokinisi,labels):
    all_items_athlokinisi.append([product,price,datetime.now(),label,'Athlokinisi'])


#assign the values to each column
for i in range(len(all_items_athlokinisi)):
    df.loc[len(df)] = (all_items_athlokinisi[i][0],all_items_athlokinisi[i][1],all_items_athlokinisi[i][2],all_items_athlokinisi[i][3],all_items_athlokinisi[i][4])



#the cygar shop
prices_final_cigars=[]

url = "https://www.thecygarshop.com/product-page/machetero-panatela"
page = urlopen(url)
html = page.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")
    
scripts = bs.find_all('span',{'data-hook':'formatted-primary-price'},string=True)
scripts
#get only the first element
price_final = float(str(scripts[0]).strip('<span data-hook="formatted-primary-price">€ </span>'))

#add the price in the list    
prices_final_cigars.append(price_final)

#numbeo
url = "https://www.numbeo.com/cost-of-living/country_price_rankings?itemId=17&displayCurrency=EUR"
page = urlopen(url)
html = page.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")
    
scripts = bs.find_all('script',string=True)
price_ini = re.findall(r"\['Cyprus', \d.+\]",str(scripts))
#get only the first element
price_final = float(str(price_ini[0]).strip("['Cyprus', ]"))

#add the price in the list    
prices_final_cigars.append(price_final)


#ewhole-sale
url = "https://www.ewsale.com/product-page/aspire-puxos-kit-%CE%B7%CE%BB%CE%B5%CE%BA%CF%84%CF%81%CE%BF%CE%BD%CE%B9%CE%BA%CE%AC-%CF%84%CF%83%CE%B9%CE%B3%CE%AC%CF%81%CE%B1-%CE%BC%CF%80%CE%B1%CF%84%CE%B1%CF%81%CE%AF%CE%B1-21700-200-ml-%CF%85%CE%B3%CF%81%CE%AC-%CE%AC%CF%84%CE%BC%CE%B9"
page = urlopen(url)
html = page.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")
    
scripts = bs.find_all('span',{'data-hook':'formatted-primary-price'},string=True)
#get only the first element
price_final = float(str(scripts[0]).strip('<span data-hook="formatted-primary-price">   €</span>').replace(',','.'))

#add the price in the list    
prices_final_cigars.append(price_final)

#columns urls,products,labels into lists
products = ['Machetero Panatela','Marlboro 20 Pack','Smok S-priv Kit E-Τσιγάρα + 2 μπαταρίες  + 200 ml Υγρά  άτμισης']
labels = ['Cigars','Cigarettes','Other Tobaco Products']
retailers = ['The CYgar Shop','NUMBEO','E-WHOLESALE']

#put the rows in a list
all_items_cigars = []
for product,price,label,retailer in zip(products,prices_final_cigars,labels,retailers):
    all_items_cigars.append([product,price,datetime.now(),label,retailer])


#assign the values to each column
for i in range(len(all_items_cigars)):
    df.loc[len(df)] = (all_items_cigars[i][0],all_items_cigars[i][1],all_items_cigars[i][2],all_items_cigars[i][3],all_items_cigars[i][4])


#stephanis
stephanisdf = products_urls.iloc[302:342,]

#the scrapper function
prices_final_stephanis = []

def scrapper_stephanis(urls:list):
    #for the different urls, putting the prices in a list
    url_stephanis = "https://www.stephanis.com.cy/en"
    for url in urls:
        try:
            url_new = url_stephanis+url
            page = urlopen(url_new)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
    
            scripts = bs.find_all('span',{'class':'item-price'},string=True)
            #get only the first element
            price_final = float(str(scripts[0]).strip('<span class="item-price">€ </span>'))

            #add the price in the list    
            prices_final_stephanis.append(price_final)
            
        except urllib.error.HTTPError as err:
            prices_final_stephanis.append('NaN')


#columns urls,products,labels into lists
urls = stephanisdf['item.url'].values.tolist()
products = stephanisdf['item.name'].values.tolist()
labels = stephanisdf['item.subclass'].values.tolist()

#scrap the prices
scrapper_stephanis(urls)

all_items_stephanis = []
for product,price,label in zip(products,prices_final_stephanis,labels):
    all_items_stephanis.append([product,price,datetime.now(),label,'Stephanis'])

#assign the values to each column
for i in range(len(all_items_stephanis)):
    df.loc[len(df)] = (all_items_stephanis[i][0],all_items_stephanis[i][1],all_items_stephanis[i][2],all_items_stephanis[i][3],all_items_stephanis[i][4])



#electroline
urls = ["https://electroline.com.cy/products/garden/garden-power-tools/%ce%b1%ce%bb%cf%85%cf%83%ce%bf%cf%80%cf%81%ce%af%ce%bf%ce%bd%ce%b1/oregon-cs1200-electric-chainsaw-1800w/",
        "https://electroline.com.cy/products/tools/hand-tools-2/screwdrivers/kapriol-kap33533-set-screwdrivers-6pcs/",
        "https://electroline.com.cy/products/garden-tools/hand-tools/hand-tools17002/tactix-900163-tool-set-14-pieces/"]

prices_final_electroline = []

for url in urls:
    try:
        #used for the request, urlopen functions
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        headers={'User-Agent':user_agent}   

        #initial price list and the value of the final price scrapped
        price_ini=[]
        
        #open and read the different urls
        request=urllib.request.Request(url,headers=headers) 
        response = urllib.request.urlopen(request)
        data = response.read().decode("utf-8")

        #get the strings for the prices of the products using regular expressions
        pattern = '\<meta property="product:price:amount" content="\d+.\d+" \/>'
        price_ini = re.findall(pattern,data)

        prices_final_electroline.append(float(str(price_ini[0]).strip('<meta property="product:price:amount" content=" " />')))
        
    except urllib.error.HTTPError as err:
            prices_final_electroline.append('NaN')

#columns urls,products,labels into lists
products = ['WORX 30091701000 Ηλεκτρικό Aλυσοπρίονο','TACTIX MER-205604 Σετ Kατσαβίδια, 12 Tεμάχια','TACTIX 900163 Σετ Εργαλείων 14 Τεμάχια',]
labels = ['Motorized major tools and equipment','Non-motorized small tools','Miscellaneous small tool accessories']

#put the rows in a list
all_items_electroline = []
for product,price,label in zip(products,prices_final_electroline,labels):
    all_items_electroline.append([product,price,datetime.now(),label,'Electroline'])


#assign the values to each column
for i in range(len(all_items_electroline)):
    df.loc[len(df)] = (all_items_electroline[i][0],all_items_electroline[i][1],all_items_electroline[i][2],all_items_electroline[i][3],all_items_electroline[i][4])



#awol
awoldf = products_urls.iloc[280:288,]

#the scrapper function
prices_final_awol = []

def scrapper_awol(urls:list):
    #for the different urls, putting the prices in a list
    url_awol = "https://www.awol.com.cy"
    for url in urls:
        try:
            #used for the request, urlopen functions
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            headers={'User-Agent':user_agent} 

            #initial price list and the value of the final price scrapped
            price_ini=[]
        
            #open and read the different urls
            request=urllib.request.Request(url_awol+url,headers=headers) 
            response = urllib.request.urlopen(request)
            data = response.read().decode("utf-8")

            #get the strings for the prices of the products using regular expressions
            pattern = '<meta property="og:price:amount" content="\d+.\d+">'
            price_ini = re.findall(pattern,data)

            prices_final_awol.append(float(str(price_ini[0]).strip('<meta property="og:price:amount" content=" " >').replace(',','.')))
            
        except urllib.error.HTTPError as err:
            prices_final_awol.append('NaN')


#columns urls,products,labels into lists
urls = awoldf['item.url'].values.tolist()
products = awoldf['item.name'].values.tolist()
labels = awoldf['item.subclass'].values.tolist()

#scrap the prices
scrapper_awol(urls)

all_items_awol = []
for product,price,label in zip(products,prices_final_awol,labels):
    all_items_awol.append([product,price,datetime.now(),label,'AWOL'])

#assign the values to each column
for i in range(len(all_items_awol)):
    df.loc[len(df)] = (all_items_awol[i][0],all_items_awol[i][1],all_items_awol[i][2],all_items_awol[i][3],all_items_awol[i][4])


#motorace
motoracedf = products_urls.iloc[288:302,]

#the scrapper function
prices_final_motorace = []

def scrapper_motorace(urls:list):
    #for the different urls, putting the prices in a list
    url_motorace = "https://www.motorace.com.cy"
    for url in urls:
        try:
            url_new = url_motorace+url
            page = urlopen(url_new)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
    
            scripts = bs.find_all('span',{'class':'price'},string=True)
            #get only the first element
            price_final = float(str(scripts[0]).strip('<span class="price">€ </span>').replace(',',''))

            #add the price in the list    
            prices_final_motorace.append(price_final)
            
        except urllib.error.HTTPError as err:
            prices_final_motorace.append('NaN')

#columns urls,products,labels into lists
urls = motoracedf['item.url'].values.tolist()
products = motoracedf['item.name'].values.tolist()
labels = motoracedf['item.subclass'].values.tolist()

#scrap the prices
scrapper_motorace(urls)

all_items_motorace = []
for product,price,label in zip(products,prices_final_awol,labels):
    all_items_motorace.append([product,price,datetime.now(),label,'MotoRace'])

#assign the values to each column
for i in range(len(all_items_motorace)):
    df.loc[len(df)] = (all_items_motorace[i][0],all_items_motorace[i][1],all_items_motorace[i][2],all_items_motorace[i][3],all_items_motorace[i][4])


#bwell pharmacy
# Bwell Pharmacy (https://bwell.com.cy/)
urls = ["https://bwell.com.cy/shop/health/cough-sore-throat/physiomer-hypertonic-eucalyptus-135-ml/",
        "https://bwell.com.cy/shop/mother-child/pregnancy-supplements/vitabiotics-pregnacare-original-30-tabs/",
        "https://bwell.com.cy/shop/health/medical-devices/geatherm-oxy-control-pulse-oximeter/",
        "https://bwell.com.cy/shop/health/medical-devices/flaem-respirair-nebulizer/"]

prices_final_bwell = []

for url in urls:
    #used for the request, urlopen functions
    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent} 

    #initial price list and the value of the final price scrapped
    price_ini=[]
        
    #open and read the different urls
    request=urllib.request.Request(url,headers=headers) 
    response = urllib.request.urlopen(request)
    data = response.read().decode("utf-8")

    #get the strings for the prices of the products using regular expressions
    pattern = '<\/span>&nbsp;\d+.\d+<\/bdi>'
    price_ini = re.findall(pattern,data)

    prices_final_bwell.append(float(str(price_ini[1]).strip('</span>&nbsp; </bdi>')))

#columns urls,products,labels into lists
products = ['Physiomer Nasal Spray Hygiene Active Prevention 135ml','Vitabiotics Pregnacare Original 30 tabs','Geatherm Oxy Control – Pulse Oximeter',
'Flaem RespirAir nebulizer']
labels = ['Pharmaceutical products','Pregnancy tests and mechanical contraceptive devices','Other medical products n.e.c.','Other therapeutic appliances and equipment']

#put the rows in a list
all_items_bwell = []
for product,price,label in zip(products,prices_final_bwell,labels):
    all_items_bwell.append([product,price,datetime.now(),label,'Bwell Pharmacy'])


#assign the values to each column
for i in range(len(all_items_bwell)):
    df.loc[len(df)] = (all_items_bwell[i][0],all_items_bwell[i][1],all_items_bwell[i][2],all_items_bwell[i][3],all_items_bwell[i][4])



#ikea
ikeadf = products_urls.iloc[342:371,]

#the scrapper function
prices_final_ikea = []

def scrapper_ikea(urls:list):
    #for the different urls, putting the prices in a list
    url_ikea = "https://www.ikea.com.cy"
    for url in urls:
        try:
            url_new = url_ikea+url
            page = urlopen(url_new)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
    
            scripts = bs.find_all('script',string=True)

            #get the strings for the prices of the products using regular expressions
            price_ini = re.findall(r'"fb_value": "\d+.\d+"',str(scripts))

            #add the price in the list    
            prices_final_ikea.append(float(price_ini[0].strip('"fb_value": " "')))
            
        except urllib.error.HTTPError as err:
            prices_final_ikea.append('NaN')

        except urllib.error.URLError:
            prices_final_ikea.append('NaN')

        except IndexError:
            prices_final_ikea.append('NaN')


#columns urls,products,labels into lists
urls = ikeadf['item.url'].values.tolist()
products = ikeadf['item.name'].values.tolist()
labels = ikeadf['item.subclass'].values.tolist()

#scrap the prices
scrapper_ikea(urls)

#put the rows in a list
all_items_ikea = []
for product,price,label in zip(products,prices_final_ikea,labels):
    all_items_ikea.append([product,price,datetime.now(),label,'IKEA'])


#assign the values to each column
for i in range(len(all_items_ikea)):
    df.loc[len(df)] = (all_items_ikea[i][0],all_items_ikea[i][1],all_items_ikea[i][2],all_items_ikea[i][3],all_items_ikea[i][4])




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


#Novella Hair Salon
prices_final_hairsalon = []
url_new = 'https://novella.com.cy/#services'
page = urlopen(url_new)
html = page.read().decode("utf-8")
bs = BeautifulSoup(html, "html.parser")

scripts = bs.find_all('td',{'class':'column-2'},string=True)
price_ini = re.findall(r'\€\d+,\d\d',str(scripts))

prices_final_hairsalon.append(round(float(str(price_ini[0]).strip('€').replace(',','.')),2))
prices_final_hairsalon.append(round(float(str(price_ini[4]).strip('€').replace(',','.')),2))

#################################################################################################################


df.loc[len(df)] = ("Women's Services, HAIRCUT Stylist",prices_final_hairsalon[0],datetime.now(),'Hairdressing for women','Novella Hair Salon')
df.loc[len(df)] = ("Men's Services, HAIRCUT Stylist",prices_final_hairsalon[1],datetime.now(),'Hairdressing for men','Novella Hair Salon')




#Cyprus Post
file = 'https://www.cypruspost.post/uploads/2cf9ec4f5a.pdf'
table_1 = tb.read_pdf(file, pages = '6',pandas_options={'header': None}, stream=True)
table_2 = tb.read_pdf(file, pages = '11',pandas_options={'header': None}, stream=True)

df_package_1 = table_1[0]
df_package_2 = table_2[0]

#change the type of columns that contain the prices
df_package_1[2]=df_package_1[2].astype('string')
df_package_2[1]=df_package_2[1].astype('string')

all_items_post = [("ΤΕΛΗ ΜΕΜΟΝΩΜΕΝΩΝ ΤΑΧΥΔΡΟΜΙΚΩΝ ΑΝΤΙΚΕΙΜΕΝΩΝ (ΕΠΙΣΤΟΛΙΚΟΥ ΤΑΧΥΔΡΟΜΕΙΟΥ) ΕΣΩΤΕΡΙΚΟΥ Α' ΠΡΟΤΕΡΑΙΟΤΗΤΑΣ Μικρά (P) 50 γρ.",round(float(df_package_1[2][14].split(' ')[0].replace(',','.')),2),datetime.now(),'Letter handling services','Cyprus Post'),
                 ("ΤΕΛΗ ΜΕΜΟΝΩΜΕΝΩΝ ΤΑΧΥΔΡΟΜΙΚΩΝ ΑΝΤΙΚΕΙΜΕΝΩΝ (ΕΠΙΣΤΟΛΙΚΟΥ ΤΑΧΥΔΡΟΜΕΙΟΥ) ΕΣΩΤΕΡΙΚΟΥ Α' ΠΡΟΤΕΡΑΙΟΤΗΤΑΣ Μεγάλα (G) 500 γρ.",round(float(df_package_1[2][21].split(' ')[0].replace(',','.')),2),datetime.now(),'Letter handling services','Cyprus Post'),
                 ("ΤΕΛΗ ΜΕΜΟΝΩΜΕΝΩΝ ΤΑΧΥΔΡΟΜΙΚΩΝ ΑΝΤΙΚΕΙΜΕΝΩΝ (ΕΠΙΣΤΟΛΙΚΟΥ ΤΑΧΥΔΡΟΜΕΙΟΥ) ΕΣΩΤΕΡΙΚΟΥ Α' ΠΡΟΤΕΡΑΙΟΤΗΤΑΣ Ακανόνιστα (E) 2000 γρ.",round(float(df_package_1[2][44].split(' ')[0].replace(',','.')),2),datetime.now(),'Letter handling services','Cyprus Post'),
                 ("ΤΕΛΗ ΥΠΗΡΕΣΙΑΣ ΔΕΜΑΤΩΝ ΕΣΩΤΕΡΙΚΟΥ 0.5 κιλό",round(float(df_package_2[1][2].replace(',','.')),2),datetime.now(),'Other postal services','Cyprus Post'),
                 ("ΤΕΛΗ ΥΠΗΡΕΣΙΑΣ ΔΕΜΑΤΩΝ ΕΣΩΤΕΡΙΚΟΥ 15 κιλά",round(float(df_package_2[1][17].replace(',','.')),2),datetime.now(),'Other postal services','Cyprus Post'),
                 ("ΤΕΛΗ ΥΠΗΡΕΣΙΑΣ ΔΕΜΑΤΩΝ ΕΣΩΤΕΡΙΚΟΥ 15 κιλά",round(float(df_package_2[1][32].replace(',','.')),2),datetime.now(),'Other postal services','Cyprus Post') ]

for i in range(6):
    df.loc[len(df)] = all_items_post[i]



#Cyprus Ministry of Education
#Caution the fees are for the year 2022-2023 based on the link:
#http://www.moec.gov.cy/idiotiki_ekpaidefsi/didaktra.html 

pdf_1 = tb.read_pdf('http://archeia.moec.gov.cy/mc/698/didaktra_idiotikon_mesi_ekpaidefsi.pdf', pages = '1',pandas_options={'header': None}, stream=True)
pdf_2 = tb.read_pdf('http://archeia.moec.gov.cy/mc/698/didaktra_idiotikon_dimotikon_scholeion.pdf', pages = '1',pandas_options={'header': None}, stream=True)
pdf_3 = tb.read_pdf('http://archeia.moec.gov.cy/mc/698/didaktra_idiotikon_nipiagogeion.pdf', pages = '3',pandas_options={'header': None}, stream=True)

df_secondary = pdf_1[0]
df_primary = pdf_2[0]
df_nursery =pdf_3[0]

#change the type of columns that contain the prices
df_nursery[7] = df_nursery[7].astype('string')
df_primary[3] = df_primary[3].astype('string')

for i in range(2,8):
    df_secondary[i]= df_secondary[i].astype('string')


avg_grammar_nic = (float(df_secondary[2][6])+float(df_secondary[3][6].split()[0])+float(df_secondary[3][6].split()[1])+float(df_secondary[4][6])+float(df_secondary[5][6])+float(df_secondary[6][6])+float(df_secondary[7][6]))/7
avg_grammar_lim = (float(df_secondary[2][23])+float(df_secondary[3][23].split()[0])+float(df_secondary[3][23].split()[1])+float(df_secondary[4][23])+float(df_secondary[5][23])+float(df_secondary[6][23])+float(df_secondary[7][23]))/7

all_items_school = [("THE GRAMMAR JUNIOR SCHOOL (Nicosia), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΝΗΠΙΑΓΩΓΕΙΩΝ 2022-2023",float(df_nursery[7][30].strip('€*').replace(".", "")),datetime.now(),'Pre-primary education (ISCED-97 level 0)','Cyprus Ministry of Education, Sport and Youth'),
                 ("THE GRAMMAR JUNIOR SCHOOL (Nicosia), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΔΗΜΟΤΙΚΩΝ ΣΧΟΛΕΙΩΝ 2022-2023",float(df_primary[3][15].strip('€').replace(",", "")),datetime.now(),'Primary education (ISCED-97 level 1)','Cyprus Ministry of Education, Sport and Youth'),
                 ("THE GRAMMAR SCHOOL (Nicosia), ΜΕΣΑ ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2022-2023, Α-ΣΤ ΤΑΞΗ",avg_grammar_nic,datetime.now(),'Secondary education','Cyprus Ministry of Education, Sport and Youth'),
                 ("THE GRAMMAR SCHOOL (Limassol), ΜΕΣΑ ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2022-2023, Α-ΣΤ ΤΑΞΗ",avg_grammar_lim,datetime.now(),'Secondary education','Cyprus Ministry of Education, Sport and Youth'),
                 ("THE GRAMMAR SCHOOL (Nicosia), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2022-2023, Ζ ΤΑΞΗ",float(df_secondary[7][6]),datetime.now(),'Post-secondary non-tertiary education (ISCED 4)','Cyprus Ministry of Education, Sport and Youth'),
                 ("THE GRAMMAR SCHOOL (Limassol), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2022-2023, Ζ ΤΑΞΗ",float(df_secondary[7][23]),datetime.now(),'Post-secondary non-tertiary education (ISCED 4)','Cyprus Ministry of Education, Sport and Youth') ]

for i in range(6):
    df.loc[len(df)] = all_items_school[i]



#Consumer Protection Service: Fuels
#https://eforms.eservices.cyprus.gov.cy/MCIT/MCIT/PetroleumPrices
#alternative: https://gr.globalpetrolprices.com/Cyprus/

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent} 

prices_final_petrol = []
url = 'https://gr.globalpetrolprices.com/Cyprus/'        

#open and read the different urls
url_new = url
request=urllib.request.Request(url,headers=headers) 
response = urllib.request.urlopen(request)
data = response.read().decode("utf-8")
data

pattern = '\d\.\d+\s'
price_ini = re.findall(pattern,data)

prices_final_petrol.append(float(str(price_ini[3]).strip('\r')))
prices_final_petrol.append(float(str(price_ini[6]).strip('\r')))
prices_final_petrol.append(float(str(price_ini[9]).strip('\r')))
prices_final_petrol.append(float(str(price_ini[12]).strip('\r')))

####################################################################################################

df.loc[len(df)] = ("Αμόλυβδη Μέση Τιμή Παγκύπρια",prices_final_petrol[0],datetime.now(),'Petrol','Global Petrol Prices')
df.loc[len(df)] = ("Πετρέλαιο Κίνησης Μέση Τιμή Παγκύπρια",prices_final_petrol[1],datetime.now(),'Diesel','Global Petrol Prices')
df.loc[len(df)] = ("Πετρέλαιο Μέση Τιμή Παγκύπρια",prices_final_petrol[2],datetime.now(),'Diesel','Global Petrol Prices')
df.loc[len(df)] = ("Πετρέλαιο Θέρμανσης Μέση Τιμή Παγκύπρια",prices_final_petrol[3],datetime.now(),'Liquid Fuels','Global Petrol Prices')


#Calculate the mean value for each category
#change type of the item.price column
df['product_price'] = df['product_price'].astype('float64')

#calculating the mean price of each category
df_mean  = round(df.groupby('product_subclass')[['product_price']].mean(),2)
df_mean.reset_index(drop=False, inplace=True)
df_mean.rename(columns={"product_price":"average price"},inplace=True)
df = pd.merge(df, df_mean, on="product_subclass", how="left")



df.to_csv("BillionPricesProject_ProductList.csv", index=False)



