# Grab Food Scraper Documentation

### GITHUB 
```https://github.com/Suryakiran09/Grab-food-web-scraper.git ```

## Overview

The Grab Food Scraper is a Python application designed to extract restaurant data from the Grab Food website (https://food.grab.com/sg/en) using web scraping techniques. The application utilizes the Selenium and BeautifulSoup libraries to automate the web browsing process, navigate to the desired location, and extract relevant information about restaurants, such as their names, cuisines, ratings, delivery times, distances, discounts, promotions, and images.

## Features

- **Web Automation**: The application uses Selenium to automate the web browsing process, handling tasks such as accepting cookies, entering the desired location, and scrolling through the page to load all restaurant data.
- **Data Extraction**: BeautifulSoup is employed to parse the HTML content of the loaded web page and extract relevant restaurant information.
- **IP Rotation (Optional)**: To mitigate potential IP blocking or rate-limiting issues, the application supports the use of a list of proxies for IP rotation during the scraping process.
- **Multithreading**: The application leverages multithreading to efficiently handle the scrolling operation, ensuring that all data is loaded before extraction.
- **Data Storage**: The extracted data is stored in two formats: a CSV file (`data.csv`) and a compressed NDJSON file (`grab_food_data.ndjson.gz`).
- **Logging**: Detailed logging is implemented to track the application's progress, record any errors or warnings, and provide relevant information during execution.

## Prerequisites

To run the Grab Food Scraper, the following prerequisites must be met:

- Python 3.x installed
- Required Python libraries:
  - Selenium
  - BeautifulSoup
  - Pandas
  - requests
- Chrome WebDriver (compatible with your Chrome version) installed and available in the system's PATH

## Installation

1. Clone the repository or download the source code.
2. Install the required Python libraries using pip:

```shell
pip install selenium beautifulsoup4 pandas requests
```

3. Download the Chrome WebDriver compatible with your Chrome version and add it to your system's PATH, or update the code to specify the path to the WebDriver executable.

## Usage

1. Open the `main.py` file.
2. Optionally, if you have a list of proxies for IP rotation, uncomment the `proxies` list in the `__main__` block and update it with your desired proxies(Better to not use them they may have got expired or not working).
3. Run the script using the following command:

```shell
python main.py
```

4. The application will start executing, and the extracted data will be saved to `grab_food_data.ndjson.gz` (compressed NDJSON file) and `data.csv` (CSV file) in the same directory.
5. Check the log file `grab_food_scraper.log` for any relevant information or errors during the execution.

## Code Structure

The Grab Food Scraper application follows an Object-Oriented Programming (OOP) approach and is structured as follows:

- `main.py`: The main script that contains the `GrabFoodScraper` class and orchestrates the scraping process.
- `GrabFoodScraper` class:
  - `__init__`: Initializes the scraper object with the URL, location, and optional proxies.
  - `setup_driver`: Sets up the Chrome WebDriver with specific options and a random proxy (if provided).
  - `accept_cookies`: Accepts cookies on the website if the "Accept" button is clickable within a timeout.
  - `enter_location`: Enters the specified location into the input field, submits, and waits for the layout to load.
  - `scroll_to_end`: Scrolls to the end of the page to load all restaurant data, leveraging multithreading for efficiency.
  - `extract_data`: Extracts restaurant data from the loaded page using BeautifulSoup.
  - `save_data`: Saves the extracted data to a CSV file and a compressed NDJSON file.
  - `run`: Orchestrates the entire scraping process by calling the other methods in the correct order.

## Logging and Error Handling

The Grab Food Scraper incorporates logging functionality to record relevant information and errors during execution. The logs are written to the `grab_food_scraper.log` file and also displayed in the console.

Exception handling and timeouts are implemented to handle situations where elements are not immediately available or the page takes longer to load.

## Scalability and Performance

To ensure scalability and performance, the Grab Food Scraper employs the following techniques:

- **IP Rotation**: The application supports the use of a list of proxies for IP rotation during the scraping process, mitigating potential IP blocking or rate-limiting issues.
- **Multithreading**: The scrolling operation is performed in a separate thread, allowing the main thread to continue executing while the page is being scrolled and loaded.
- **Optimized Data Extraction**: The application utilizes BeautifulSoup for efficient HTML parsing and data extraction, minimizing the computational overhead.
- **Compressed Data Storage**: The extracted data is stored in a compressed NDJSON format, reducing the storage footprint and improving data transfer efficiency.

## Null Value Report

The null value report for the extracted data can be checked in the `main.ipynb` file. Here are the details:

```python
Total Count of Records: 277
Null/Non-null Statistics:
Column: Restaurant Name, Null: 0, Non-null: 277
Column: Restaurant Cuisine, Null: 0, Non-null: 277
Column: Restaurant Rating, Null: 42, Non-null: 235
Column: Restaurant Delivery Time, Null: 0, Non-null: 277
Column: Restaurant Distance, Null: 0, Non-null: 277
Column: Discount, Null: 248, Non-null: 29
Column: Promo, Null: 0, Non-null: 277
Column: Images, Null: 0, Non-null: 277
```

This report provides information about the total number of records extracted and the null/non-null statistics for each column in the extracted data. It can be used to analyze the data quality and identify any missing or incomplete values.

## Problem Faced During the Implementation

### Problem 1: Handling Dynamic Content Loading

During the implementation, one of the challenges faced was handling dynamic content loading on the website. The Grab Food website loads restaurant data dynamically as the user scrolls down the page, making it difficult to extract all the available data.

#### Solution/Approach:

To address this issue, the application implements a scrolling mechanism that scrolls to the end of the page and waits for the content to load fully. This is achieved by continuously scrolling to the bottom of the page and checking if the page height has changed. Once the page height remains constant, it is assumed that all data has been loaded.

### Problem 2: Timeout and Exception Handling

Another challenge encountered was handling timeouts and exceptions when interacting with the website. Sometimes, certain elements on the page were not immediately available or took longer to load, causing the application to throw exceptions or timeout errors.

#### Solution/Approach:

To mitigate this issue, the application incorporates exception handling and timeouts. The code uses the WebDriverWait class from Selenium to wait for specific elements to be present or clickable within a specified timeout period. If the timeout is exceeded, the code gracefully handles the exception and proceeds with the scraping process.

## Future Enhancements

### Error Handling and Recovery

- **Retry Mechanism**: Implement a retry mechanism for failed requests or timeouts to automatically retry failed requests a certain number of times before logging an error.
- **Checkpointing**: Introduce checkpointing functionality to save the current state of the scraping process periodically, allowing for recovery from unexpected interruptions without losing progress.

### User Interface

- **GUI Application**: Develop a graphical user interface (GUI) for the scraper, providing users with a more intuitive and user-friendly way to interact with the application, configure scraping parameters, and view the extracted data.
- **Interactive Reports**: Generate interactive reports or dashboards using tools like Dash or Streamlit to allow users to explore and analyze the extracted data in real-time.


## Steps to Execute the Code Locally

1. Clone the repository or download the source code.
2. Install the required Python libraries using pip:

```shell
pip install selenium beautifulsoup4 pandas requests
```

3. Download the Chrome WebDriver compatible with your Chrome version and add it to your system's PATH, or update the code to specify the path to the WebDriver executable.
4. Open the `main.py` file.
5. Optionally, if you have a list of proxies for IP rotation, uncomment the `proxies` list in the `__main__` block and update it with your desired proxies.
6. Run the script using the following command:

```shell
python main.py
```

7. Check the log file `grab_food_scraper.log` for any relevant information or errors during the execution.

!!!Warning: Delay for Image Loading
#### It's important to note that a delay of 25 seconds has been added for image loading please open the website. This delay


!!!Warning: Location Extraction
#### I have extracted the locations also for the particular restaurants but extracted only for some restaurants didnt added it into the main code it is added in the main.ipynb file.