from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from driver_path import driver_path # Create a driver_path.py file with the path to your ChromeDriver or which driver you are using ...

def scrape_the_link(website):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')

    driver = webdriver.Chrome(service=Service(driver_path), options=options)
    driver.get(website)
    website_source = driver.page_source
    driver.quit()
    return website_source

def clean_body(website_source):
    soup = BeautifulSoup(website_source, "html.parser")
    body = soup.body
    if body:
        return body.get_text(separator=' ', strip=True)
    else:
        return ""
