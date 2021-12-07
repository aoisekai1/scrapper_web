import time
import sys
import os
from pandas.core.indexes.base import Index
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from urllib.parse import parse_qs

import pandas as pd

global str

browser = webdriver.Chrome()

# url_name = input('Input url: ')

# print(url_name)

url = "https://www.tokopedia.com/search?st=product&q=samsung&navsource=home"
url_page = 'https://www.tokopedia.com/search?navsource=home&page=2&q=samsung&source=universe&srp_component_id=02.02.02.01&st=product'
# parsed_url = urlparse(url)

# try:
#     page = parse_qs(parsed_url.query)['page'][0]
# except KeyError:
#     page = 'null'

# def test_store(url):
#     browser.get(url)

  


# test_store(url)

def scrapper(url):
    dataTittles = []
    dataPrices = []
    dataStores = []
    dataLocations = []
    dataRates = []
    dataSells = []
    dataLinks = []
    browser.get(url)

    status = False
    finished = False
    print("Please wait....")
    try:
        data_not_found =  browser.find_element(By.CLASS_NAME,'css-1muhkix').text
        status = True
        if data_not_found:
            print('Data not found in page')
            browser.quit()
            sys.exit()
        else:
            status = False
    
    except  NoSuchElementException:
        status = False

    if not status:
        time.sleep(2)
        screen_height = browser.execute_script("return window.screen.height")
        i=0
        n=0
        
        while True:

            # scroll one screen height each time
            browser.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
            i += 1
            # print(screen_height)
            time.sleep(2)
            # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
            scroll_height = browser.execute_script("return document.body.scrollHeight;")  
            # Break the loop when the height we need to scroll to is larger than the total scroll heigh 
            
            if (screen_height) * i > scroll_height:
                print("Started scraping...")
                products = browser.find_elements(By.CLASS_NAME, 'css-akzs43')
                count_products = len(products)
                x = 0
                for product in products:
                    x = x+1
                    title = product.find_element(By.CLASS_NAME, 'css-1f4mp12').text
                    price = product.find_element(By.CLASS_NAME, 'css-rhd610').text

                    #Check no such element for rate and return null
                    try:
                        rate = product.find_element(By.CLASS_NAME, 'css-etd83i').text
                    except NoSuchElementException:
                        rate = 'null'
                    
                    try:
                        sell = product.find_element(By.CLASS_NAME, 'css-1kgbcz0').text
                    except NoSuchElementException:
                        sell = 'null'

                    try:
                        if x <= 15:
                            store = browser.find_element(By.CSS_SELECTOR,'#zeus-root > div > div.css-jau1bt > div > div.css-rjanld > div:nth-child(4) > div:nth-child(1) > div:nth-child('+str(x)+') > div > div > div > div > div > div.css-1sxqhh0 > a > div.css-vogbyu > div.css-1ktbh56 > div > span:nth-child(2)').text
                        else:
                            n = n+1
                            store = browser.find_element(By.CSS_SELECTOR,'#zeus-root > div > div.css-jau1bt > div > div.css-rjanld > div:nth-child(4) > div:nth-child(2) > div:nth-child('+str(n)+') > div > div > div > div > div > div.css-1sxqhh0 > a > div.css-vogbyu > div.css-1ktbh56 > div > span:nth-child(2)').text
                    except NoSuchElementException:
                        store = "null"
                    
                    try:
                        link = product.find_element(By.CLASS_NAME,'pcv3__info-content').get_attribute('href')
                    except NoSuchElementException:
                        link = 'null'
                    
                    # link = product.find.element(By.CLASS_NAME, '')
                    if count_products == x :
                        finished = True
                    
                    dataTittles.append(title)
                    dataPrices.append(price)
                    dataRates.append(rate)
                    dataSells.append(sell)
                    dataLinks.append(link)
                    dataStores.append(store)

                print('Finished')
                if finished:
                    toCSV(dataTittles, dataPrices,dataStores,dataRates,dataSells,dataLinks)
                    browser.quit()
                break        
        
    
def toCSV(allTitles, allPrice, allStore, allRate, allSell, allLink):
    df = pd.DataFrame({"Product Name":allTitles, "Price":allPrice, "Store":allStore, "Rate":allRate,"Selling":allSell, "Link":allLink})
    df.to_csv("Data_Joran._Tokped.csv", index=False)
    print(df)

scrapper(url)



# allProducts=browser.find_elements(By.CLASS_NAME, 'css-akzs43')
# lenProducs=len(allProducts)
# n = 0
# for x in range(lenProducs):
#     x = x+1
#     if x <= 15:
#         store = browser.find_element(By.CSS_SELECTOR,'#zeus-root > div > div.css-jau1bt > div > div.css-rjanld > div:nth-child(4) > div:nth-child(1) > div:nth-child('+str(x)+') > div > div > div > div > div > div.css-1sxqhh0 > a > div.css-vogbyu > div.css-1ktbh56 > div > span:nth-child(2)')
#     else:
#         n = n+1
#         print(n)
#         # store = browser.find_element(By.CSS_SELECTOR,'#zeus-root > div > div.css-jau1bt > div > div.css-rjanld > div:nth-child(4) > div:nth-child(2) > div:nth-child('+str(n)+') > div > div > div > div > div > div.css-1sxqhh0 > a > div.css-vogbyu > div.css-1ktbh56 > div > span:nth-child(2)')

#     print(store.text)