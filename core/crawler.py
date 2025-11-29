import threading
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from queue import Queue
import time

class Crawler:
    def __init__(self, base_url, max_threads=3, session=None, proxies=None):
        self.base_url = base_url
        self.visited_urls = set()
        self.url_queue = Queue()
        self.max_threads = max_threads
        self.session = session
        if proxies and self.session:
            self.session.proxies.update(proxies)

    def is_valid(self, url):
        ignore_ext = ('.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.pdf', '.ico', '.bmp', '.svg')
        return not url.lower().endswith(ignore_ext)

    def crawl_url(self, url):
        try:
            resp = self.session.get(url, timeout=5)
            time.sleep(1) 
            if 'text' not in resp.headers.get('Content-Type', ''):
                return
            bs = BeautifulSoup(resp.content, 'html.parser')
            for link in bs.find_all('a', href=True):
                next_url = urljoin(url, link['href']).split('#')[0]
                if self.is_valid(next_url) and next_url.startswith(self.base_url):
                    if next_url not in self.visited_urls:
                        self.visited_urls.add(next_url)
                        self.url_queue.put(next_url)
        except Exception as e:
            print(f"[Crawler Error] {url}: {e}")

    def worker(self):
        while not self.url_queue.empty():
            url = self.url_queue.get()
            self.crawl_url(url)
            self.url_queue.task_done()

    def run(self):
        self.visited_urls.add(self.base_url)
        self.url_queue.put(self.base_url)
        threads = []
        for _ in range(self.max_threads):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            threads.append(t)
            t.start()
        self.url_queue.join()
        return list(self.visited_urls)