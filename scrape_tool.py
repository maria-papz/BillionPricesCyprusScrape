# Import libraries
from ast import Try
import pandas as pd 
import re
from lxml import html, etree
import requests
from datetime import datetime
import time
import xlsxwriter
from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import json
import tabula as tb
from tabula import read_pdf
import PyPDF2
from datetime import date, timedelta
from urllib.error import URLError

#read from csv not to lose past records
df = pd.read_csv("BillionPricesProject_ProductList.csv")

# XPath for supermarketCy has a repeating pattern (may have the same pattern for other categories of the website as well)
# We create a function so that there is no need to find the XPath for every bread added
# Accepts name of bread and page the bread is found
# Returns scraped data

def SupermarketCyScrape():
    try:
        scy_data = pd.read_csv("SupermarketCy.csv")

        for webpage, group in scy_data.groupby('webpage'):
            found_product = set()
            pages = 1
            while pages <= 11:
                page = requests.get('https://www.supermarketcy.com.cy/'+webpage+'?page='+str(pages))
                # Parsing the page
                # (We need to use page.content rather than
                # page.text because html.fromstring implicitly
                # expects bytes as input.)
                tree = html.fromstring(page.content)

                for index, row in enumerate(group.itertuples()):
                    if index not in found_product:
                        retailer = 'SupermarketCy'
                        now = datetime.now()
                        date_time_scraped = now

                        ## product name
                        product_name = tree.xpath('//div[@data-title=\''+row.names+'\']/a/h5/text()')
                        product_subclass = row.product_subclass

                        # convert to string and remove whitespace
                        product_name = (''.join(product_name)).replace(' ', '').strip()

                        if product_name != '':
                            ## product price
                            product_price = tree.xpath('//div[contains(@data-title,\''+row.names+'\')]/div[@class="flex-col sm:flex-row"]/div[@class=\'sm:mr-10 flex justify-between\']//div/div[@class=\'text-primary text-h4 font-medium mb-8\']/text()')
                            product_price = float((''.join(product_price)).replace(' ', '').replace('€', '').replace(',', '.').strip())
                            df.loc[len(df)] = [product_name, product_price, date_time_scraped, product_subclass, retailer, 0]
                            found_product.add(index)
                        else:
                            if pages == 11:
                                product_name = (''.join(row.names)).replace(' ', '').strip()
                                df.loc[len(df)] = [product_name, None, date_time_scraped, product_subclass, retailer, 0]

                # Check if all products have been found
                if len(found_product) == len(group):
                    break

                pages += 1

    except Exception as e:
        print(f"Error occurred in SupermarketCyScrape(): {e}")

#put all the endings of the urls in lists based on the class they belong along with the descriptions of the products that should be scrapped

urls_bread = [['/psomi','/psomi?page=2','/psomi?page=3'],['ΣίφουναςΟλικήςΨωμίΚομμένο780g', 'ΣίφουναςΜαύροΜικρόΨωμίΚομμένο500g', 'ΣίφουναςΚοινόΨωμίΚομμένο560g', 
'ΣίφουναςΚοινόΨωμίΚομμένο970g', 'ΣίφουναςΆσπροΨωμί560g', 'ΣίφουναςΚοινόΨωμί970g']]

urls_bakery=[["/pites","/tost","/psomakia","/almyra","/keik","/glyka-1","/glyka-1?page=2","/krakers","/krakers?page=2","/kritsinia","/kritsinia?page=2",
"/kritsinia?page=3","/kroutons","/fryganies","/paximadia","/paximadia?page=2","/paximadia?page=3","/paximadia?page=4","/koulourakia","/koulourakia?page=2"],
['ΣίφουναςΠίττεςΆσπρεςΜεγάλες5Τεμ550g', 'ΣίφουναςΨωμίΦέτεςΤόστΆσπροΜικρό700g', 'ΣίφουναςΦραντζολάκιαΣτρογγυλά4Τεμ', 'ΣίφουναςΦραντζολάκιαΜακρόστεναΜεγάλα4Τεμ', 
'ΣίφουναςΚρουασάνΒουτύρου1Τεμ', 'ΣίφουναςΛουκανικόπιτα1Τεμ', 'ΣίφουναςΠίταΣάτζιηςΜεΜέλι1Τεμ', 'ΣίφουναςΕλιόπιταΣφολιάτα1Τεμ', 'ΣίφουναςΚέικΓεωγραφίας750g', 'ΣίφουναςMixΣιροπιαστά410g',
"7DaysMiniBakeRollsΠίτσα80g","BakandysΧωριάτικαΚριτσίνιαΣιταρένια275g","ΜαρίαςΠαξιμάδιαΓλυκανίσου300g","JohnsofΚρουτόνια320g",
"EliteΦρυγανιέςΜεΣίκαλη360g3+1Δώρο","EliteΦρυγανιέςΟλικήςΆλεσης360g3+1Δώρο","BakandysΠαξιμάδιαΣικάλεως250g"]]

urls_cereals=[["/dimitriaka?page=1","/dimitriaka?page=2","/dimitriaka?page=3","/dimitriaka?page=4","/dimitriaka?page=5","/dimitriaka?page=6","/dimitriaka?page=7","/dimitriaka?page=8","/dimitriaka?page=9","/dimitriaka?page=10","/dimitriaka?page=11"],
['QuakerΝιφάδεςΒρώμης500g', 'QuakerΤραγανέςΜπουκιέςΒρώμηΣοκολάτα450g','OreoO&#039;sCereal350g','KelloggsCornFlakes375g', 'KelloggsCocoPopsChocos375g',
 'KelloggsCocoPops500g', 'KelloggsSpecialK700g','KelloggsMielPopsLoops330g']]

urls_pastas=[["/makaronia","/makaronia?page=2","/makaronia?page=3","/makaronia?page=4","/penes","/penes?page=2",
"/kritharaki"],['BarillaΣπαγγέτιNo5500g', 'ΜέλισσαPrimoGustoΣπαγγέτιNo6500g', 'ΜέλισσαPrimoGustoΚριθαράκι500g',
'ΜιτσίδηΣπαγέττι500g','ΜιτσίδηΚριθαράκι500g','ΜιτσίδηΜακαρόνιαΑ500g','ΜιτσίδηΧωριάτικαΜακαρόνια500g','ΘίιαμβοςΣπαγέττο500g']]

urls_rice = [["/parmpoil", "/parmpoil?page=2","/mpasmati","/karolina","/glase","/pourgouri","/pourgouri?page=2","/diafora-ryzia"],
['3ΑΡύζιΠάρποιλτ1kg', 'BensOriginalΡύζιΜακρύκοκκο10Λεπτά1kg', 'TildaΡυζιΜπασματι1kg', '3ΑΡύζιΜπασμάτι1kg',
 '3ΑΡύζιJasmine1kg', 'ΑφοίΑ.ΚεπόλαΠουργούρι1kg','ΑφοίΑ.ΚεπόλαΠουργούριΓιαΚούπες500g', 'ΜιτσίδηΠουργούρι500g', 'ΜιτσίδηΠουργούρι1kg',
'3ΑΠουργούρι500g','NaturalLifeΑποφλειωμένοΠουργούριΠιλάφι500g']]

urls_saltspices = [["/alati","/piperi","/mpacharika","/meigmata","/aromatika","/aromatika?page=2"],['SailorΑλάτι250g', 'CarnationSpicesΠιπέριΜαύροΑλεσμένο34g', 
'CarnationSpicesΚανέλαΑλεσμένη34g', 'CarnationSpicesΠάπρικαΓλυκιά30g', 'CarnationSpicesΚουρκουμάςΚιτρινόριζα30g', 'KnorrAromatΜείγμαΛαχανικών&amp;Μυρωδικών90g', 
'CarnationSpicesΔιάφοραΒότανα12g', 'CarnationSpicesΣκόρδοΣκόνη40g', 'CarnationSpicesΡίγανη30g', 'CarnationSpicesΘυμάρι10g', 'CarnationSpicesΚόλιανδροςΣκόνη20g', 
'CarnationSpicesΜαϊδανός10g', 'CarnationSpicesΒασιλικός10g', 'CarnationSpicesΆνηθος10g', 'CarnationSpicesΔεντρολίβανοΛάσμαρι10g']]

urls_nuts = [["/xiroi-karpoi","/xiroi-karpoi?page=2","/xiroi-karpoi?page=3","/xiroi-karpoi?page=4","/xiroi-karpoi?page=5","/xiroi-karpoi?page=5","/xiroi-karpoi?page=6","/xiroi-karpoi?page=7","/apoxiramena-frouta",
"/apoxiramena-frouta?page=2","/apoxiramena-frouta?page=3","/apoxiramena-frouta?page=4"],['ΛειβαδιώτηΠράσινηΣφραγίδαΑμύγδαλα120g', 'SeranoΚάσιους140g', 
'ΑμαλίαΚαρυδόψιχα140g', 'ΑμαλίαΦουντούκιαΩμή140g', 'SeranoΦυστικόψιχαΚαβουρδισμένηΑλατισμένη175g','ΕποχέςΑποξηραμέναΣύκα350g', 
'ΑμαλίαΧρυσόμηλαΑποξηραμένα250g', 'SeranoSnackin&#039;GoodΑποξηραμέναΔαμάσκηναΧωρίςΚουκούτσιΧωρίςΠρόσθετηΖάχαρη250g', 'ΚαρπόςΑπόΤηΓηΜαςΑποξηραμέναΔαμάσκηναΜεΚουκούτσι400g', 
'ΑμαλίαΦοινίκιαΤυνησίας250g', 'SeranoΣταφίδες350g']]

urls_jams = [["/meli","/meli?page=2","/meli?page=3","/marmelades","/pralines","/fystikovoutyro","/diafora-aleimmata"],['RoyalBeeΜέλι475g', 'MavroudesΜέλι380g',
 'ΤοΤζιβέρτιΜέλιΑνθέωνSqueeze485g', 'BonapiΜέλιΑνθέων450g','BlossomΜαρμελάδαΜερίδες6x30g', 'Nutella200g', 'ΌλυμποςSuperSpreadΦυστικοβούτυροΑπαλό350g', 'DfΤαχίνι250g']]

urls_crisps = [["/patatakia"],['ΧαραλάμπουςΓαριδάκιαΜεΤυρί10X22g']]

urls_sauces=[["/ntomatas","/ntomatas?page=2","/ntomatas?page=3","/zomoi","/zomoi?page=2","/zomoi?page=3"],['PelargosΚλασικό3X250g', 
'ΜιτσίδηΠάσταΝτομάτας4X70g', 'BlossomΠάσταΝτομάτας4X70g', 'KeanPomiloriΠεραστήΝτομάτα690g', 'SwsΠάσταΝτομάτας425g','ΜιτσίδηΠεραστήΝτομάτα3x500g', 
'MaggiΖωμόςΚότας12Τεμ','MaggiΖωμόςΛαχανικών16Τεμ','MaggiΖωμόςΓιαΖυμαρικά12Τεμ','KnorrΖωμόςΚότας12Τεμ','KnorrΖωμόςΛαχανικών12Τεμ']]

urls_oil=[["/elaiolado","/elaiolado?page=2"],['ΆγιοςΓεώργιοςΠαρθένοΕλαιόλαδο2L','ΕλιοχώριΠαρθένοΕλαιόλαδο2L', 'ΣεκέπΠαρθένοΕλαιόλαδο1L']]

urls_otheroil=[["/ilianthelaio"],['AlokozayΗλιανθέλαιο1L', 'AmbrosiaΗλιανθέλαιο3L','ΕμμέλειαΡαφιναρισμένοΗλιανθέλαιο3L', 'AmbrosiaΗλιανθέλαιο4L']]

urls_preservedfish=[["/tonou","/tonou?page=2","/tonou?page=3"],['SevycoΆσπροςΤόνοςΣεΕλαιόλαδο4X95g', 'SevycoΡοζέΤόνοςΣεΣογιέλαιο4X200g',
 'RioMareΤόνοςΣεΕλαιόλαδο160g2+1Δωρεάν','RioMareΤόνοςΣεΝερό80g3+1Δωρεάν']]

