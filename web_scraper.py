import requests
from bs4 import BeautifulSoup
import csv
import time
import random

class WebScraper:
    def __init__(self, base_url, pages_to_scrape):
        self.base_url = base_url
        self.pages_to_scrape = pages_to_scrape
        self.data = []

    def fetch_page(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an error for HTTP errors
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_product(self, product):
        try:
            title = product.find('h2', class_='product-title').get_text(strip=True)
            price = product.find('span', class_='product-price').get_text(strip=True)
            link = product.find('a', class_='product-link')['href']
            return {
                'title': title,
                'price': price,
                'link': link
            }
        except AttributeError as e:
            print(f"Error parsing product: {e}")
            return None

    def scrape(self):
        for page in range(1, self.pages_to_scrape + 1):
            url = f"{self.base_url}/page/{page}"
            html = self.fetch_page(url)
            if html:
                soup = BeautifulSoup(html, 'html.parser')
                products = soup.find_all('div', class_='product-item')
                for product in products:
                    parsed_product = self.parse_product(product)
                    if parsed_product:
                        self.data.append(parsed_product)
            time.sleep(random.uniform(1, 3))  # Respectful scraping

    def save_to_csv(self, filename):
        keys = self.data[0].keys() if self.data else []
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.data)

def main():
    base_url = 'https://example-ecommerce-site.com/products'
    pages_to_scrape = 10
    scraper = WebScraper(base_url, pages_to_scrape)
    
    print("Starting scraping process...")
    scraper.scrape()
    
    print("Saving to CSV...")
    scraper.save_to_csv('scraped_data.csv')
    
    print("Scraping process completed!")

if __name__ == "__main__":
    main()