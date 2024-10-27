import requests
from bs4 import BeautifulSoup
import os
import time
from tqdm import tqdm
import re

class BookScraper:
    def __init__(self):
        self.base_url = "https://freekidsbooks.org/page/{}/"
        self.download_dir = "downloaded_books"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Create download directory if it doesn't exist
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def download_file(self, url, filename, folder):
        try:
            response = requests.get(url, headers=self.headers, stream=True)
            response.raise_for_status()
            
            # Clean filename of invalid characters
            filename = re.sub(r'[<>:"/\\|?*]', '', filename)
            
            file_path = os.path.join(folder, filename)
            total_size = int(response.headers.get('content-length', 0))

            with open(file_path, 'wb') as file, tqdm(
                desc=filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as progress_bar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    progress_bar.update(size)
            
            return True
        except Exception as e:
            print(f"Error downloading {filename}: {str(e)}")
            return False

    def scrape_page(self, page_number):
        url = self.base_url.format(page_number)
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all books on the page
            books = soup.find_all('a', class_='download-book')
            
            for book in books:
                book_url = book.get('href')
                book_name = book.get('download', 'unknown.pdf')
                
                # Scraping the author
                author_tag = book.find_previous('p', class_='author')
                author_name = author_tag.get_text(strip=True) if author_tag else "Unknown Author"
                
                # Scraping the description
                description_tag = book.find_previous('div', class_='book_description_middle')
                description_p = description_tag.find_all('p')[1].get_text(strip=True) if description_tag else "No description available."
                
                # Clean the book name for folder creation
                folder_name = re.sub(r'[<>:"/\\|?*]', '', book_name.replace('.pdf', ''))
                folder_path = os.path.join(self.download_dir, folder_name)
                
                # Create folder for the book
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                
                # Download the book
                print(f"\nDownloading: {book_name}")
                success = self.download_file(book_url, book_name, folder_path)
                
                if success:
                    print(f"Successfully downloaded: {book_name}")
                else:
                    print(f"Failed to download: {book_name}")
                
                # Save the author in a file
                author_file = os.path.join(folder_path, 'author.txt')
                with open(author_file, 'w') as file:
                    file.write(author_name)
                
                # Save the description in a file
                description_file = os.path.join(folder_path, 'description.txt')
                with open(description_file, 'w') as file:
                    file.write(description_p)
                
                # Be nice to the server
                time.sleep(2)
                
        except Exception as e:
            print(f"Error scraping page {page_number}: {str(e)}")

    def run(self, start_page=1, end_page=12):
        print(f"Starting to scrape pages {start_page} to {end_page}")
        for page in range(start_page, end_page + 1):
            print(f"\nScraping page {page}")
            self.scrape_page(page)
            # Be nice to the server between pages
            time.sleep(3)

if __name__ == "__main__":
    scraper = BookScraper()
    scraper.run(1, 12)
