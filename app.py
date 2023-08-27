import asyncio
import aiohttp
from collections import deque
from urllib.parse import urljoin
import os
from bs4 import BeautifulSoup
from readability import Document

# Global Configuration Variables
MAX_QUEUE_SIZE = 500000
DEPTH_LIMIT = 3
FILE_NAME = "clean_scraped_data.txt"
BUFFER_SIZE = 5
INITIAL_URL = "https://pl.wikipedia.org/wiki/Wikipedia:Strona_g%C5%82%C3%B3wna"
NUM_WORKERS_MULTIPLIER = 3
TCP_CONNECTOR_LIMIT_PER_HOST = 20

class WebScraper:
    def __init__(self):
        self.visited = set()
        self.queue = asyncio.Queue(maxsize=MAX_QUEUE_SIZE)
        self.html_processing_queue = asyncio.Queue()
        self.unique_texts = set()
        self.buffered_texts = deque()
        self.semaphore = asyncio.Semaphore(5)

    async def save_to_file(self):
        with open(FILE_NAME, 'a', encoding='utf-8') as f:
            while self.buffered_texts:
                f.write(self.buffered_texts.popleft())
                f.write('\n\n')
                
        print(f"(Visited: {len(self.visited)} articles, "
              f"File size: {self.get_file_size_in_mb(FILE_NAME):.2f} MB, "
              f"Queue size: {self.queue.qsize()}, "
              f"Unique texts: {len(self.unique_texts)})")

    @staticmethod
    def get_file_size_in_mb(file_name):
        return os.path.getsize(file_name) / (1024 * 1024)

    async def process_html(self, text):
        document = Document(text)
        readable_article = document.summary()

        soup = BeautifulSoup(readable_article, 'html.parser')
        cleaned_text = soup.text.strip()

        if len(cleaned_text) > 20:
            cleaned_content = ' '.join(cleaned_text.split())
            if cleaned_content not in self.unique_texts:
                self.unique_texts.add(cleaned_content)
                self.buffered_texts.append(cleaned_content)

                if len(self.buffered_texts) >= BUFFER_SIZE:
                    await self.save_to_file()

    async def html_processor(self):
        while True:
            text = await self.html_processing_queue.get()
            await self.process_html(text)
            self.html_processing_queue.task_done()

    async def fetch(self, url, session, depth):
        async with self.semaphore:
            if depth > DEPTH_LIMIT or url in self.visited:
                return

            self.visited.add(url)

            try:
                async with session.get(url) as response:
                    if 'text/html' not in response.headers.get('content-type', ''):
                        return

                    text = await response.text(errors='replace')
                    await self.html_processing_queue.put(text)

                    for link in BeautifulSoup(text, 'html.parser').find_all('a'):
                        href = link.get('href')
                        if href and self.queue.qsize() < MAX_QUEUE_SIZE:
                            full_url = urljoin(url, href)
                            if full_url not in self.visited:
                                await self.queue.put((full_url, depth + 1))

            except Exception as e:
                print(f"An error occurred: {e}")

    async def worker(self, session):
        while True:
            url, depth = await self.queue.get()
            await self.fetch(url, session, depth)
            self.queue.task_done()

    async def main(self):
        await self.queue.put((INITIAL_URL, 1))

        num_workers = int(os.cpu_count() * NUM_WORKERS_MULTIPLIER)

        connector = aiohttp.TCPConnector(limit_per_host=TCP_CONNECTOR_LIMIT_PER_HOST)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for _ in range(num_workers):
                task = asyncio.create_task(self.worker(session))
                tasks.append(task)
            
            html_processor_task = asyncio.create_task(self.html_processor())

            await self.queue.join()
            await self.html_processing_queue.join()

            for task in tasks:
                task.cancel()
            
            html_processor_task.cancel()

        await self.save_to_file()

if __name__ == "__main__":
    scraper = WebScraper()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scraper.main())
