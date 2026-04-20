"""
Simple web crawler that starts from a given URL, fetches its content,
finds all links to the same domain, and crawls them concurrently using threads.
Limits the number of visited pages to 50.

Sources & Documentation:
- requests: https://docs.python-requests.org/en/latest/
- BeautifulSoup (bs4): https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- threading: https://docs.python.org/3/library/threading.html
- queue: https://docs.python.org/3/library/queue.html
"""

import threading
import queue
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from typing import Set
from concurrent.futures import ThreadPoolExecutor

def get_links(url: str, domain: str) -> Set[str]:
    """
    Fetch the content of the URL and extract all links that belong to the same domain.
    """
    links = set()
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all("a", href=True):
            href = tag['href']
            # Construct absolute URL
            absolute_url = urljoin(url, href)
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc == domain:
                # Remove fragment part
                clean_url = absolute_url.split('#')[0]
                links.add(clean_url)
    except (requests.RequestException, Exception):
        pass
    return links

def crawler(start_url: str, max_pages: int = 50) -> None:  # Zmieniono na 50 zgodnie z poleceniem
    """
    Crawl web pages starting from start_url, visiting up to max_pages pages.
    """
    parsed_start = urlparse(start_url)
    domain = parsed_start.netloc

    visited = set()  # type: Set[str]
    q = queue.Queue()
    q.put(start_url)

    lock = threading.Lock()

    def worker():
        while True:
            try:
                url = q.get(timeout=3)
            except queue.Empty:
                break
            with lock:
                if len(visited) >= max_pages:
                    q.task_done()
                    break
                if url in visited:
                    q.task_done()
                    continue
                visited.add(url)
            links = get_links(url, domain)
            with lock:
                for link in links:
                    if link not in visited:
                        q.put(link)
            q.task_done()

    num_threads = 10
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()
        threads.append(t)

    q.join()

    for t in threads:
        t.join(timeout=1)

    print(f"Visited {len(visited)} pages.")

if __name__ == "__main__":
    start_url = "https://example.com"
    import time
    start_time = time.perf_counter()
    crawler(start_url)
    end_time = time.perf_counter()
    print(f"Czas wykonania: {end_time - start_time:.2f} sekundy")
