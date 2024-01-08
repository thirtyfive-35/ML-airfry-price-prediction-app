from bs4 import BeautifulSoup
from playwright.sync_api import Playwright, sync_playwright, expect
import time


class hepsiburada_data_extraction:
    def __init__(self,base_url,target_url,target_class,limit_page) -> None:
        self.base_url = base_url
        self.target_url = target_url
        self.target_class = target_class
        self.limit_page = limit_page
        
    def run(self):
        with sync_playwright() as self.p:
            self.hepsiburada_link(self.p)
    def extract_links(self,html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        div_with_class = soup.find('div', class_= self.target_class)
        if div_with_class:
            links = [a['href'] for a in div_with_class.find_all('a', href=True)]
            return links
        else:
            return []

    def complete_links(self,base_url, links):
        completed_links = []
        for link in links:
            if link.startswith("http"):
                completed_links.append(link)
            else:
                completed_links.append(base_url + link)
        return completed_links

    def hepsiburada_link(self,playwright: Playwright) -> None:
        browser = self.p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(self.target_url)
            
        # Çerez uyarısını kabul et
        page.get_by_role("button", name="Kabul et").click()

        print("Extracted Links:")
        sayfa_numarasi = 1
        with open("dosya.txt", "w", encoding="utf-8") as dosya:
            while True:
                # Bu kısımda sayfanın HTML içeriğini alıyoruz.
                html_content = page.content()

                # BeautifulSoup kullanarak bağlantıları çıkartıyoruz.
                links = self.complete_links(self.base_url,self.extract_links(html_content))

                for link in links:
                    dosya.write(link + '\n')

                # Sayfa numarasını artırarak bir sonraki sayfaya geç
                sayfa_numarasi += 1
                yeni_sayfa_url = f"{self.target_url}?sayfa={sayfa_numarasi}"
                page.goto(yeni_sayfa_url)
                time.sleep(2)

                # Hepsiburada'nın sayfa numarası sınırlaması varsa, döngüyü sonlandır
                if "Sayfa bulunamadı" in page.title():
                    break
                        
                if sayfa_numarasi == self.limit_page:
                    break

        context.close()
        browser.close()

