import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from readability import Document

visited = set()
queue = []
depth_limit = 4
file_name = "clean_scraped_data.txt"
unique_texts = set()

async def save_to_file(content, file_name):
    cleaned_content = ' '.join(content.split())
    if cleaned_content not in unique_texts:
        unique_texts.add(cleaned_content)
        with open(file_name, 'a') as f:
            f.write(cleaned_content + "\n\n")

def get_file_size(file_name):
    return os.path.getsize(file_name)

async def fetch(url, session, depth):
    global visited, queue

    if depth > depth_limit:
        return

    if url in visited:
        return

    visited.add(url)

    try:
        response = await session.head(url)
        if 'text/html' not in response.headers.get('content-type', ''):
            return

        response = await session.get(url)
        text = await response.text()
        document = Document(text)
        readable_article = document.summary()

        soup = BeautifulSoup(readable_article, 'html.parser')
        cleaned_text = soup.text.strip()

        if len(cleaned_text) > 30:
            await save_to_file(cleaned_text, file_name)
            print(f"(Visited: {len(visited)} articles, File size: {get_file_size(file_name)} bytes)")

        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                full_url = urljoin(url, href)
                if full_url not in visited:
                    queue.append((full_url, depth + 1))

    except Exception as e:
        print(f"An error occurred: {e}")

async def main():
    global queue
    initial_url = "https://pl.wikipedia.org/wiki/Wikipedia:Strona_g%C5%82%C3%B3wna"
    queue.append((initial_url, 1))

    async with aiohttp.ClientSession() as session:
        while queue:
            url, depth = queue.pop(0)
            await fetch(url, session, depth)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