urls_driedfish = [["/psariou-1"],['ΚαμήλαΣαρδελάκιαΣεΗλιανθέλαιο120g', 'TrataΡέγγαΚαπνιστή160g', 'FlokosΦιλέτοΣκουμπρίΚαπνιστόΣεΦυτικόΛάδι160g',
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

urls_sugar = [["/aspri"],["ΠερμανθούληςΛευκήΚρυσταλλικήΖάχαρη1kg"]]

urls_flour= [["/alevri","/alevri?page=2"],['ΜιτσίδηΑλεύριΓιαΌλεςΤιςΧρήσεις1kg','ΜιτσίδηΑλεύριΦαρίνα001kg',
 'ΜιτσίδηΑλεύριΧωριάτικο1kg','ΜιτσίδηΑλεύριΦαρίναΖαχαροπλαστικής1kg','ΑδελφοίΚαζάζηΑλεύριΦαρίνα001kg','ΑδελφοίΚαζάζηΑλεύριΧωριάτικο1kg']]

urls_chocolate = [["/sokolata-galaktos","/lefki-sokolata"],['BakandysΣοκολάταΓάλακτοςΚουβερτούρα4x37.5g', 
'BakandysΆσπρηΣοκολάταΚουβερτούρα4x37.5g']]

urls_confectionary= [["/diafora-alla-eidi", "/diafora-alla-eidi?page=2","/diafora-alla-eidi?page=3","/apoxiramena-frouta?page=5","/mageiriki-soda"],['HristalΜαγειρικήΣόδα125g', 
'RoyalBakingPowder113g', 'ΣτέλλαΑνθόνεροΚιτρόμηλο500ml', 'ΑμαλίαΝησιαστέ400g', 'CarltonaΆμυλοΑραβοσίτου450g', 'BakandysΣαβουαγιάρ200g', 
'ΓιώτηςΜαγιάΣτιγμής3x8g', 'ΑμαλίαΙνδοκάρυδοΑλεσμένο250g', 'SpryΦυτικόΜαγειρικόΠροιόν350g', 'ΑγρούΡοδόσταγμα500ml']]

urls_freshvegetables= [[ "/freska-lachanika","/freska-lachanika?page=2","/freska-lachanika?page=3","/freska-lachanika?page=4",
"/freska-lachanika?page=5","/freska-lachanika?page=6","/freska-lachanika?page=7","/freska-lachanika?page=8","/freska-lachanika?page=9"],
['Ντομάτες1kg', 'ΑγγουράκιαΧωραφιού1kg', 'Λεμόνια1kg', 'ΚρεμμύδιαΑκαθάριστα1kg', 'Αγγουράκια1kg', 'ΝτοματίνιαΜίνιΦοινικωτά500g',
 'ΚαρόταΑκαθάριστα1kg', 'Αβοκάντο1kg', 'ΜαρούλιΡομάναΔέσμη1Τεμ', 'ΠιπεριέςΧρωματιστές4Τεμ', 'Σκόρδος1Τεμ']]

urls_potatoes =[["/freska-lachanika"],['ΦρέσκεςΠατάτεςΚυπριακέςΝέαςΣoδειάς2kg']]

urls_fruit = [["/freska-frouta","/freska-frouta?page=2","/freska-frouta?page=3"],['ΜπανάνεςΕισαγωγής1kg','ΜήλαPinkLady1kg', 'ΠράσινοΣταφύλι750g', 'ΜήλαGrannySmith1kg', 'ΑχλάδιαConference1kg', 
'ΜήλαΚόκκιναDelicious1kg', 'Μύρτιλα125g', 'ΜήλαΚίτριναDelicious1kg', 'Ακτινίδια500g', 'ΜήλαRoyalGala1kg', 'ΠορτοκάλιαΓιαΧυμό1kg']]

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
'FloraLight100%Φυτικό450g', 'ΜινέρβαΦαστSoftLight220g']]

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
            price_excelfinal.append(None)  
    
#scrape all the websites and assign for each product the price, date, label class and retailer
all_items_supermarketcy = []
for url,i,label in zip(urls_all,range(len(urls_all)),class_labels):
    scrapper_supermarketcy(url[0],url[1])
    for product,price in zip(product_excelfinal,price_excelfinal):
        all_items_supermarketcy.append([product,price,datetime.now(),label,'SupermarketCy',mean_price])
            
#assign the values to each column
for i in range(len(all_items_supermarketcy)):
    df.loc[len(df)] = (all_items_supermarketcy[i][0],all_items_supermarketcy[i][1],all_items_supermarketcy[i][2],all_items_supermarketcy[i][3],all_items_supermarketcy[i][4],0)

#ALPHAMEGA
def AlphaMega():
    try:
        data_alphaMega = pd.read_csv("AlphaMega.csv")
        for index, am in data_alphaMega.iterrows():
            page = requests.get(am['website'].strip())
            tree = html.fromstring(page.content)
            product_name = (''.join(am['product_name'])).replace(' ', '').strip()
            now = datetime.now()
            date_time_scraped = now
            product_subclass = am['product_subclass']
            retailer = am['retailer']
            t = tree.xpath("//div[@class='grid grid--align-content-start']/script[@type='application/ld+json']/text()")
            if len(t) > 0:
                product_price = t[0]
                # Preprocess the product_price string
                product_price = product_price.replace('\n', '').replace('\r', '')

                # Use regex to extract the price
                price_match = re.search(r'"price":\s*"([\d.]+)"', product_price)
                if price_match:
                    product_price = price_match.group(1)
                else:
                    print(f"No price found for product: {product_name}")
                    continue
                df.loc[len(df)] = [product_name, product_price, date_time_scraped, product_subclass, retailer, 0]
            else:
                df.loc[len(df)]=[product_name, None, date_time_scraped, product_subclass, retailer, 0]
    except Exception as e:
        print(f"Error occurred in AlphaMega(): {e}")

AlphaMega()

SupermarketCyScrape()

#CYTA
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
            if prices_phoneservices:
                prices_final_phone.append(float(prices_phoneservices[0].strip('\€').strip('\/').replace(',', '.')))
            else:
                prices_final_phone.append(None)
            if len(prices_phoneservices)>1:
                prices_final_phone.append(float(prices_phoneservices[1].strip('\€').strip('\/').replace(',', '.')))
            else:
                prices_final_phone.append(None)

        if url=='https://www.cyta.com.cy/mobile-internet':
            scrappe_page(url,'strong',r"\€\d\d.\d\d")
            if prices_phoneservices:
                prices_final_phone.append(float(prices_phoneservices[0].strip('\€').replace(',', '.')))
            else:
                prices_final_phone.append(None)

        if url == 'https://www.cyta.com.cy/freedom-plans':
            scrappe_page(url,'span',r"\€\d\d.\d\d")
            if prices_phoneservices:
                prices_final_phone.append(float(prices_phoneservices[0].strip('\€').replace(',', '.')))
            else:
                prices_final_phone.append(None)

#put the rows in a list
all_items_cyta = []
for url,i,label in zip(urls_all_phones,range(len(urls_all_phones)),class_labels_phones):
    scrapper_phoneservices_cyta(url[0])
    for product,price in zip(url[1],prices_final_phone):
        all_items_cyta.append([product,price,datetime.now(),label,'CYTA',price])
            
#assign the values to each column
for i in range(len(all_items_cyta)):
    df.loc[len(df)] = (all_items_cyta[i][0],all_items_cyta[i][1],all_items_cyta[i][2],all_items_cyta[i][3],all_items_cyta[i][4],all_items_cyta[i][5])

#PRIMETEL
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
            if prices_phoneservices:
                prices_final_phone.append(float(prices_phoneservices[0].strip('\€\<\/p').replace(',', '.')))
            else:
                prices_final_phone.append(None)
            if len(prices_phoneservices)>1:
                prices_final_phone.append(float(prices_phoneservices[1].strip('\€\<\/p').replace(',', '.')))
            else:
                prices_final_phone.append(None)
            if len(prices_phoneservices)>2:
                prices_final_phone.append(float(prices_phoneservices[2].strip('\€\<\/p').replace(',', '.')))
            else:
                prices_final_phone.append(None)

        if url=='https://primetel.com.cy/giga-unlimited-en':
            scrappe_page(url,r"\€\d.*" )
            if len(prices_phoneservices)>1:
                prices_final_phone.append(float(prices_phoneservices[1].strip('\€')))
            else:
                prices_final_phone.append(None)
            if len(prices_phoneservices)>3:
                prices_final_phone.append(float(prices_phoneservices[3].strip('\€')))
            else:
                prices_final_phone.append(None)
            if len(prices_phoneservices)>5:
                prices_final_phone.append(float(prices_phoneservices[5].strip('\€')))
            else:
                prices_final_phone.append(None)

#put the rows in a list
all_items_primetel = []
for url,label in zip(urls_all_phones,class_labels_phones):
    scrapper_phoneservices_primetel(url[0])
    for product,price in zip(url[1],prices_final_phone):
        all_items_primetel.append([product,price,datetime.now(),label,'Primetel'])
            
#assign the values to each column
for i in range(len(all_items_primetel)):
    df.loc[len(df)] = (all_items_primetel[i][0],all_items_primetel[i][1],all_items_primetel[i][2],all_items_primetel[i][3],all_items_primetel[i][4],0)

#CABLENET
def cablenet():
    proxies = {
    'http': 'http://your_proxy_server:your_proxy_port',
    'https': 'https://your_proxy_server:your_proxy_port',}

    url = "https://cablenet.com.cy/τηλεφωνία/τέλη-τοπικών-κλήσεων/"
    response = requests.get(url,proxies )

    tree = html.fromstring(response.content)

    price_element = tree.xpath("//tr/td[text()='CYTA Σταθερό Δίκτυο']/following-sibling::td[3]")
    if price_element:
        price = price_element[0].text
        df.loc[len(df)]=['Κλήσειςπροςσταθερό',price,datetime.now(),'Wired telephone services','Cablenet',0]
    else:
         df.loc[len(df)]=['Κλήσειςπροςσταθερό',None,datetime.now(),'Wired telephone services','Cablenet',0]

    url = "https://cablenet.com.cy/χρεώσεις/"
    response = requests.get(url)
    tree = html.fromstring(response.content)

    price_element = tree.xpath("//tr/td[text()='National Mobile']/following-sibling::td[3]")
    if price_element:
        price = price_element[0].text
        price= price.split('/')[0]
        df.loc[len(df)]=['Κλήσειςπροςκινητό',price,datetime.now(),'Wireless telephone services','Cablenet',0]
    else:
        df.loc[len(df)]=['Κλήσειςπροςκινητό',None,datetime.now(),'Wireless telephone services','Cablenet',0]

    # Make a GET request to the webpage
    url = "https://cablenet.com.cy/purpleinternet/"
    response = requests.get(url)

    # Parse the HTML content
    html_content = response.content
    tree = etree.HTML(html_content)

    price_with_euro_sign_l = tree.xpath( "//p[contains(text(), 'χωρίς συμβόλαιο')]/preceding-sibling::p[2]//strong/text()")

    if price_with_euro_sign_l:
        price_with_euro_sign = price_with_euro_sign_l[0]
        price = price_with_euro_sign.replace("€", "")
        df.loc[len(df)]=['PurpleInternet',price,datetime.now(),'Internet access provision services','Cablenet',0]
    else:
        df.loc[len(df)]=['PurpleInternet',None,datetime.now(),'Internet access provision services','Cablenet',0]

    # Make a GET request to the webpage
    url = "https://cablenet.com.cy/en/packages-mobile/"
    response = requests.get(url)

    # Parse the HTML content
    html_content = response.content
    tree = etree.HTML(html_content)

    price_with_euro_sign_l = tree.xpath( "(//div[@class='wpb_text_column us_custom_1e54aa4c']//span[contains(@style, 'font-size: 300%')]/strong/text())[3]")
    if price_with_euro_sign_l:
        price_with_euro_sign = price_with_euro_sign_l[0]
        price = price_with_euro_sign.replace("€", "")
        df.loc[len(df)]=['PurpleMaxMobile',price,datetime.now(),'Bundled telecommunication services','Cablenet',0] 
    else:
        df.loc[len(df)]=['PurpleMaxMobile',None,datetime.now(),'Bundled telecommunication services','Cablenet',0] 

