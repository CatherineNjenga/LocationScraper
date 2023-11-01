# imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv


# choosing chrome as default browser
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

#zip codes excel worksgeet
file_path = r"C:\Users\Toshiba\Desktop\HelloData\zip_code_database.xlsx"

# DataFrames
df = pd.read_excel(file_path,  usecols='B,H', dtype='string')
header = ['Pharmacy Name', 'address', 'phone number', 'website', 'business hours', 'pham services']

with open('ScraperDataSet.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

data_len = len(df)
count = 0

# webpage scraper
def scraper():
    driver.get("https://www.bullseyelocations.com/pages/locator-with-services-vR?f=1")
    text_input = driver.find_element("id","txtCityStateZip")
    text_input.clear()
    text_input.send_keys(df.zip[count])
    dropdown = Select(driver.find_element("name", "ctl00$ContentPlaceHolder1$radiusList"))
    dropdown.select_by_value("50")

    """
        useful if one needs to manually click on the search button
        Currently the website auto clicks the search button
    """
    #search_button = driver.find_element("id", "ContentPlaceHolder1_searchButton2")
    #search_button.click()

    #try-except block for timed-out error
    try:
        time = 10
        # Alternative method but less effective in preventing program crashes.
        #WebDriverWait(driver, time).until(EC.visibility_of_element_located((By.CLASS_NAME, 'jcarousel-item')))
        WebDriverWait(driver, timeout=10, poll_frequency=0.5, ignored_exceptions=[TimeoutException]).until(EC.visibility_of_element_located((By.CLASS_NAME, "jcarousel-item")))
    except:
        pass

    # Use BeautifulSoup to get the webpage
    page = BeautifulSoup(driver.page_source, "html.parser")
    phams_container = page.find("ul", class_="resultsList")
    phams_list = phams_container.find_all("li", class_="jcarousel-item")

    for pham in phams_list:
        name = pham.find("h3").text.strip()
        address = pham.find("span", itemprop="streetAddress").text.strip()
        telephone = pham.find("span", itemprop="telephone").text.strip()
        website = pham.find("a", id="website").attrs['href'].strip()
        hours_container = pham.find("div", itemprop="openingHoursSpecification")
        business_hours = hours_container.find("meta").attrs["content"]
        services = pham.find("ul", class_="categoryWrapInner")
        services_list = services.find_all("li")
        pham_details = [name, address, telephone, website, business_hours]
        services = ''

        for service in services_list:
            pham_services = service.find_all("span", class_="categoryLabel")

            for pham in pham_services:
                pham = pham.text
                services += pham + ', '

        # Truncate the trailing comma and space on the last element on services string     
        services = services[:-2]
        pham_details.append(services)  
       
        # Save the scraped details in a csv file created previously
        import csv
        with open('ScraperDataSet.csv', 'a', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(pham_details)

        # Not necessary since chrome auto closes the driver, might be useful for other browsers.
        #driver.close()

# Automation of zip-codes access from the excel worksheet
while(count < data_len):
    scraper()
    count = count + 1
    time.sleep(60)



