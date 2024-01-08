from hepsiburada_link_scraping import hepsiburada_data_extraction
from data_scraping import HepsiburadaDataExtractor
from data_scraping import toCsv

# data link scraping
base_url = "https://www.hepsiburada.com"
target_url = "https://www.hepsiburada.com/fritozler-c-22017"
target_class = 'VVfQFa_rVJ7k5k6NHFV3'
limit_page = 5


nesne = hepsiburada_data_extraction(base_url,target_url,target_class,limit_page)
nesne.run()

# data scraping
base_url = "https://www.hepsiburada.com"
target_class = "data-list tech-spec"  
price_data_attribute = "markupText:'currentPriceBeforePoint'"
product_name_selector = 'product-name best-price-trick'

# Dosyadan linkleri oku
with open("dosya.txt", "r", encoding="utf-8") as dosya:
    links = dosya.read().splitlines()

extractor = HepsiburadaDataExtractor(base_url, target_class, price_data_attribute, product_name_selector)
extractor.run(links)

# txt to csv
toCsv()