cablenet()

#EPIC
def epic():
    name='Internet and Telephony 10'
    url = "https://www.epic.com.cy/en/page/H1r10tnT/internet-telephony"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    price=tree.xpath("(//div[@class='mtn-data'])[1]/div[@class='mtn-prices mtn-equal mtn-prices-bb']/div[@class='mtn-from']/div[@class='price']/text()")
    if price:
        price=price[0].replace("€","")
        price=price.replace(".","")
        df.loc[len(df)]=[name,price,datetime.now(),'Internet access provision services','epic',0]
    else:
        df.loc[len(df)]=[name,None,datetime.now(),'Internet access provision services','epic',0]

    name='Internet and Telephony 20'
    url = "https://www.epic.com.cy/en/page/H1r10tnT/internet-telephony"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    price=tree.xpath("(//div[@class='mtn-data'])[2]/div[@class='mtn-prices mtn-equal mtn-prices-bb']/div[@class='mtn-from']/div[@class='price']/text()")
    if price:
        price=price[0].replace("€","")
        price=price.replace(".","")
        df.loc[len(df)]=[name,price,datetime.now(),'Internet access provision services','epic',0]  
    else:
        df.loc[len(df)]=[name,None,datetime.now(),'Internet access provision services','epic',0]  

    name='Internet and Telephony 50'
    url = "https://www.epic.com.cy/en/page/H1r10tnT/internet-telephony"
    response = requests.get(url)
    tree = html.fromstring(response.content)
    price=tree.xpath("(//div[@class='mtn-data'])[3]/div[@class='mtn-prices mtn-equal mtn-prices-bb']/div[@class='mtn-from']/div[@class='price']/text()")
    if price:
        price=price[0].replace("€","")
        price=price.replace(".","")
        df.loc[len(df)]=[name,price,datetime.now(),'Internet access provision services','epic',0]
    else:
        df.loc[len(df)]=[name,None,datetime.now(),'Internet access provision services','epic',0]

epic()

# read csv file with product description, class and urls
products_urls = pd.read_excel('products_bpp.xlsx')

#MARKS&SPENCER
marksspencerdf = products_urls.iloc[206:223,]

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
            if price_ini:
                price_final = float(price_ini[0].strip('content="">'))

                #add the price in the list    
                prices_final_marksspencer.append(price_final)
            else:
                prices_final_marksspencer.append(None)
            
        except urllib.error.HTTPError as err:
            prices_final_marksspencer.append('NaN')

#columns urls,products,labels into lists
urls = marksspencerdf['item.url'].values.tolist()
products = marksspencerdf['item.name'].values.tolist()
labels = marksspencerdf['item.subclass'].values.tolist()

#scrape the prices
scrapper_marksspencer(urls)

#put the rows in a list
all_items_marksspencer = []
for product,price,label in zip(products,prices_final_marksspencer,labels):
    all_items_marksspencer.append([product,price,datetime.now(),label,'Marks&Spencer'])

#assign the values to each column
for i in range(len(all_items_marksspencer)):
    df.loc[len(df)] = (all_items_marksspencer[i][0],all_items_marksspencer[i][1],all_items_marksspencer[i][2],all_items_marksspencer[i][3],all_items_marksspencer[i][4],0)

#ATHLOKINISI
athlokinisidf = products_urls.iloc[259:276,]
 
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
            if scripts:
                #get only the first element
                price_final = round(float(str(scripts[0]).strip('<span class="ammount">€ </span>')),2)
                #add the price in the list    
                prices_final_athlokinisi.append(price_final)
            else:
                prices_final_athlokinisi.append(None)

        except urllib.error.HTTPError as err:
            prices_final_athlokinisi.append('NaN')

        except IndexError:
            prices_final_athlokinisi.append('NaN')

#columns urls,products,labels into lists
urls = athlokinisidf['item.url'].values.tolist()
products = athlokinisidf['item.name'].values.tolist()
labels = athlokinisidf['item.subclass'].values.tolist()
division = athlokinisidf['item.division'].values.tolist()

#scrape the prices
scrapper_athlokinisi(urls)

#put the rows in a list
all_items_athlokinisi = []
for product,price,label in zip(products,prices_final_athlokinisi,labels):
     all_items_athlokinisi.append([product,price,datetime.now(),label,'Athlokinisi'])

#assign the values to each column
for i in range(len(all_items_athlokinisi)):
    df.loc[len(df)] = (all_items_athlokinisi[i][0],all_items_athlokinisi[i][1],all_items_athlokinisi[i][2],all_items_athlokinisi[i][3],all_items_athlokinisi[i][4],0)

#INTERSPORT
# internsportsdf = products_urls.iloc[223:240,]

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

# #assign the values to each column
# for i in range(len(all_items_internsports)):
#     df_internsports.loc[i] = (all_items_internsports[i][0],all_items_internsports[i][1],all_items_internsports[i][2],all_items_internsports[i][3],all_items_internsports[i][4])

#FAMOUSSPORT
famoussportsdf = products_urls.iloc[240:259,]

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
            if price_ini:
                price_final = round(float(str(price_ini[0]).strip('>€').replace(',','.')),2)

                #add the price in the list    
                prices_final_famoussports.append(price_final)
            else:
                prices_final_famoussports.append(None)
            
        except urllib.error.HTTPError as err:
            prices_final_famoussports.append('NaN')

#columns urls,products,labels into lists
urls = famoussportsdf['item.url'].values.tolist()
products = famoussportsdf['item.name'].values.tolist()
labels = famoussportsdf['item.subclass'].values.tolist()

#scrape the prices
scrapper_famoussports(urls)

#put the rows in a list
all_items_famoussports = []
for product,price,label in zip(products,prices_final_famoussports,labels):
    all_items_famoussports.append([product,price,datetime.now(),label,'FamousSports'])

#assign the values to each column
for i in range(len(all_items_famoussports)):
    df.loc[len(df)] = (all_items_famoussports[i][0],all_items_famoussports[i][1],all_items_famoussports[i][2],all_items_famoussports[i][3],all_items_famoussports[i][4],0)

# #STRADIVARIOUS NEW CODE
# urls = ["https://www.stradivarius.com/cy/buttoned-blazer-l01918531?colorId=004",
#         "https://www.stradivarius.com/cy/vneck-polyamide-bodysuit-l07003151?colorId=001",
#         "https://www.stradivarius.com/cy/striped-cotton-tshirt-l06501502?colorId=001&categoryId=1020047036",
#         "https://www.stradivarius.com/cy/smart-straightleg-trousers-l04562485?colorId=001&categoryId=1020047051",
#         "https://www.stradivarius.com/cy/minimalist-trousers-with-pockets-l01477778?colorId=430&categoryId=1020047051"]

# prices_stradivarious= []

# def scrapper_stradivarious(urls:list):
#     for url in urls:
#         try:
#             #used for the request, urlopen functions
#             user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
#             headers={'User-Agent':user_agent} 

#             #initial price list and the value of the final price scrapped
#             price_ini=[]
                
#             #open and read the different urls
#             request=urllib.request.Request(url,headers=headers) 
#             response = urllib.request.urlopen(request)
#             data = response.read().decode("utf-8")

#             #get the strings for the prices of the products using regular expressions
#             pattern = '\<meta content=.*€'
#             price_ini = re.findall(pattern,data)
#             price_ini = re.sub(r'[^0-9.]', '', price_ini[0])

#             prices_stradivarious.append(float(price_ini))

#         except urllib.error.HTTPError as err:
#             prices_stradivarious.append('NaN')

# #columns urls,products,labels into lists
# products = ['BUTTONED BLAZER','VNECK POLYAMIDE BODYSUIT','STRIPPED COTTON TSHIRT','SMART STRAIGHT LEG TROUSERS','MINIMALIST TROUSERS WITH POCKETS']

# #scrap the prices
# scrapper_stradivarious(urls)

# #put the rows in a list
# all_items_stradivarious = []
# for product,price in zip(products,prices_stradivarious):
#     all_items_stradivarious.append([product,price,datetime.now(),'Garments for women','Stradivarious'])

# #assign the values to each column
# for i in range(len(all_items_stradivarious)):
#     df.loc[len(df)] = (all_items_stradivarious[i][0],all_items_stradivarious[i][1],all_items_stradivarious[i][2],all_items_stradivarious[i][3],all_items_stradivarious[i][4],0)

#BERSHKA/STRADIVARIOUS
# def garments():
#     headers = {'User-agent': 'Mozilla/5.0'}  
#     data_garmets = pd.read_csv("Garmets.csv")
#     for index, am in data_garmets.iterrows():
#         page = requests.get(am['website'].strip(),headers=headers)
#         st=page.content.decode('utf-8')
#         tree = html.fromstring(st)
#         product_name = (''.join(am['product_name'])).replace(' ','').strip()
#         try:
#             pp=tree.xpath("//script[@type='application/ld+json']/text()")
#             product_price=pp[0]
#             if am['retailer'] == 'Bershka':
#                 if product_price:
#                     product_price = json.loads(product_price)['offers'][0]['price']
#                 else:
#                     product_price=None
#             else:
#                 if product_price:
#                     product_price = json.loads(product_price)['offers']['price']
#                 else:
#                     product_price = None
#             print(product_price)
#             now = datetime.now()
#             date_time_scraped = now
#             product_subclass=am['product_subclass']
#             retailer= am['retailer']
#             df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
#         except IndexError:
#             print("Index Error")

# garments()

#NOVELLA HAIR SALON
def Novella():
    prices_final_hairsalon = []
    url_new = 'https://novella.com.cy/#services'
    page = urlopen(url_new)
    html = page.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")

    scripts = bs.find_all('td',{'class':'column-2'},string=True)
    price_ini = re.findall(r'\€\d+,\d\d',str(scripts))

    if len(price_ini)>0:
        prices_final_hairsalon.append(round(float(str(price_ini[0]).strip('€').replace(',','.')),2))
    else:
        prices_final_hairsalon.append(None)
    if len(price_ini)>4:
        prices_final_hairsalon.append(round(float(str(price_ini[4]).strip('€').replace(',','.')),2))
    else:
        prices_final_hairsalon.append(None)

    #################################################################################################################

    df.loc[len(df)] = ("Women's Services, HAIRCUT Stylist",prices_final_hairsalon[0],datetime.now(),'Hairdressing for women','Novella Hair Salon',0)
    df.loc[len(df)] = ("Men's Services, HAIRCUT Stylist",prices_final_hairsalon[1],datetime.now(),'Hairdressing for men','Novella Hair Salon',0)

Novella()

