# web_testing.py

import time
import logging
import ssl
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Ensure SSL is properly loaded (if needed for your environment)
ssl._create_default_https_context = ssl._create_unverified_context

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def init_driver():
    """
    Initializes a headless Chrome driver with custom options.
    """
    options = Options()
    options.add_argument("--headless")  # Run in headless mode for speed
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Disable GPU acceleration
    options.add_argument("--remote-debugging-port=9222")  # Enable debugging

    # Assumes that the ChromeDriver executable is in your PATH.
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def test_login(driver, url, username, password):
    """
    Tests login functionality by navigating to the given URL and attempting to log in.
    """
    try:
        driver.get(url)
        time.sleep(2)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password + Keys.RETURN)
        time.sleep(2)
        
        if "dashboard" in driver.current_url:
            logging.info("Login test passed.")
            return True
        else:
            logging.error("Login test failed.")
            return False
    except Exception as e:
        logging.error(f"Login test error: {str(e)}")
        return str(e)

def test_page_load(driver, url):
    """
    Measures the page load time for the given URL.
    Returns the load time in seconds or an error message.
    """
    try:
        start_time = time.time()
        driver.get(url)
        end_time = time.time()
        load_time = end_time - start_time
        logging.info(f"Page load time for {url}: {load_time:.2f} seconds")
        return load_time
    except Exception as e:
        logging.error(f"Page load error for {url}: {str(e)}")
        return str(e)

def run_web_tests():
    """
    Runs automated web tests on a set of URLs and returns the results.
    """
    urls = [
        "https://automationteststore.com/",  # Example e-commerce site
        "https://demo.opencart.com/",         # OpenCart Demo
        "https://www.saucedemo.com/"           # SauceDemo
    ]
    
    driver = init_driver()
    test_results = []
    
    for url in urls:
        result = test_page_load(driver, url)
        test_results.append((url, result))
    
    driver.quit()
    return test_results

def save_test_results(results, filename="test_results.csv"):
    """
    Saves the test results to a CSV file.
    """
    df = pd.DataFrame(results, columns=['url', 'load_time'])
    df.to_csv(filename, index=False)
    logging.info(f"Test results saved to {filename}")
