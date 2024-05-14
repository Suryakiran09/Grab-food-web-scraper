import time
import pandas as pd
import gzip
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
import random

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename='grab_food_scraper.log')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

class GrabFoodScraper(threading.Thread):
    def __init__(self, url, location, proxies=None):
        # Initialize GrabFoodScraper object with URL, location, and optional proxies
        threading.Thread.__init__(self) 
        self.url = url
        self.location = location
        self.proxies = proxies
        self.setup_driver()  # Set up Selenium WebDriver

    def setup_driver(self):
        # Set up Chrome WebDriver with specific options
        chrome_options = webdriver.ChromeOptions()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134"
        chrome_options.add_argument(f'user-agent={user_agent}')
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        if self.proxies:
            proxy = random.choice(self.proxies)
            proxy_host, proxy_port = proxy.split(":")
            proxy_server = f"{proxy_host}:{proxy_port}"
            chrome_options.add_argument(f'--proxy-server={proxy_server}')
        self.driver = webdriver.Chrome(options=chrome_options)

    def accept_cookies(self):
        # Accept cookies if the accept button is clickable within a timeout
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept")]'))).click()
        except TimeoutException:
            pass  # If timeout occurs, proceed without clicking

    def enter_location(self):
        # Enter location into the input field, submit, and wait for the layout to load
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-layout")))
        location_input = self.driver.find_element(By.ID, 'location-input')
        location_input.click()
        time.sleep(2)
        location_input.clear()
        location_input.send_keys(self.location)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-btn.submitBtn___2roqB.ant-btn-primary")))
        submit_button = self.driver.find_element(By.CSS_SELECTOR, '.ant-btn.submitBtn___2roqB.ant-btn-primary')
        submit_button.click()
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".ant-layout")))

    def scroll_to_end(self):
        # Define function to scroll to the end of the page
        def _scroll():
            last_height = self.driver.execute_script("return document.body.scrollHeight")
            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

        # Create a thread for scrolling
        scroll_thread = threading.Thread(target=_scroll)
        scroll_thread.start()
        scroll_thread.join()  # Wait for scrolling thread to finish

    def extract_data(self):
        # Extract restaurant data from the loaded page
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "RestaurantListRow___1SbZY")))
        layout_div = self.driver.find_element(By.CLASS_NAME, 'RestaurantListRow___1SbZY')
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "name___2epcT")))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        details = soup.find_all('div', class_='ant-row-flex ant-row-flex-start ant-row-flex-top asList___1ZNTr')

        restaurant_names = []
        restaurant_cuisines = []
        ratings = []
        direction = []
        delivery_times = []
        distances = []
        discount = []
        images = []
        promo = []

        for index, div in enumerate(details):
            # Extract restaurant name
            restaurant_name = div.find('p', class_='name___2epcT').text.strip()
            restaurant_names.append(restaurant_name)

            # Extract restaurant cuisine
            cuisine_div = div.find('div', class_='cuisine___T2tCh')
            cuisines = cuisine_div.text.strip() if cuisine_div else None
            restaurant_cuisines.append(cuisines)

            rating_div = div.find('div', class_='numbersChild___2qKMV')
            if rating_div.find('div', class_='ratingStar'):
                ratings.append(rating_div.text)
            else:
                ratings.append(None)

            directions = div.find_all('div', class_="numbersChild___2qKMV")
            for direction_div in directions:
                if direction_div.find('div', class_="deliveryClock"):
                    direction.append(direction_div.text)

            discount_div = div.find('div', class_="colInfo___3iLqj").find('div', class_="discount___3h-0m")
            if discount_div:
                discount.append(discount_div.text)
            else:
                discount.append(None)

            if div.find('div', class_="promoTagHead___1bjRG"):
                promo.append(True)
            else:
                promo.append(False)
            
            image = div.find('img', class_="realImage___2TyNE")
            images.append(div.find('img').get('src'))

        for x in direction:
            delivery_time, distance = x.split('•')
            delivery_times.append(delivery_time[:7])
            distances.append(distance[-6:])

        df = pd.DataFrame({
            'Restaurant Name': restaurant_names,
            'Restaurant Cuisine': restaurant_cuisines,
            'Restaurant Rating': ratings,
            'Restaurant Delivery Time': delivery_times,
            'Restaurant Distance': distances,
            'Discount': discount,
            'Promo': promo,
            'Images' : images
        })

        return df

    def save_data(self, data):
        # Save extracted data to a CSV file and a gzipped JSON file
        filename = f"grab_food_data.ndjson.gz"
        data.to_csv('data.csv')
        # Check if the file already exists
        try:
            with gzip.open(filename, 'xb') as f:
                for record in data.to_dict('records'):
                    f.write(f"{record}\n".encode())
            logging.info(f"Data saved to {filename}")
        except FileExistsError:
            logging.warning(f"File '{filename}' already exists. Data not saved.")

    def run(self):
        # Execute the scraping process
        self.driver.get(self.url)
        self.accept_cookies()
        self.enter_location()
        self.scroll_to_end()
        time.sleep(25)  # Add a delay to ensure all data is loaded
        data = self.extract_data()
        self.save_data(data)
        self.driver.quit()  # Close the WebDriver when done

if __name__ == "__main__":
    url = "https://food.grab.com/sg/en"
    location = "PT Singapore - Choa Chu Kang North 6, Singapore, 689577"
    # proxies = [
    #     "117.250.3.58:8080",
    #     "35.185.196.38:3128",
    #     "113.160.166.196:6129",
    #     "13.40.37.133:4000",
    #     "8.219.97.248:80"
    # ]
    scraper = GrabFoodScraper(url, location)
    scraper.run()