#CYPRUS POST
def CyPost():
    file = 'https://www.cypruspost.post/uploads/2cf9ec4f5a.pdf'
    table_1 = tb.read_pdf(file, pages = '6',pandas_options={'header': None}, stream=True)
    table_2 = tb.read_pdf(file, pages = '11',pandas_options={'header': None}, stream=True)

    df_package_1 = table_1[0]
    df_package_2 = table_2[0]

    #change the type of columns that contain the prices
    df_package_1[2]=df_package_1[2].astype('string')
    df_package_2[1]=df_package_2[1].astype('string')

    all_items_post = [("ΤΕΛΗ ΜΕΜΟΝΩΜΕΝΩΝ ΤΑΧΥΔΡΟΜΙΚΩΝ ΑΝΤΙΚΕΙΜΕΝΩΝ (ΕΠΙΣΤΟΛΙΚΟΥ ΤΑΧΥΔΡΟΜΕΙΟΥ) ΕΣΩΤΕΡΙΚΟΥ Α' ΠΡΟΤΕΡΑΙΟΤΗΤΑΣ Μικρά (P) 50 γρ.",round(float(df_package_1[2][14].split(' ')[0].replace(',','.')),2),datetime.now(),'Letter handling services','Cyprus Post',0),
                    ("ΤΕΛΗ ΜΕΜΟΝΩΜΕΝΩΝ ΤΑΧΥΔΡΟΜΙΚΩΝ ΑΝΤΙΚΕΙΜΕΝΩΝ (ΕΠΙΣΤΟΛΙΚΟΥ ΤΑΧΥΔΡΟΜΕΙΟΥ) ΕΣΩΤΕΡΙΚΟΥ Α' ΠΡΟΤΕΡΑΙΟΤΗΤΑΣ Μεγάλα (G) 500 γρ.",round(float(df_package_1[2][21].split(' ')[0].replace(',','.')),2),datetime.now(),'Letter handling services','Cyprus Post',0),
                    ("ΤΕΛΗ ΜΕΜΟΝΩΜΕΝΩΝ ΤΑΧΥΔΡΟΜΙΚΩΝ ΑΝΤΙΚΕΙΜΕΝΩΝ (ΕΠΙΣΤΟΛΙΚΟΥ ΤΑΧΥΔΡΟΜΕΙΟΥ) ΕΣΩΤΕΡΙΚΟΥ Α' ΠΡΟΤΕΡΑΙΟΤΗΤΑΣ Ακανόνιστα (E) 2000 γρ.",round(float(df_package_1[2][44].split(' ')[0].replace(',','.')),2),datetime.now(),'Letter handling services','Cyprus Post',0),
                    ("ΤΕΛΗ ΥΠΗΡΕΣΙΑΣ ΔΕΜΑΤΩΝ ΕΣΩΤΕΡΙΚΟΥ 0.5 κιλό",round(float(df_package_2[1][2].replace(',','.')),2),datetime.now(),'Other postal services','Cyprus Post',0),
                    ("ΤΕΛΗ ΥΠΗΡΕΣΙΑΣ ΔΕΜΑΤΩΝ ΕΣΩΤΕΡΙΚΟΥ 15 κιλά",round(float(df_package_2[1][17].replace(',','.')),2),datetime.now(),'Other postal services','Cyprus Post',0),
                    ("ΤΕΛΗ ΥΠΗΡΕΣΙΑΣ ΔΕΜΑΤΩΝ ΕΣΩΤΕΡΙΚΟΥ 30 κιλά",round(float(df_package_2[1][32].replace(',','.')),2),datetime.now(),'Other postal services','Cyprus Post',0) ]

    for i in range(6):
        df.loc[len(df)] = all_items_post[i]

CyPost()

