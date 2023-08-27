# webScpaer_alpha
This is a web scraper written in Python that utilizes asynchronous programming with the aiohttp library to efficiently retrieve and parse web pages. It extracts the main content from HTML pages using the readability library and saves the cleaned texts to a file.

# Documentation: Web Scraper

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [Documentation](#documentation)

## Overview
This is a web scraper written in Python that utilizes asynchronous programming with the `aiohttp` library to efficiently retrieve and parse web pages. It extracts the main content from HTML pages using the `readability` library and saves the cleaned texts to a file.

## Installation
To use this web scraper, follow the steps below:

1. Install Python: This code requires Python 3.7 or higher. If you don't have Python installed, download and install it from the official Python website (https://www.python.org/).

2. Install dependencies: Open a terminal or command prompt and navigate to the project directory. Run the following command to install the required libraries:
   ```
   pip install aiohttp beautifulsoup4 readability-lxml
   ```

3. Clone the repository: Use `git clone` to clone the repository to your local machine:
   ```
   git clone <repository_url>
   ```

## Usage
Once you have installed the necessary dependencies and cloned the repository, follow the usage instructions below:

1. Modify the code: Open the `main.py` file and update the following variables according to your requirements:
   - `depth_limit`: The maximum depth of web pages to be visited.
   - `file_name`: The name of the file to which the cleaned texts will be saved.
   - `initial_url`: The initial URL from which the scraping will start.

2. Run the scraper: Open a terminal or command prompt, navigate to the project directory, and execute the following command:
   ```
   python main.py
   ```

3. Wait for the scraping to finish: The scraper will start visiting web pages, extracting the main content, and saving it to the file. Progress and file size will be displayed in the console.

## Documentation

### `save_to_file(content, file_name)`

This function saves the cleaned content to the specified file.

- **Parameters:**
  - `content` (str): The cleaned text content to be saved.
  - `file_name` (str): The name of the file to which the content will be saved.

### `get_file_size(file_name)`

This function returns the size of a file in bytes.

- **Parameters:**
  - `file_name` (str): The name of the file.

- **Returns:**
  - `int`: The size of the file in bytes.

### `fetch(url, session, depth)`

This is an asynchronous function that fetches a web page, extracts the main content, and updates the scraping queue.

- **Parameters:**
  - `url` (str): The URL of the web page to be fetched.
  - `session` (aiohttp.ClientSession): An aiohttp session object for making HTTP requests.
  - `depth` (int): The current depth of the page in the scraping process.

### `main()`

This is the main function that sets up the scraping process.

### Additional Information

- The `visited` set keeps track of URLs that have already been visited to avoid duplicate scraping.

- The `queue` list holds URLs to be visited along with their respective depth.

- The scraper adheres to a maximum depth limit specified by `depth_limit`.

- The `initial_url` variable determines the starting point for the scraping process.

- The `readability` library is used to extract the main content from HTML pages.

- The `BeautifulSoup` library is used to parse the cleaned content and retrieve links.

- The `unique_texts` set keeps track of unique cleaned texts to avoid duplicates in the saved file.

- The `cleaned_text` is saved to the `file_name` if its length is greater than 30 characters.

- The program outputs the number of visited articles and the file size at regular intervals.

## Conclusion
This web scraper provides an efficient way to extract and save cleaned text content from web pages. It uses asynchronous programming to speed up the scraping process and ensures that the saved file contains only unique content. Feel free to modify and adapt the code according to your own requirements.
