import threading
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import os 

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class WebScrap:
    def __init__(self):
        self.file_extensions = ["mp3", "aac", "pptx", "pdf", "mp4", "xlsx"]
        self.text_data = set()

    def check_is_file_link(self, url):
        if url.split(".")[-1] in self.file_extensions:
            return True
        return False
        
    def write_data(self, scraped_data, path, file_name):
        write_path = os.path.join(path, file_name)
        with open(write_path, "a") as f:
            f.write(scraped_data)
            f.close

    def get_links_and_scrap(self, url, depth, domain, visited=set(), unique_lines=set()):
        if depth == 0:
            return set()

        visited.add(url)

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines() if line.strip())

        for line in lines:
            self.text_data.add(line)

        visible_links = set()

        for link in links:
            href = link.get('href')
            if href and not href.startswith('#') and not href.startswith('javascript:void') and not self.check_is_file_link(href):
                absolute_link = self.get_absolute_url(url, href)

                if absolute_link not in visited and domain in absolute_link:
                    visited.add(absolute_link)
                    visible_links.add(absolute_link)

                    threads = []
                    thread = threading.Thread(target= self.get_links_and_scrap, args=(absolute_link, depth-1, domain, visited, unique_lines))
                    threads.append(thread)
                    thread.start()
                    
        return visible_links

    def get_absolute_url(self, base_url, href):
        return urljoin(base_url, href)
    
    def perform_scraping(self, url, depth=2):
        domain = urlparse(url).netloc
        visible_links = self.get_links_and_scrap(url, depth, domain)
        combined_data = "\n".join(self.text_data)
        return combined_data

def main():
    sd = WebScrap()
    url = "https://zealogics.com"
    depth =  5 # Set the desired depth
    sd.perform_scraping(url, depth)

    # domain = urlparse(url).netloc

    # start_time = time.time()

    # visible_links = sd.get_links_and_scrap(url, depth, domain)
    # sd.write_data(sd.text_data)

    # elapsed_time = time.time() - start_time
    # print(f"Scrap completed in {elapsed_time} seconds")
    
if __name__ == "__main__":
    main()

    a = 0