def CyMinistryEducation():
    
    #The fees are found in the following link :
    #http://www.moec.gov.cy/idiotiki_ekpaidefsi/didaktra.html 
    
    try:
        pdf_1_1 = tb.read_pdf('http://archeia.moec.gov.cy/mc/698/didaktra_idiotikon_mesi_ekpaidefsi.pdf', pages = '1', pandas_options={'header': None}, stream=True)
        pdf_1_2 = tb.read_pdf('http://archeia.moec.gov.cy/mc/698/didaktra_idiotikon_mesi_ekpaidefsi.pdf', pages = '2', pandas_options={'header': None}, stream=True)
        pdf_2 = tb.read_pdf('http://archeia.moec.gov.cy/mc/698/didaktra_idiotikon_dimotikon_scholeion.pdf', pages = '1', pandas_options={'header': None}, stream=True)
        pdf_3 = tb.read_pdf('http://archeia.moec.gov.cy/mc/698/didaktra_idiotikon_nipiagogeion.pdf', pages = '4', pandas_options={'header': None}, stream=True)

        df_secondary_1 = pdf_1_1[0]
        df_secondary_2 = pdf_1_2[0]
        df_primary = pdf_2[0]
        df_nursery = pdf_3[0]
        # print(df_nursery[2].astype('string'))

        #change the type of columns that contain the prices
        df_nursery[3] = df_nursery[3].astype('string')
        df_primary[2] = df_primary[2].astype('string')
        
        for i in range(2,7):
            df_secondary_1[i]= df_secondary_1[i].astype('string')
            df_secondary_2[i]= df_secondary_2[i].astype('string')
            
            #Nicosia
            value_1=(float(df_secondary_1[2][4].replace("€",'').replace(".","")))
            value_2=(float(df_secondary_1[3][4].replace("€",'').replace(".","")))
            value_3=(float(df_secondary_1[4][4].replace("€",'').replace(".","")))
            value_4=(float(df_secondary_1[5][4].replace("€",'').replace(".","")))
            value_5=(float(df_secondary_1[6][4].replace("€",'').replace(".","")))
            value_6=(float(df_secondary_1[7][4].replace("€",'').replace(".","")))

            #Limassol
            value_7=(float(df_secondary_2[2][15].replace("€",'').replace(".","")))
            value_8=(float(df_secondary_2[3][15].replace("€",'').replace(".","")))
            value_9=(float(df_secondary_2[4][15].replace("€",'').replace(".","")))
            value_10=(float(df_secondary_2[5][15].replace("€",'').replace(".","")))
            value_11=(float(df_secondary_2[6][15].replace("€",'').replace(".","")))
            value_12=(float(df_secondary_2[7][15].replace("€",'').replace(".","")))
            
            avg_grammar_nic = ( value_1 + value_2 + value_3 + value_4 + value_5 + value_6 ) / 6
            
            avg_grammar_lim = ( value_7 + value_8 + value_9 + value_10 + value_11 + value_12 ) / 6
        
        all_items_school = [("THE GRAMMAR JUNIOR SCHOOL (Nicosia), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΝΗΠΙΑΓΩΓΕΙΩΝ 2024-2025",float(df_nursery[3][1].replace("€","").replace(".","")),datetime.now(),'Pre-primary education (ISCED-97 level 0)','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR JUNIOR SCHOOL (Nicosia), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΔΗΜΟΤΙΚΩΝ ΣΧΟΛΕΙΩΝ 2024-2025",float(df_primary[2][25].replace("€","").replace(".","")),datetime.now(),'Primary education (ISCED-97 level 1)','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR SCHOOL (Nicosia), ΜΕΣΑ ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2024-2025,Α-ΣΤ ΤΑΞΗ",avg_grammar_nic,datetime.now(),'Secondary education','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR SCHOOL (Limassol), ΜΕΣΑ ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2024-2025,Α-ΣΤ ΤΑΞΗ",avg_grammar_lim,datetime.now(),'Secondary education','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR SCHOOL (Nicosia), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2024-2025, Ζ ΤΑΞΗ",float(df_secondary_1[8][4].replace("€","").replace(".","")),datetime.now(),'Post-secondary non-tertiary education (ISCED 4)','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR SCHOOL (Limassol), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2024-2025, Ζ ΤΑΞΗ",float(df_secondary_2[8][15].replace("€","").replace(".","")),datetime.now(),'Post-secondary non-tertiary education (ISCED 4)','Cyprus Ministry of Education, Sport and Youth',0) ]
    
    except urllib.error.URLError:
        
        all_items_school = [("THE GRAMMAR JUNIOR SCHOOL (Nicosia), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΝΗΠΙΑΓΩΓΕΙΩΝ 2024-2025",None,datetime.now(),'Pre-primary education (ISCED-97 level 0)','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR JUNIOR SCHOOL (Nicosia), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΔΗΜΟΤΙΚΩΝ ΣΧΟΛΕΙΩΝ 2024-2025",None,datetime.now(),'Primary education (ISCED-97 level 1)','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR SCHOOL (Nicosia), ΜΕΣΑ ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2024-2025, Α-ΣΤ ΤΑΞΗ",None,datetime.now(),'Secondary education','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR SCHOOL (Limassol), ΜΕΣΑ ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2024-2025, Α-ΣΤ ΤΑΞΗ",None,datetime.now(),'Secondary education','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR SCHOOL (Nicosia), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2024-2025, Ζ ΤΑΞΗ",None,datetime.now(),'Post-secondary non-tertiary education (ISCED 4)','Cyprus Ministry of Education, Sport and Youth',0),
                        ("THE GRAMMAR SCHOOL (Limassol), ΕΤΗΣΙΑ ΔΙΔΑΚΤΡΑ ΙΔΙΩΤΙΚΩΝ ΣΧΟΛΕΙΩΝ ΜΕΣΗΣ ΕΚΠΑΙΔΕΥΣΗΣ 2024-2025, Ζ ΤΑΞΗ",None,datetime.now(),'Post-secondary non-tertiary education (ISCED 4)','Cyprus Ministry of Education, Sport and Youth',0) ]
    
    for i in range(6):
        df.loc[len(df)] =  all_items_school[i]

CyMinistryEducation()

# Read the csv file with the products
fueldaddydf = pd.read_excel('03.Based_list.xlsx')

# Transform the column of the urls into list
urls_fueldaddy = fueldaddydf['WebLine'].values.tolist()

# Function for fuels from Fuel Daddy
def results_fuelDaddy(urls:list):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}

    for url in urls:
        # Build the complete URL for the current route
        url_fueldaddy = "https://www.fueldaddy.com.cy/en/" + str(url)
        bs = BeautifulSoup(url_fueldaddy, "html.parser")
        
        # Send a GET request to the URL
        response = requests.get(bs, {'headers':header})
        
        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Read the price of the company
        element_price = soup.find_all("div", {"class":"price-item"})
        
        # Read the name of the company
        element_name = soup.find_all("span", {"class":"brand-title"})
        element_name_str = str(element_name)

        # Extract the company name using regular expressions
        company_name_w = re.search(r'>([^<]+)<', element_name_str)
        if company_name_w:
            company_name = company_name_w.group(1).strip()
        else:
            company_name = None
        
        # Read the name of retailer
        brand_names = soup.find_all("div", {"class":"col-md-7 pump-info-right"})
        for brand_name in brand_names:
            brand = brand_name.find_all(class_ = "col-sm-9")[1]
            for brand_name in brand:
                brand_word = brand_name.get_text(strip = True)
            
        # Scrapping the price
        new_row = []
        for i in range(len(element_price)):
            new_row = []
            name = element_price[i].find(class_ = "brandtag cut-text fueltype-heading").get_text(strip = True)
            new_row.append(name + " - " + company_name)
            price = element_price[i].find(class_ = "pricetag").get_text(strip = True).replace(" €","")
            new_row.append(float(price))
            new_row.append(datetime.now())
            if (name[0] == "H") or (name[0] == "K"):
                item_subclass = ("liquid fuels")
            elif(name[0] == "U"):
                item_subclass = ("petrol")
            elif(name[0] == "D"):
                item_subclass = ("diesel")
            new_row.append(item_subclass)
            new_row.append(brand_word)
            new_row.append(0)
            df.loc[len(df)] = new_row

    #df['product_name'] = df['product_name'].apply(lambda x:x)
    
results_fuelDaddy(urls_fueldaddy)

#GLOBAL PETROL PRICES
#def Fuel():
#    #https://eforms.eservices.cyprus.gov.cy/MCIT/MCIT/PetroleumPrices
#    #alternative: https://gr.globalpetrolprices.com/Cyprus/

#    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
#    headers={'User-Agent':user_agent} 

#    prices_final_petrol = []
#    url = 'https://gr.globalpetrolprices.com/Cyprus/'        

#    #open and read the different urls
#    url_new = url
#    request=urllib.request.Request(url,headers=headers) 
#    response = urllib.request.urlopen(request)
#    data = response.read().decode("utf-8")
#    data

#    pattern = '\d\.\d+\s'
#    price_ini = re.findall(pattern,data)

#    if len(price_ini)>3:
#         df.loc[len(df)] = ("Αμόλυβδη Μέση Τιμή Παγκύπρια",price_ini[3],datetime.now(),'Petrol','Global Petrol Prices',0)
#    if len(price_ini)>6:
#        df.loc[len(df)] = ("Πετρέλαιο Κίνησης Μέση Τιμή Παγκύπρια",price_ini[6],datetime.now(),'Diesel','Global Petrol Prices',0)
#    if len(price_ini)>9:
#        df.loc[len(df)] =  ("Πετρέλαιο Μέση Τιμή Παγκύπρια",price_ini[9],datetime.now(),'Liquid Fuels','Global Petrol Prices',0)
#    if len(price_ini)>12:
#        df.loc[len(df)] = ("Πετρέλαιο Θέρμανσης Μέση Τιμή Παγκύπρια",price_ini[12],datetime.now(),'Liquid Fuels','Global Petrol Prices',0)

#Fuel()

def Tobacco():
    
    prices_final_cigars=[]

    url = "https://www.thecygarshop.com/product-page/machetero-petit-corona" #"https://www.thecygarshop.com/product-page/machetero-panatela"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
        
    scripts = bs.find_all('span',{'data-hook':'formatted-primary-price'},string=True)

    if scripts:
        price_ini = re.findall(r"\d.\d\d",str(scripts))
        #get only the first element
        price_final = float(str(price_ini[0]).replace(',','.'))

        #add the price in the list    
        prices_final_cigars.append(price_final)
    else:
        prices_final_cigars.append(None)
    
    url = "https://www.numbeo.com/cost-of-living/country_price_rankings?itemId=17&displayCurrency=EUR"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
        
    scripts = bs.find_all('script',string=True)
    price_ini = re.findall(r"\['Cyprus', \d.+\]",str(scripts))
    #get only the first element
    if price_ini:
        price_final = float(str(price_ini[0]).strip("['Cyprus', ]"))

        #add the price in the list    
        prices_final_cigars.append(price_final)
    else:
        prices_final_cigars.append(None)
        
    url = "https://www.ewsale.com/product-page/aspire-puxos-kit-%CE%B7%CE%BB%CE%B5%CE%BA%CF%84%CF%81%CE%BF%CE%BD%CE%B9%CE%BA%CE%AC-%CF%84%CF%83%CE%B9%CE%B3%CE%AC%CF%81%CE%B1-%CE%BC%CF%80%CE%B1%CF%84%CE%B1%CF%81%CE%AF%CE%B1-21700-200-ml-%CF%85%CE%B3%CF%81%CE%AC-%CE%AC%CF%84%CE%BC%CE%B9"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    bs = BeautifulSoup(html, "html.parser")
        
    scripts = bs.find_all('span',{'data-hook':'formatted-primary-price'},string=True)
    if scripts:
        price_ini = re.findall(r"\d\d.\d\d",str(scripts))
        #get only the first element
        price_final = float(str(price_ini[0]).replace(',','.'))

        #add the price in the list    
        prices_final_cigars.append(price_final)
    else:
        #add the price in the list    
        prices_final_cigars.append(None)

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent} 
    urls = ['https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos/item/496756/Rocky%20Patel%20Sixty%20Toro',
        'https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos/item/496759/Rocky%20Patel%20TUBO%20SAMPLER%206%20cig.',
        'https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos/item/511874/Perdomo%2010th%20Anniversary%20MADURO%20Super%20Toro',
        'https://fetch.com.cy/shop/stores/Nicosia/store/222/The%20Royal%20Cigars%20%7C%20Strovolos/item/280001/CARRILLO%20INTERLUDE%20ROTHCHILD%20JR%20MADURO%20NATURAL']

    for url in urls:
        try:
            page = urlopen(url)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
                    
            scripts = bs.find_all('div',{'class':"itemDetailsPrice"},string=True)
            if scripts: 
                #get the strings for the prices of the products using regular expressions
                pattern = '\d+.\d+'
                price_ini = re.findall(pattern,str(scripts[0]))
                
                #get only the first element
                price_final = float(price_ini[1])

                #add the price in the list    
                prices_final_cigars.append(price_final)
            else:
                prices_final_cigars.append(None)
            
        except urllib.error.HTTPError as err:
                prices_final_cigars.append('NaN')
    
    urls = ['https://altervape.eu/collections/eliquids/products/manhattan','https://altervape.eu/collections/eliquids/products/cabochard-vanille-caramel-0mg-50ml',
        'https://altervape.eu/collections/eliquids/products/manhattan-shake']
    
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
            pattern = '<meta property="product:price:amount" content="\d+.\d+">'
            price_ini = re.findall(pattern,data)
            if price_ini:
                prices_final_cigars.append(float(str(price_ini[0]).strip('<meta property="product:price:amount" content=" " />').replace(',', '.')))
            else:
                prices_final_cigars.append(None)

        except urllib.error.HTTPError as err:
                prices_final_cigars.append('NaN')

            #columns urls,products,labels into lists
        products = ['Machetero Panatela','Marlboro 20 Pack','Smok S-priv Kit E-Τσιγάρα + 2 μπαταρίες  + 200 ml Υγρά  άτμισης','Rocky Patel Sixty Toro',
                    'Rocky Patel Tubo Sampler 6 Cig.','Perdomo 10Th Anniversary Maduro Super Toro','Carrillo Interlude Rothchild Jr. Maduro Natural',
                    'E-liquid Manhattan','E-liquid Cabochard - Vanille Caramel 0mg 50ml','E-liquid Manhattan Shake']
        labels = ['Cigars','Cigarettes','Other Tobaco Products','Cigars','Cigars','Cigars','Cigars','Other Tobaco Products','Other Tobaco Products','Other Tobaco Products']
        retailers = ['The CYgar Shop','NUMBEO','E-WHOLESALE','The Royal Cigars Strovolos','The Royal Cigars Strovolos','The Royal Cigars Strovolos',
                    'The Royal Cigars Strovolos','Alter Vape','Alter Vape','Alter Vape']
    #put the rows in a list
    all_items_cigars = []
    for product,price,label,retailer in zip(products,prices_final_cigars,labels,retailers):
        all_items_cigars.append([product,price,datetime.now(),label,retailer,0])

    #assign the values to each column
    for i in range(len(all_items_cigars)):
        df.loc[len(df)] =(all_items_cigars[i][0],all_items_cigars[i][1],all_items_cigars[i][2],all_items_cigars[i][3],all_items_cigars[i][4],all_items_cigars[i][5])
Tobacco()

#STEPHANIS
def Stephanis():

    #for the different urls, putting the prices in a list
    prices_final_stephanis = []
    stephanisdf = products_urls.iloc[298:338,]
    
    #columns urls,products,labels into lists
    urls = stephanisdf['item.url'].values.tolist()
    products = stephanisdf['item.name'].values.tolist()
    labels = stephanisdf['item.subclass'].values.tolist()
    url_stephanis = "https://www.stephanis.com.cy/en"
    for url in urls:
        try:
            url_new = url_stephanis+url
            page = urlopen(url_new)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
    
            scripts = bs.find_all('span',{'class':'item-price'},string=True)
            #get only the first element
            if scripts:
                price_final = float(str(scripts[0]).strip('<span class="item-price">€ </span>'))

                #add the price in the list    
                prices_final_stephanis.append(price_final)
            else:
                scripts = bs.find_all('div',{'class':'listing-details-heading large-now-price with-sale'})
                if scripts:
                    price_final = float(str(scripts[0]).strip('<div class="listing-details-heading large-now-price with-sale">€ </div>'))
                    prices_final_stephanis.append(price_final)
                else: 
                    prices_final_stephanis.append(None)
            
        except urllib.error.HTTPError as err:
            prices_final_stephanis.append('NaN')
    for i in range(len(products)):
        df.loc[len(df)]=(products[i],prices_final_stephanis[i],datetime.now(),labels[i],'Stephanis',0)

Stephanis()


#ELECTROLINE
def Electroline():
    urls = ["https://electroline.com.cy/products/garden/garden-power-tools/%ce%b1%ce%bb%cf%85%cf%83%ce%bf%cf%80%cf%81%ce%af%ce%bf%ce%bd%ce%b1/oregon-cs1200-electric-chainsaw-1800w/",
        "https://electroline.com.cy/products/tools/hand-tools-2/screwdrivers/kapriol-kap33533-set-screwdrivers-6pcs/",
        "https://electroline.com.cy/products/tools/hand-tools-2/hand-tools-set/total-tot-thkthp21176-hand-tools-set-117-pieces/"]

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
                    if price_ini:
                        prices_final_electroline.append(float(str(price_ini[0]).strip('<meta property="product:price:amount" content=" " />')))
                    else:
                        prices_final_electroline.append(None)

            except urllib.error.HTTPError as err:
                prices_final_electroline.append('NaN')

            #columns urls,products,labels into lists
    products = ['WORX 30091701000 Ηλεκτρικό Aλυσοπρίονο','TACTIX MER-205604 Σετ Kατσαβίδια, 12 Tεμάχια','TOTAL TOT-THKTHP21176 Σετ Εργαλεία Χειρός 117 Τεμάχια']
    labels = ['Motorized major tools and equipment','Non-motorized small tools','Miscellaneous small tool accessories']

    #put the rows in a list
    all_items_electroline = []
    for product,price,label in zip(products,prices_final_electroline,labels):
        all_items_electroline.append([product,price,datetime.now(),label,'Electroline',0])

    #assign the values to each column
    for i in range(len(all_items_electroline)):
        df.loc[len(df)] = (all_items_electroline[i][0],all_items_electroline[i][1],all_items_electroline[i][2],all_items_electroline[i][3],all_items_electroline[i][4],all_items_electroline[i][5])
Electroline()                  

#IKEA
def ikea():
    ikeadf = products_urls.iloc[338:367,]
    prices_final_ikea = []
    url_ikea = "https://www.ikea.com.cy"
    #columns urls,products,labels into lists
    urls = ikeadf['item.url'].values.tolist()
    products = ikeadf['item.name'].values.tolist()
    labels = ikeadf['item.subclass'].values.tolist()
    division = ikeadf['item.division'].values.tolist()

    for url in urls:
        try:
            url_new = url_ikea+url
            page = urlopen(url_new)
            html = page.read().decode("utf-8")
            bs = BeautifulSoup(html, "html.parser")
    
            scripts = bs.find_all('script',string=True)

            #get the strings for the prices of the products using regular expressions
            price_ini = re.findall(r'"fb_value": "\d+.\d+"',str(scripts))
            if price_ini:
                #add the price in the list    
                prices_final_ikea.append(float(price_ini[0].strip('"fb_value": " "')))
            else:
                prices_final_ikea.append(None)
            
        except urllib.error.HTTPError as err:
            prices_final_ikea.append('NaN')

        except urllib.error.URLError:
            prices_final_ikea.append('NaN')

        except IndexError:
            prices_final_ikea.append('NaN')

    for i in range(len(products)):
        df.loc[len(df)]= (products[i],prices_final_ikea[i],datetime.now(),labels[i],'IKEA',0)

ikea()

#AWOL
def awol():
    awoldf = products_urls.iloc[276:284,]
    urls = awoldf['item.url'].values.tolist()
    products = awoldf['item.name'].values.tolist()
    labels = awoldf['item.subclass'].values.tolist()
    division = awoldf['item.division'].values.tolist()
    #the scrapper function
    prices_final_awol = []
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
            if price_ini:
                prices_final_awol.append(float(str(price_ini[0]).strip('<meta property="og:price:amount" content=" " >').replace(',','.')))
            else:
                prices_final_awol.append(None)
            
        except urllib.error.HTTPError as err:
            prices_final_awol.append('NaN')
    #create the dataframe
    for i in range(len(products)):
        df.loc[len(df)] = (products[i],prices_final_awol[i],datetime.now(),labels[i],'AWOL',0)
awol()

#MOTORACE
def moto_race():
    motoracedf = products_urls.iloc[284:298,]
    #the scrapper function
    prices_final_motorace = []
    #columns urls,products,labels into lists
    urls = motoracedf['item.url'].values.tolist()
    products = motoracedf['item.name'].values.tolist()
    labels = motoracedf['item.subclass'].values.tolist()
    division = motoracedf['item.division'].values.tolist()
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
            if scripts:
                price_final = float(str(scripts[0]).strip('<span class="price">€ </span>').replace(',',''))

                #add the price in the list    
                prices_final_motorace.append(price_final)
            else:
                prices_final_motorace.append(None)
            
        except urllib.error.HTTPError as err:
            prices_final_motorace.append('NaN')
    for i in range(len(products)):
        df.loc[len(df)] = (products[i],prices_final_motorace[i],datetime.now(),labels[i],'MotoRace',0)
moto_race()

#BWELL PHARMACY
def bwell():
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
        if len(price_ini)>1:

            prices_final_bwell.append(float(str(price_ini[1]).strip('</span>&nbsp; </bdi>')))
        else:
            prices_final_bwell.append(None)
    #columns urls,products,labels into lists
    products = ['Physiomer Nasal Spray Hygiene Active Prevention 135ml','Vitabiotics Pregnacare Original 30 tabs','Geatherm Oxy Control – Pulse Oximeter',
    'Flaem RespirAir nebulizer']
    labels = ['Pharmaceutical products','Pregnancy tests and mechanical contraceptive devices','Other medical products n.e.c.','Other therapeutic appliances and equipment']

    #put the rows in a list
    all_items_bwell = []
    for product,price,label in zip(products,prices_final_bwell,labels):
        all_items_bwell.append([product,price,datetime.now(),label,'Bwell Pharmacy',0])

    #assign the values to each column
    for i in range(len(all_items_bwell)):
        df.loc[len(df)] = (all_items_bwell[i][0],all_items_bwell[i][1],all_items_bwell[i][2],all_items_bwell[i][3],all_items_bwell[i][4],all_items_bwell[i][5])

bwell()

#MAZDA
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
    date_time_scraped = now
    product_name="New Mazda 2"
    product_subclass="New motor cars"
    retailer="Mazda"
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    pdf_file.close()
mazda()

#NISSAN
def nissan():
        # Define the URL for the Booking.com page for hotel X
    url = "https://www.nissan.com.cy/vehicles/new-vehicles/juke-2022/prices-specifications.html#-"

    # Define the headers for the HTTP request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)
    tree = html.fromstring(response.content)
    # Use XPath to extract the price value
    price_tree = tree.xpath('//iframe[@id="individualVehiclePriceJSON"]/text()')
    if price_tree:
        price_json = price_tree[0]

        # Extract the price of 23500 from the JSON string
        import json
        price_data = json.loads(price_json)
        product_price = price_data['juke_2019']['default']['grades']['LVL001']['gradePrice']
    else:
        product_price=None
    now = datetime.now()
    date_time_scraped = now
    product_name="Nissan Juke"
    product_subclass="New motor cars"
    retailer="Nissan"
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
nissan()

# #WOLT
# def Wolt():
#     retailer="Wolt"
#     product_subclass="Restaurants, cafes and dancing establishments"
#     # Define the URL for the Booking.com page for hotel X
#     url = "https://wolt.com/en/cyp/nicosia/restaurant/costanicosia"

#     # Define the headers for the HTTP request
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#     url = 'https://wolt.com/en/cyp/nicosia/restaurant/costanicosia'
#     response = requests.get(url)
#     html_content = response.text

#     tree = etree.HTML(html_content)

#     # Find the button element containing the cappuccino information
#     button_xpath = tree.xpath('//button[descendant::h3[text()="Cappuccino"]]')
#     if button_xpath:
#         button_element = button_xpath[0]

#         # Extract the price from the button element
#         price_xpath_cappuccino = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#         if button_element.xpath(price_xpath_cappuccino):
#             product_price = float(button_element.xpath(price_xpath_cappuccino)[0].replace('€', ''))
#     else:
#         product_price=None

#     product_name="Costa Coffee Cappuccino Medio"
#     now = datetime.now()
#     date_time_scraped = now
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


#     # Find the button element containing the cappuccino information
#     product_name="Costa Coffee Espresso Single"
#     now = datetime.now()
#     date_time_scraped = now
#     button_xpath = '//button[descendant::h3[text()="Espresso"]]'
#     button_element= tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_espresso = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_espresso)[0].replace('€', ''))

#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#     product_name="Costa Coffee Freddo Cappuccino Medio"
#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Freddo Cappuccino"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_fcappuccino = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_fcappuccino)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#     product_name="Costa Coffee Freddo Espresso Medio"
#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Freddo Espresso"]]'
#     button_element= tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_fespresso = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     price_fespresso = float(button_element.xpath(price_xpath_fespresso)[0].replace('€', ''))
#     product_price = float(button_element.xpath(price_xpath_fcappuccino)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#     ###PIATSA GOUROUNAKI

#     product_name="Piatsa Gourounaki, Meat platter for 2 persons  (Nicosia)"
#     url = 'https://wolt.com/en/cyp/nicosia/restaurant/piatsa-gourounaki-mall-of-egkomi'
#     response = requests.get(url)
#     html_content = response.text

#     tree = etree.HTML(html_content)

#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Ποικιλία Κρεάτων Για Δυο"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_pk2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_pk2)[0].replace('€', ''))

#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#     ####PIXIDA  
#     # Define the URL for the Booking.com page for hotel X
#     product_name="Pixida, Fish meze for each guest with minimum 2 guests (Nicosia)"
#     url = 'https://wolt.com/en/cyp/nicosia/restaurant/pyxida'
#     response = requests.get(url)
#     html_content = response.text

#     tree = etree.HTML(html_content)

#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Meze Platter for 2"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_mp2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_mp2)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


#     ###LIMASSOL
#     product_name="Kofini Tavern Mix Grill for 2"
#     url = 'https://wolt.com/en/cyp/limassol/restaurant/kofini-tavern#mix-grills-platters-6'
#     response = requests.get(url)
#     html_content = response.text

#     tree = etree.HTML(html_content)

#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Mix Grill For 2"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_mg2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_mg2)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#     product_name="Kofini Tavern, Seafood Platter"
#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Seafood Platter"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_sfp = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price= float(button_element.xpath(price_xpath_sfp)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#     ## LARNACA VLACHOS
#     product_name="Vlachos Taverna, Ποικιλία Σχάρας Για 2 Άτομα"
#     url = 'https://wolt.com/en/cyp/larnaca/restaurant/vlachos-taverna#itemcategory-3'
#     response = requests.get(url)
#     html_content = response.text

#     tree = etree.HTML(html_content)

#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Ποικιλία Σχάρας Για 2 Άτομα"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_mg2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_mg2)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


#     ### Larnaca ZAKOS
#     product_name="Zakos Beach Restaurant, Ψαρομεζέδες Ζάκος (Για 2 Άτομα)"
#     url = 'https://wolt.com/en/cyp/larnaca/restaurant/zakos-beach-restaurant'
#     response = requests.get(url)
#     html_content = response.text

#     tree = etree.HTML(html_content)

#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Ψαρομεζέδες Ζάκος (Για 2 Άτομα)"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_psz2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_psz2)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


#     ### Paphos Tavernaki
#     product_name="Paphos Tavernaki, Ποικιλία Σχάρας Για 2 Άτομα"
#     url = 'https://wolt.com/en/cyp/paphos/restaurant/tavernaki-paphos#itemcategory-3'
#     response = requests.get(url)
#     html_content = response.text

#     tree = etree.HTML(html_content)

#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Ποικιλία Σχάρας Για 2 Άτομα"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_ps2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_ps2)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]


#     ### Paphos Ocean Basket
#     product_name="Ocean Basket, Platter for 2"
#     url = 'https://wolt.com/en/cyp/paphos/restaurant/ocean-basket-paphos'
#     response = requests.get(url)
#     html_content = response.text

#     tree = etree.HTML(html_content)

#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Platter For 2"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_p2 = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_p2)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#     product_subclass="Fast food and take away food services"

#     ###MACCIES

#     url = 'https://wolt.com/en/cyp/limassol/restaurant/mcdonalds-oldport'
#     response = requests.get(url)
#     html_content = response.text

#     tree = etree.HTML(html_content)

#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Share Box"]]'
#     button_element = tree.xpath(button_xpath)[0]
#     product_name="McDonald's Sharebox"
#     # Extract the price from the button element
#     price_xpath_sb = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_sb)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#     product_name="McDonald's Big Mac"
#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="Big Mac"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_bm = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_bm)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#     product_name="McDonald's McChicken"
#     # Find the button element containing the cappuccino information
#     button_xpath = '//button[descendant::h3[text()="McChicken"]]'
#     button_element = tree.xpath(button_xpath)[0]

#     # Extract the price from the button element
#     price_xpath_mc = './/span[@data-test-id="horizontal-item-card-price"]/text()'
#     product_price = float(button_element.xpath(price_xpath_mc)[0].replace('€', ''))
#     now = datetime.now()
#     date_time_scraped = now 
#     df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
# Wolt()


def Wolt():
    retailer = "Wolt"
    product_subclass = "Restaurants, cafes and dancing establishments"

    def handle_error(error):
        # Handle specific error cases
        if isinstance(error, (requests.ConnectionError, requests.Timeout)):
            # Connection errors
            print("Error: Connection error occurred.")
        elif isinstance(error, etree.XPathError):
            # XPath errors
            print("Error: Invalid XPath expression.")
        else:
            # Other errors
            print(f"Error: {str(error)}")

    def scrape_price(url, product_name, xpath, date_time_scraped):
        try:
            response = requests.get(url)
            html_content = response.text
            tree = etree.HTML(html_content)

            button_element = tree.xpath(xpath)[0]
            price_xpath = './/span[@data-test-id="horizontal-item-card-price"]/text()'
            product_price = float(button_element.xpath(price_xpath)[0].replace('€', ''))

            df.loc[len(df)] = [product_name, product_price, date_time_scraped, product_subclass, retailer, 0]
        except (IndexError, requests.RequestException, etree.XPathError) as error:
            handle_error(error)
            df.loc[len(df)] = [product_name, None, date_time_scraped, product_subclass, retailer, 0]

    # Costa Coffee
    now = datetime.now()
    date_time_scraped = now

    scrape_price('https://wolt.com/en/cyp/nicosia/restaurant/costanicosia',
                 "Costa Coffee Cappuccino Medio",
                 '//button[descendant::h3[text()="Cappuccino"]]',
                 date_time_scraped)

    scrape_price('https://wolt.com/en/cyp/nicosia/restaurant/costanicosia',
                 "Costa Coffee Espresso Single",
                 '//button[descendant::h3[text()="Espresso"]]',
                 date_time_scraped)

    scrape_price('https://wolt.com/en/cyp/nicosia/restaurant/costanicosia',
                 "Costa Coffee Freddo Cappuccino Medio",
                 '//button[descendant::h3[text()="Freddo Cappuccino"]]',
                 date_time_scraped)

    scrape_price('https://wolt.com/en/cyp/nicosia/restaurant/costanicosia',
                 "Costa Coffee Freddo Espresso Medio",
                 '//button[descendant::h3[text()="Freddo Espresso"]]',
                 date_time_scraped)

    # Piatsa Gourounaki
    scrape_price('https://wolt.com/en/cyp/nicosia/restaurant/piatsa-gourounaki-mall-of-egkomi',
                 "Piatsa Gourounaki, Meat platter for 2 persons (Nicosia)",
                 '//button[descendant::h3[text()="Ποικιλία Κρεάτων Για Δυο"]]',
                 date_time_scraped)

    # Pixida
    scrape_price('https://wolt.com/en/cyp/nicosia/restaurant/pyxida',
                 "Pixida, Meze Platter for 2",
                 '//button[descendant::h3[text()="Meze Platter for 2"]]',
                 date_time_scraped)
    
    # To ladolemono
    scrape_price('https://wolt.com/en/cyp/limassol/restaurant/to-ladolemono',
                 "Ποικιλία Για 2",
                 '//button[descendant::h3[text()="Ποικιλία Για 2"]]',
                 date_time_scraped)

    # Vlachos Taverna
    scrape_price('https://wolt.com/en/cyp/larnaca/restaurant/vlachos-taverna#itemcategory-3',
                 "Vlachos Taverna, Ποικιλία Σχάρας Για 2 Άτομα",
                 '//button[descendant::h3[text()="Ποικιλία Σχάρας Για 2 Άτομα"]]',
                 date_time_scraped)

    # Zakos Beach Restaurant
    scrape_price('https://wolt.com/en/cyp/larnaca/restaurant/zakos-beach-restaurant',
                 "Zakos Beach Restaurant, Ψαρομεζέδες Ζάκος (Για 2 Άτομα)",
                 '//button[descendant::h3[text()="Ψαρομεζέδες Ζάκος (Για 2 Άτομα)"]]',
                 date_time_scraped)

    # Paphos Tavernaki
    scrape_price('https://wolt.com/en/cyp/paphos/restaurant/tavernaki-paphos#itemcategory-3',
                 "Paphos Tavernaki, Ποικιλία Σχάρας Για 2 Άτομα",
                 '//button[descendant::h3[text()="Ποικιλία Σχάρας Για 2 Άτομα"]]',
                 date_time_scraped)

    # Paphos Ocean Basket
    scrape_price('https://wolt.com/en/cyp/paphos/restaurant/ocean-basket-paphos',
                 "Ocean Basket, Platter for 2",
                 '//button[descendant::h3[text()="Platter For 2"]]',
                 date_time_scraped)

    product_subclass = "Fast food and take away food services"

    # McDonald's
    scrape_price('https://wolt.com/en/cyp/limassol/restaurant/mcdonalds-oldport',
                 "McDonald's Sharebox",
                 '//button[descendant::h3[text()="Share Box"]]',
                 date_time_scraped)

    scrape_price('https://wolt.com/en/cyp/limassol/restaurant/mcdonalds-oldport',
                 "McDonald's Big Mac",
                 '//button[descendant::h3[text()="Big Mac"]]',
                 date_time_scraped)

    scrape_price('https://wolt.com/en/cyp/limassol/restaurant/mcdonalds-oldport',
                 "McDonald's McChicken",
                 '//button[descendant::h3[text()="McChicken"]]',
                 date_time_scraped) 

Wolt()


#PIZZA HUT
def PizzaHut():
    url = "https://www.pizzahut.com.cy/delivery-menu.pdf?v=1"  # Replace with the URL of the PDF file
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
    date_time_scraped = now 
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

#CERA
def cera():
    url = "https://www.cera.org.cy/Templates/00001/data/hlektrismos/kostos_xrisis.pdf"  # Replace with the URL of the PDF file
    response = requests.get(url)
    retailer="Cyprus Energy Regulatory Authority"
    product_subclass="Electricity"
    with open("file.pdf", "wb") as f:
        f.write(response.content)

    cdf = read_pdf("file.pdf",pages="all")[0]
    now = datetime.now()
    date_time_scraped = now 
    product_name="Καταναλωτές συνδεδεμένοι στο δίκτυο Χαμηλής Τάσης"
    product_price=cdf.loc[9][1]
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    product_name="Καταναλωτές συνδεδεμένοι στο δίκτυο Μέσης Τάσης"
    product_price=cdf.loc[9][2]
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
    product_name="Καταναλωτές συνδεδεμένοι στο δίκτυο Υψηλής Τάσης"
    product_price=float((cdf.loc[9][3]).replace(' ',''))
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

cera()

#WATER BOARD
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
    date_time_scraped = now 
    df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

water_board()


def sewage():
    url = "https://www.sbn.org.cy/el/apoxeteftika-teli"

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Send the HTTP request and get the HTML content of the page

    retailer="Sewerage Board of Nicosia"
    product_subclass="Sewage Collection"
    

    product_name="Sewerage Board of Nicosia, Ετήσιο Τέλος Αποχέτευσης 2022 (€ για κάθε €1000 εκτιμημένης αξίας)"
    now = datetime.now()
    date_time_scraped = now 
    try:
        response = requests.get(url, headers=headers)
        tree = html.fromstring(response.content)
        text_list=tree.xpath('(//li[@style="padding-left: 30px;"])[1]/strong/text()')
        text1 = "".join(text_list)
        text_list2=tree.xpath("//p[@style='padding-left: 30px;']/text()")
        text2 = "".join(text_list2)
        price_match = re.search(r'(\d+(?:,\d+)?)', text1)
        if price_match:
            product_price = float(price_match.group(1).replace(",", "."))
            # print(product_price)
            df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

        else:
            print("Price not found in text.")
            df.loc[len(df)] =[product_name,None,date_time_scraped,product_subclass,retailer,0]

        # Extract the price from the text using a regular expression
        product_name="Sewerage Board of Nicosia, Τέλος Χρήσης Αποχέτευσης (€ ανά κυβικό μέτρο καταναλισκόμενου νερού)"
        price_match = re.search(r'(\d+(?:,\d+)?)\s*(?:\w+\s*)?(ανά\s*κυβικό\s*μέτρο\s*καταναλισκόμενου\s*νερού)'
    , text2)

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
            date_time_scraped = now 
            # print(product_price)
            df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]
            
        else:
            print('No price found in text')
            df.loc[len(df)] =[product_name,None,date_time_scraped,product_subclass,retailer,0]
    except Exception as e:
        print()
        df.loc[len(df)] =['Sewerage Board of Nicosia, Ετήσιο Τέλος Αποχέτευσης 2022 (€ για κάθε €1000 εκτιμημένης αξίας)',product_price,date_time_scraped,product_subclass,retailer,0]
        df.loc[len(df)] =['Sewerage Board of Nicosia, Τέλος Χρήσης Αποχέτευσης (€ ανά κυβικό μέτρο καταναλισκόμενου νερού)',product_price,date_time_scraped,product_subclass,retailer,0]

