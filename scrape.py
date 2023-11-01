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

file_path = r"C:\Users\Toshiba\Desktop\HelloData\zip_code_database.xlsx"

# DataFrames
df = pd.read_excel(file_path,  usecols='B,H', dtype='string')
#df_pham = pd.DataFrame(columns=['Pharmacy Name', 'address', 'phone number', 'website', 'business hours', 'pham services'])
header = ['Pharmacy Name', 'address', 'phone number', 'website', 'business hours', 'pham services']

with open('ScraperDataSet.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

data_len = len(df)
count = 0

# webpage
def scraper():
    driver.get("https://www.bullseyelocations.com/pages/locator-with-services-vR?f=1")
    text_input = driver.find_element("id","txtCityStateZip")
    text_input.clear()
    text_input.send_keys(df.zip[count])
    dropdown = Select(driver.find_element("name", "ctl00$ContentPlaceHolder1$radiusList"))
    dropdown.select_by_value("50")
    #dropdown2 = Select(driver.find_element("name", "ctl00$ContentPlaceHolder1$ddlCategories"))
    #dropdown2.select_by_value("50")
    #search_button = driver.find_element("id", "ContentPlaceHolder1_searchButton2")
    #search_button.click()
    #driver.page_source
    #try-except for timed-out error
    try:
        time = 10
        #WebDriverWait(driver, time).until(EC.visibility_of_element_located((By.CLASS_NAME, 'jcarousel-item')))
        WebDriverWait(driver, timeout=10, poll_frequency=0.5, ignored_exceptions=[TimeoutException]).until(EC.visibility_of_element_located((By.CLASS_NAME, "jcarousel-item")))
    except:
        pass
    page = BeautifulSoup(driver.page_source, "html.parser")
    phams_container = page.find("ul", class_="resultsList")

    #phams_container = page.find(id ="resultsCarouselWide")
    #print(phams_container)
    phams_list = phams_container.find_all("li", class_="jcarousel-item")
    #print(phams_list)

    for pham in phams_list:
        #pham = item.find("div", class_="itemWrap")
        name = pham.find("h3").text.strip()
        address = pham.find("span", itemprop="streetAddress").text.strip()
        telephone = pham.find("span", itemprop="telephone").text.strip()
        website = pham.find("a", id="website").attrs['href'].strip()
        hours_container = pham.find("div", itemprop="openingHoursSpecification")
        business_hours = hours_container.find("meta").attrs["content"]
        #print("name", name)
        #print("address", address)
        #print("telephone", telephone)
        #print("website", website)
        #print("business hours", business_hours)
        services = pham.find("ul", class_="categoryWrapInner")
        services_list = services.find_all("li")
        pham_details = [name, address, telephone, website, business_hours]
        #pham_service = []
        services = ''
        #length = len(df_pham)
        #pham_details = [name, address, telephone, website, business_hours]
        for service in services_list:
            pham_services = service.find_all("span", class_="categoryLabel")
            for pham in pham_services:
                pham = pham.text
                services += pham + ', '
        print(services)      
        services = services[:-2]
        pham_details.append(services)  
        #pham_details = [name, address, telephone, website, business_hours, pham_service]
        #print(pham_details)
                #df_pham
        #print(length)
        #df_pham.loc[length] = pham_details
        #time.sleep(120)
        #pham_details = [name, address, telephone, website, business_hours, pham_service]

        import csv
        with open('ScraperDataSet.csv', 'a', newline='', encoding='UTF8') as f:
            writer = csv.writer(f)
            writer.writerow(pham_details)


#count = count + 1

      #driver.close()

while(count < data_len):
    scraper()
    count = count + 1
    time.sleep(60)



