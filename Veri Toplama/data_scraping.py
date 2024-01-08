from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv

class HepsiburadaDataExtractor:
    def __init__(self, base_url, target_class, price_data_attribute, product_name_selector):
        self.base_url = base_url
        self.target_class = target_class
        self.price_data_attribute = price_data_attribute
        self.product_name_selector = product_name_selector
        self.sayac = 0

    def extract_data(self, page):
        # Sayfanın HTML içeriğini al
        html_content = page.content()
        table_content = ""
        
        # BeautifulSoup ile işle
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Belirli bir table'ı seç
        table = soup.find('table', class_=self.target_class)

        if table:
            # Table içindeki tr'leri seç
            rows = table.find_all('th')
            cols = table.find_all('td')

            for row, col in zip(rows, cols):
                table_content += row.get_text(strip=True) + " " + col.get_text(strip=True) + ";"

            # span içindeki metni al
            price_span = soup.find('span', {'data-bind': self.price_data_attribute})
            if price_span:
                price_text = price_span.get_text(strip=True)
                table_content += "price " + price_text + ";"

            # Ürün adı içindeki metni al
            product_name_h1 = soup.find('h1', {'class': self.product_name_selector})
            if product_name_h1:
                product_name_text = product_name_h1.get_text(strip=True)
                # İlk boşluğa kadar olan kısmı al
                first_word = product_name_text.split()[0]
                table_content += "marka " + first_word + ";"
        return table_content

    def run(self, links):
        # Aşağıdaki satırda sync_playwright() fonksiyonunu kullanın
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            context = browser.new_context()
            for link in links:
                try:
                    page = context.new_page()
                    page.goto(link)
                    self.sayac += 1
                    page.wait_for_load_state('load', timeout=30000)  # Bekleme süresini artırabilirsiniz
                    table_content = self.extract_data(page)
                    self.write_doc(table_content)
                    page.close()
                except Exception as e :
                    print(f"{self.sayac}")
                    continue

            context.close()
            browser.close()

    def write_doc(self, table_content):
        with open("data2.txt", "a", encoding="utf-8") as file:
            file.write(table_content + "\n")





def toCsv():
    label = []

    with open("data2.txt", "r", encoding="utf-8") as file:
        veri_seti = file.readlines()

        for satir in veri_seti:
            veriler = satir.split(';')
            
            for veri in veriler:
                etiket_deger = veri.strip().split(' ')
                etiket = etiket_deger[0]
                deger = ' '.join(etiket_deger[1:])
                if etiket != '':
                    if etiket not in label:
                        label.append(etiket)

    # CSV dosyasına yazma işlemi
    with open("output2.csv", "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        # İlk satır olarak etiketleri yaz
        writer.writerow(label)

        with open("data2.txt", "r", encoding="utf-8") as file:
            veri_seti = file.readlines()

            for satir in veri_seti:
                veriler = satir.split(';')

                # Satırdaki etiketleri ve değerleri kontrol et
                satir_degerleri = [''] * len(label)  # Her etiket için bir değer listesi
                for veri in veriler:
                    etiket_deger = veri.strip().split(' ')
                    etiket = etiket_deger[0]
                    deger = ' '.join(etiket_deger[1:])

                    # Eğer etiket label listesinde varsa, değeri ilgili indekse ekle
                    if etiket in label:
                        indeks = label.index(etiket)
                        satir_degerleri[indeks] = deger

                # CSV dosyasına satırı yaz
                writer.writerow(satir_degerleri)