sewage()

#WATERSEWAGE LARNACA AND LIMASSOL
def waterSewageOtherCities():

    url = "https://www.sbla.com.cy/Sewage-Charges"
    response = requests.get(url)

    tree = html.fromstring(response.content)
    name='Λεμεσος Phase 1 Sewage Costs '
    price=tree.xpath("//tbody/tr[last()]/td[4]/text()")
    if price:
        price=price[0].replace(".","") 
        price=price.replace(",",".") 
        df.loc[len(df)] =[name,price,datetime.now(),'Sewage collection','SBLA',0]
    else:
        df.loc[len(df)] =[name,None,datetime.now(),'Sewage collection','SBLA',0]
    name='Λεμεσος Phase 2 Sewage Costs '
    price=tree.xpath("//tbody/tr[last()]/td[7]/text()")
    if price:
        price=price[0].replace(".","") 
        price=price.replace(",",".")
        df.loc[len(df)] =[name,price,datetime.now(),'Sewage collection','SBLA',0]
    else:
        df.loc[len(df)] =[name,None,datetime.now(),'Sewage collection','SBLA',0]

    name='Λεμεσος Τέλη Αποχέτευσης Ομβρίων'
    price=tree.xpath("//tbody/tr[last()]/td[8]/text()")
    if price:
        price=price[0].replace(".","") 
        price=price.replace(",",".") 
        df.loc[len(df)] =[name,price,datetime.now(),'Sewage collection','SBLA',0]
    else:
        df.loc[len(df)] =[name,None,datetime.now(),'Sewage collection','SBLA',0]

    url = "https://www.lsdb.org.cy/ypiresies/oikonomika/apocheteftika-teli/"
    response = requests.get(url)
    tree = html.fromstring(response.content)

    name='Λαρνακα Phase 1 Sewage Costs '
    price=tree.xpath("//tbody/tr[last()-1]/td[3]/text()")
    if price:
        price=price[0].replace(".","") 
        price=price.replace(",",".") 
        df.loc[len(df)] =[name,price,datetime.now(),'Sewage collection','LSDB',0]
    else:
        df.loc[len(df)] =[name,None,datetime.now(),'Sewage collection','LSDB',0]
    name='Λαρνακα Phase 2 Sewage Costs '
    price=tree.xpath("//tbody/tr[last()-1]/td[5]/text()")
    if price:
        price=price[0].replace(".","") 
        price=price.replace(",",".")
        df.loc[len(df)] =[name,price,datetime.now(),'Sewage collection','LSDB',0]
    else:
        df.loc[len(df)] =[name,None,datetime.now(),'Sewage collection','LSDB',0]
    name='Λαρνακα Τέλη Αποχέτευσης Ομβρίων'
    price=tree.xpath("//tbody/tr[last()-1]/td[8]/text()")
    if price:
        price=price[0].replace(".","") 
        price=price.replace(",",".") 
        df.loc[len(df)] =[name,price,datetime.now(),'Sewage collection','LSDB',0]
    else:
        df.loc[len(df)] =[name,None,datetime.now(),'Sewage collection','LSDB',0]
    name='Τέλη Χρήσης €/m3'
    price=tree.xpath("//tbody/tr[last()-1]/td[9]/text()")
    if price:
        price=price[0].replace(".","") 
        price=price.replace(",",".") 
        df.loc[len(df)] =[name,price,datetime.now(),'Sewage collection','SBLA',0]
    else:
        df.loc[len(df)] =[name,None,datetime.now(),'Sewage collection','SBLA',0]

    try:
        url = "https://www.wbl.com.cy/el/page/water-rates"
        response = requests.get(url)
        tree = html.fromstring(response.content)
        name= 'Λεμεσος Οικιακά τέλη ανά τετραμηνία (συντελεστής ΦΠΑ 5%)'
        price1=tree.xpath('//table[1]/tbody/tr[2]/td[2]/text()')
        price2=tree.xpath('//table[1]/tbody/tr[3]/td[2]/text()')
        if price:
            price1=price1[0].replace(".","") 
            price1=price1.replace(",",".") 
            price2=price2[0].replace(".","")
            price2=price2.replace(",",".") 
            price=float(price1)+float(price2)
            df.loc[len(df)] =[name,price,datetime.now(),'Water Supply','WBL',0]
        else:
            df.loc[len(df)] =[name,None,datetime.now(),'Water Supply','WBL',0]  

    except IndexError:
        df.loc[len(df)] =[name,None,datetime.now(),'Water Supply','WBL',0] 

    try:
        name= 'Λεμεσος Εμποροβιομηχανικά  τέλη ανά τετραμηνία (συντελεστής ΦΠΑ 5%)'
        price1=tree.xpath('//table[5]/tbody/tr[2]/td[2]/text()')
        price2=tree.xpath('//table[5]/tbody/tr[3]/td[2]/text()')
        if price:
            price1=price1[0].replace(".","") 
            price1=price1.replace(",",".") 
            price2=price2[0].replace(".","")
            price2=price2.replace(",",".") 
            price=float(price1)+float(price2)
            df.loc[len(df)] =[name,price,datetime.now(),'Water Supply','WBL',0]
        else:
            df.loc[len(df)] =[name,None,datetime.now(),'Water Supply','WBL',0]
            
    except IndexError:
        df.loc[len(df)] =[name,None,datetime.now(),'Water Supply','WBL',0]

    url = "https://www.lwb.org.cy/gr/fees-and-rights.html"
    response = requests.get(url)
    tree = html.fromstring(response.content)

    name= 'Λαρνακα Οικιακά τέλη (ανά τριμηνία) (συντελεστής ΦΠΑ 5%)'
    price1=tree.xpath('//*[@id="a_w_66"]/div/div/table/tbody/tr[2]/td[2]/text()')
    price2=tree.xpath('//*[@id="a_w_66"]/div/div/table/tbody/tr[3]/td[2]/text()')
    if price:
        price1=price1[0].replace(".","") 
        price1=price1.replace(",",".") 
        price2=price2[0].replace(".","")
        price2=price2.replace(",",".") 
        price=float(price1)+float(price2)
        df.loc[len(df)] =[name,price,datetime.now(),'Water Supply','LWB',0]
    else:
        df.loc[len(df)] =[name,None,datetime.now(),'Water Supply','LWB',0]

    name= 'Λαρνακα Εμποροβιομηχανικά τέλη (ανά τριμηνία) (συντελεστής ΦΠΑ 5%)'
    price1=tree.xpath('//*[@id="a_w_67"]/div/div/table/tbody/tr[2]/td[2]/text()')
    price2=tree.xpath('//*[@id="a_w_67"]/div/div/table/tbody/tr[3]/td[2]/text()')
    if price:
        price1=price1[0].replace(".","") 
        price1=price1.replace(",",".") 
        price2=price2[0].replace(".","")
        price2=price2.replace(",",".") 
        price=float(price1)+float(price2)
        df.loc[len(df)] =[name,price,datetime.now(),'Water Supply','LWB',0]
    else:
        df.loc[len(df)] =[name,None,datetime.now(),'Water Supply','LWB',0]

