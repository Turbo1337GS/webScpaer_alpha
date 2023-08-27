# Web Scraper Alpha

Web Scraper Alpha is an asynchronous web scraping tool designed to crawl websites and extract cleaned text content from HTML pages. It uses asyncio and aiohttp libraries for efficient and concurrent processing of HTTP requests and HTML parsing.

## Installation

To use Web Scraper Alpha, follow these steps:

1. Clone the project from the GitHub repository: [https://github.com/Turbo1337GS/webScpaer_alpha](https://github.com/Turbo1337GS/webScpaer_alpha).
2. Install the required dependencies by running the following command in your terminal:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use Web Scraper Alpha, follow the instructions below:

1. Import the necessary libraries and classes:
   ```python
   import asyncio
   import aiohttp
   from collections import deque
   from urllib.parse import urljoin
   import os
   from bs4 import BeautifulSoup
   from readability import Document
   ```

2. Set global configuration variables according to your needs. These variables include:
   - `MAX_QUEUE_SIZE`: Maximum size of the crawling queue.
   - `DEPTH_LIMIT`: Maximum depth of crawling.
   - `FILE_NAME`: Name of the file to save the scraped data.
   - `BUFFER_SIZE`: Number of texts to buffer before saving to file.
   - `INITIAL_URL`: Starting URL for the web scraping process.
   - `NUM_WORKERS_MULTIPLIER`: Number of workers to create for concurrent processing.
   - `TCP_CONNECTOR_LIMIT_PER_HOST`: Maximum number of TCP connections per host.

3. Create an instance of the `WebScraper` class:
   ```python
   scraper = WebScraper()
   ```

4. Run the web scraping process by executing the `main` method:
   ```python
   loop = asyncio.get_event_loop()
   loop.run_until_complete(scraper.main())
   ```

5. The scraped data will be saved in the file specified by `FILE_NAME`.

## Class: WebScraper

The `WebScraper` class encapsulates the functionalities required for web scraping. It contains the following methods:

### Method: \_\_init\_\_

The constructor method initializes the instance variables of the class:
- `visited`: A set to store the URLs that have been visited.
- `queue`: An asyncio Queue to store the URLs to be crawled.
- `html_processing_queue`: An asyncio Queue to store the extracted HTML content for further processing.
- `unique_texts`: A set to store the unique cleaned text content.
- `buffered_texts`: A deque to buffer the cleaned text content before saving to file.
- `semaphore`: An asyncio Semaphore to limit the number of concurrent tasks.

### Method: save_to_file

This method saves the buffered text content to the specified file. It writes the content to the file and clears the buffer. It also prints statistics about the scraping process, including the number of visited articles, file size, queue size, and unique texts.

### Method: get_file_size_in_mb

This static method calculates the file size in megabytes given a file name.

### Method: process_html

This method processes the extracted HTML content. It uses the `readability` library to extract the article content from the HTML and then uses `BeautifulSoup` for further cleaning. The cleaned text content is added to the unique texts set and buffered for saving to file.

### Method: html_processor

This method is a coroutine that continuously processes the HTML content extracted from the queue. It calls the `process_html` method to clean and store the text content. It marks the task as done after processing.

### Method: fetch

This method performs the HTTP request to a given URL using an aiohttp session. It checks if the response contains HTML content and adds it to the HTML processing queue. It also extracts and enqueues all the linked URLs within the HTML. URL visits and exceptions are logged for debugging purposes.

### Method: worker

This method is a coroutine that continuously fetches and processes URLs from the queue. It calls the `fetch` method to perform the HTTP request and handling.

### Method: main

This method is the entry point of the web scraping process. It initializes the queue with the starting URL, creates a session with a TCP connector, and spawns worker tasks to handle the crawling and processing. After the tasks are completed, it saves any remaining buffered texts to the file.

## Configuration Variables

The web scraping process can be customized by adjusting the following global configuration variables:

- `MAX_QUEUE_SIZE`: Maximum size of the crawling queue. Increase this value if you want to scrape larger websites.
- `DEPTH_LIMIT`: Maximum depth of crawling. Increase this value to crawl deeper into a website.
- `FILE_NAME`: Name of the file to save the scraped data. You can change this to any filename you prefer.
- `BUFFER_SIZE`: Number of texts to buffer before saving to file. Increase this value to reduce the number of I/O operations.
- `INITIAL_URL`: Starting URL for the web scraping process. Change this to the desired website's URL.
- `NUM_WORKERS_MULTIPLIER`: Number of workers to create for concurrent processing. Adjust this value based on your CPU capabilities and desired crawling speed.
- `TCP_CONNECTOR_LIMIT_PER_HOST`: Maximum number of TCP connections per host. You can tune this value to optimize network performance.

## Conclusion

Web Scraper Alpha provides a powerful and customizable solution for scraping websites asynchronously. It leverages asyncio and aiohttp to achieve high-performance scraping and supports multi-threaded processing. By following the installation and usage instructions provided, you can easily apply Web Scraper Alpha to scrape websites and extract valuable information.