waterSewageOtherCities()


def extract_float_price(price_str):
    # Remove any non-digit characters except for the dot
    prices = re.findall(r'€(\d+(?:\.\d+)?)', price_str)
    if prices:
        return float(prices[0])
    return None

def Rio():
    retailer = "Rio Cinemas"
    product_subclass = "Cinemas, theatres, concerts"
    url = 'https://www.riopremiercinemas.com.cy/price-policy/'
    response = requests.get(url)
    tree = html.fromstring(response.content)

    try:
        product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[2]/span/strong/text()")[0])
        product_name = "Rio Cinemas, Adults ticket"
        now = datetime.now()
        date_time_scraped = now
        df.loc[len(df)] = [product_name, product_price, date_time_scraped, product_subclass, retailer, 0]
    except (IndexError, ValueError) as e:
        print(f"Error retrieving price for Rio Cinemas, Adults ticket: {e}")

    try:
        product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[3]/span/strong/text()")[0])
        product_name = "Rio Cinemas, Children (up to 11) ticket"
        now = datetime.now()
        date_time_scraped = now
        df.loc[len(df)] = [product_name, product_price, date_time_scraped, product_subclass, retailer, 0]
    except (IndexError, ValueError) as e:
        print(f"Error retrieving price for Rio Cinemas, Children (up to 11) ticket: {e}")

    try:
        product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[4]/span/strong/text()")[0])
        product_name = "Rio Cinemas, Senior (64+)/ Student ticket"
        now = datetime.now()
        date_time_scraped = now
        df.loc[len(df)] = [product_name, product_price, date_time_scraped, product_subclass, retailer, 0]
    except (IndexError, ValueError) as e:
        print(f"Error retrieving price for Rio Cinemas, Senior (64+)/ Student ticket: {e}")

    try:
        product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[6]/span/strong/text()")[0])
        product_name = "Rio Cinemas, Adults 3D ticket"
        now = datetime.now()
        date_time_scraped = now
        df.loc[len(df)] = [product_name, product_price, date_time_scraped, product_subclass, retailer, 0]
    except (IndexError, ValueError) as e:
        print(f"Error retrieving price for Rio Cinemas, Adults 3D ticket: {e}")

    try:
        product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[7]/span/strong/text()")[0])
        product_name = "Rio Cinemas, Children 3D ticket"
        now = datetime.now()
        date_time_scraped = now
        df.loc[len(df)] = [product_name, product_price, date_time_scraped, product_subclass, retailer, 0]
    except (IndexError, ValueError) as e:
        print(f"Error retrieving price for Rio Cinemas, Children 3D ticket: {e}")

    try:
        product_price = extract_float_price(tree.xpath("//div[@class='txt']/p[8]/span/strong/text()")[0])
        product_name = "Rio Cinemas, Senior/Students 3D ticket"
        now = datetime.now()
        date_time_scraped = now
        df.loc[len(df)] = [product_name, product_price, date_time_scraped, product_subclass, retailer, 0]
    except (IndexError, ValueError) as e:
        print(f"Error retrieving price for Rio Cinemas, Senior/Students 3D ticket: {e}")

Rio()


#BOOKING
def Booking():

    retailer="Booking"
    product_subclass="Hotels, motels, inns and similar accommodation services"
   
# Define the URL for the Booking.com page for hotel X
    url = "https://www.booking.com/hotel/cy/frangiorgio-apartments.el.html"

    product_name="Frangiorgio Hotel, Τιμή για Δίκλινο για 1 βράδυ (Larnaca)"

    # Define the current month and year
    now = date.today()
    year = now.year
    month = now.month

    # Find the last weekend (last Saturday and Sunday) of the current month
    last_day_of_month = date(year, month+1, 1) - timedelta(days=1)
    last_weekend = None

    for d in range(last_day_of_month.day, 0, -1):
        current_date = date(year, month, d)
        if current_date.weekday() == 5:  # Saturday
            last_weekend = current_date
            break

    if last_weekend is None:
        for d in range(last_day_of_month.day, 0, -1):
            current_date = date(year, month, d)
            if current_date.weekday() == 6:  # Sunday
                last_weekend = current_date
                break

    if last_weekend is None:
        print("No valid last weekend found for the current month.")
        exit()

    # Define the date range and room type for the last weekend of the current month
    check_in_date = f"{year}-{month}-{last_weekend.day}"
    check_out_date = f"{year}-{month}-{last_weekend.day + 1}"
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
        if product_price:
            product_price=float(product_price[0])
        now = datetime.now()
        date_time_scraped = now 
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    product_name="Navarria Blue Hotel, Τιμή για Δίκλινο για 1 βράδυ (Λεμεσός)"
    # Define the URL for the Booking.com page for hotel X
    url = "https://www.booking.com/hotel/cy/navarria-ag-tychonas.el.html"
    #  Δίκλινο Δωμάτιο με 1 Διπλό ή 2 Μονά Κρεβάτια 
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
        if product_price:
            product_price=float(product_price[0])
        now = datetime.now()
        date_time_scraped = now 
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
        if product_price:
            product_price=float(product_price[0])
        now = datetime.now()
        date_time_scraped = now 
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
        if product_price:
            product_price=float(product_price[0])
        now = datetime.now()
        date_time_scraped = now 
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
        if product_price:
            product_price=float(product_price[0])
        now = datetime.now()
        date_time_scraped = now 
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

    room_type_id = "106235701" 
    url="https://www.booking.com/hotel/cy/princessa-vera-apartments.el.html"
    product_name="Princessa Vera Hotel Apartments, Τιμή για Standard Στούντιο 2 μονά κρεβάτι 1 βράδυ (Paphos)"

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
        if product_price:
            product_price=float(product_price[0])
        now = datetime.now()
        date_time_scraped = now 
        df.loc[len(df)] =[product_name,product_price,date_time_scraped,product_subclass,retailer,0]

#Booking()

#def GasCylinder():
#    try:
#        # Extract last month reported name
#        url = "https://consumer.gov.cy/en/price-observatories/learn-your-rights/66/?ctype=ar"
#        response = requests.get(url)
#        response.raise_for_status()  # Check for connection errors

#        tree = html.fromstring(response.content)
#        month_name = tree.xpath('//div[@class="mar-top-a"]/ul[@id="docs-list"]/li[last()]/a[@class="grp-head expand"]/text()')

#        if month_name:
#            clean_month_name = re.sub(r'^\d+\s*-\s*', '', month_name[0])
#            clean_month_name = clean_month_name.replace(" ", "_")
#            print(clean_month_name)

            # Remove unwanted characters
#            url = "https://consumer.gov.cy/assets/modules/wnp/articles/202302/66/docs/paratiritirio_" + clean_month_name.lower() + ".pdf"
#            response = requests.get(url)
#            response.raise_for_status()  # Check for connection errors

#            with open("file.pdf", "wb") as f:
#                f.write(response.content)

#            pdf_file = open("file.pdf", "rb")
#            pdf_reader = PyPDF2.PdfReader(pdf_file)

#            # Extracting price
#            for i in range(len(pdf_reader.pages)):  # Check if the required page exists
#                page = pdf_reader.pages[i]
#                match = re.search(r"\d+\s+ΚΥΛΙΝΔΡΟΣ.*?\d+\.\d+\s+\d+\.\d+\s+(\d+\.\d+)", page.extract_text())

#                if match:
#                    middle_price = match.group(1)
#                    df.loc[len(df)] = ["ΚΥΛΙΝΔΡΟΣ 10kg ", middle_price, datetime.now(), 'Liquefied hydrocarbons', 'Consumer Observatory', 0]
#                else:
#                    print("Price ΚΥΛΙΝΔΡΟΣ 10kg failed.")
#        else:
#            df.loc[len(df)] = ["ΚΥΛΙΝΔΡΟΣ 10kg ", None, datetime.now(), 'Liquefied hydrocarbons', 'Consumer Observatory', 0]
#    except Exception as e:
#        print("An error occurred:", e)
#        df.loc[len(df)] = ["ΚΥΛΙΝΔΡΟΣ 10kg ", None, datetime.now(), 'Liquefied hydrocarbons', 'Consumer Observatory', 0]

#GasCylinder()

#EUROPEAN UNIVERSITY
def euc():
    try:
        euc = tb.read_pdf('https://syllabus.euc.ac.cy/tuitions/euc-tuition-fees-c.pdf', pages = '2',pandas_options={'header': None}, stream=True)

        list_euc = []

        for i in range(0,4):
            euc[i][1] = euc[i][1].astype('string')
            for word in euc[i][1].to_list():
                word = word.replace(',','')
                word = int(word)
                list_euc.append(word)
        #the medicine and dental medicine the prices cannot be scrapped and are put here manually, same for online programs
        #the prices change only once a year
        df.loc[len(df)]=["EUROPEAN UNIVERSITY CYPRUS, Bachelors Programmes Average Yearly Tuition for 2024-2025",(sum(list_euc)+21000+21900+(9240*4))/(len(list_euc)+6),datetime.now(),'Tertiary education','European University Cyprus',0]
    except urllib.error.URLError:
        df.loc[len(df)]=["EUROPEAN UNIVERSITY CYPRUS, Bachelors Programmes Average Yearly Tuition for 2024-2025",None,'Tertiary education','European University Cyprus',0]

euc()

#fill the missing values with forward fill
def fillNone(df):
    df['product_price'] = pd.to_numeric(df['product_price'], errors='coerce')
    #transform the date_time_scrapped to datetime column
    df['date_time_scraped'] = pd.to_datetime(df['date_time_scraped'])
    df = df.sort_values(by=['product_name', 'date_time_scraped'])
    df['product_price'] = df.groupby(['product_name','retailer'])['product_price'].fillna(method='ffill')
    return df

df = fillNone(df)

#sort the values based on the date
df=df.sort_values(by='date_time_scraped')

def update_average_price():
    df['product_subclass'] = df['product_subclass'].str.lower()
    df['product_subclass'] = df['product_subclass'].replace('yogurt', 'yoghurt')
    df['product_subclass'] = df['product_subclass'].replace('miscellaneous printer matter', 'miscellaneous printed matter')
    df['product_subclass'] = df['product_subclass'].replace('other tobaco products', 'other tobacco products')
    df['product_subclass'] = df['product_subclass'].replace('hairdressing for men', 'hairdressing for men and children')
    df['product_subclass'] = df['product_subclass'].replace('other meats', 'hairdressing for men and children')
    
    now = datetime.now()
    today = now.date()

    # Convert 'date_time_scraped' column to datetime
    df['date_time_scraped'] = pd.to_datetime(df['date_time_scraped'])
    # Convert 'product_price' column to numeric, ignoring non-numeric values

    # Filter for today's products and update 'subclass_average' column
    today_products = df[df['date_time_scraped'].dt.date == today]
    df.loc[df['date_time_scraped'].dt.date == today, 'subclass_average'] = round(today_products.groupby('product_subclass')['product_price'].transform('mean'), 4)

update_average_price()

df.to_csv("BillionPricesProject_ProductList.csv", index=False)
