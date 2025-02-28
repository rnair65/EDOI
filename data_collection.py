import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

import pandas as pd
import requests
import re

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-notifications") # Disable popups
chrome_options.add_argument("--incognito")  # Enable incognito mode

# Uncomment below if you do not want chrome to pop up
chrome_options.add_argument("--headless")  # Run in headless mode



# Initialize WebDriver with options
driver = webdriver.Chrome(options=chrome_options)

# Get the current year
current_year = datetime.datetime.now().year

# Create a list of 10 years starting from the current year
years = [current_year - i for i in range(10)]

# # Iterate through the years and check the URL

########################### ESG #######################################

def find_most_recent_data(base_url, year_placeholder="{current_year}"):
    for year in years:
        # Replace the placeholder with the current year
        url = base_url.replace(year_placeholder, str(year))
        response = requests.get(url)
        time.sleep(2)
        
        if (199 < response.status_code < 300) or (response.status_code == 403):  # 200 means the page exists
            print(f"Active page found: {url}")

            return url
        else:
            print(f"Page not found: {url}")
            print(response.status_code)

def find_most_recent_year(base_url, year_placeholder="{current_year}"):
    for year in years:
        # Replace the placeholder with the current year
        url = base_url.replace(year_placeholder, str(year))
        response = requests.get(url)
        time.sleep(2)
        
        if (199 < response.status_code < 300) or (response.status_code == 403):  # 200 means the page exists
            # print(f"Active page found: {url}")

            return year
        else:
            # print(f"Page not found: {url}")
            print(response.status_code)

def find_fortune_100_best_companies_to_work_for(): # Functional

    # Change if URL structure changes
    base_url = 'https://fortune.com/ranking/best-companies/{current_year}/'

    most_recent_url = find_most_recent_data(base_url)
    most_recent_year = find_most_recent_year(base_url)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(most_recent_url)

    time.sleep(10)

    rows_listed = driver.find_element("xpath", '//*[@id="search-section"]/div/div[3]/div[2]/div[2]/span[2]/div/button')
    rows_listed.click()

    time.sleep(3)

    set_100_rows = driver.find_element("xpath", "//li[contains(text(), '100 Rows')]")
    set_100_rows.click()
    set_100_rows.send_keys(Keys.ENTER)

    time.sleep(5)

    table = driver.find_element('xpath', '//*[@id="search-section"]/div/div[3]/div[1]/table')
    df = pd.read_html(table.get_attribute('outerHTML'))[0]  # Convert to DataFrame
    df.columns = df.columns.str.replace(r'^Remove', '', regex=True)
    # Convert all column names to uppercase
    df.columns = df.columns.str.upper()

    df.to_csv(f"live_data/fortune_100_best_companies_to_work_for_{most_recent_year}.csv", index=False)

    time.sleep(5)

    driver.close()

    time.sleep(5)

    return most_recent_year


def find_newsweek_most_responsible(): # Functional

    base_url = 'https://www.newsweek.com/rankings/americas-most-responsible-companies-{current_year}'

    most_recent_url = find_most_recent_data(base_url)
    most_recent_year = find_most_recent_year(base_url)

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(most_recent_url)

    time.sleep(10)

    table = driver.find_element("xpath", '//*[@id="block-ibtmedia-rankings-rankings-service-header"]/div/div/div/div/div/div[2]/table')

    df = pd.read_html(table.get_attribute('outerHTML'))[0]  # Convert to DataFrame
    # df.columns = df.columns.str.replace(r'^Remove', '', regex=True)
    # Convert all column names to uppercase
    df.columns = df.columns.str.upper()

    df.to_csv(f"live_data/newsweek_most_responsible_{most_recent_year}.csv", index=False)

    time.sleep(5)

    driver.close()

    time.sleep(5)

    return most_recent_year



def find_just_capitals_just_100(): # Functional
    base_url = 'https://justcapital.com/rankings/'
    most_recent_url = find_most_recent_data(base_url)
    most_recent_year = find_most_recent_year(base_url)

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(most_recent_url)

    time.sleep(10)

    table = driver.find_element("xpath", '//*[@id="rankings"]')

    # Find the ul element
    ul_element = driver.find_element(By.XPATH, '//*[@id="rankings"]')

    # Get all li elements within ul
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    # Extract text and split into columns
    data = [li.text.split("\n") for li in li_elements if len(li.text.split("\n")) == 3]

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Rank", "Company", "Industry"])

    # Convert Rank to integer
    df["Rank"] = pd.to_numeric(df["Rank"], errors="coerce")
    
    df.to_csv(f"live_data/just_capitals_just_100.csv", index=False)

    return most_recent_year



def find_points_of_light_civic_50(): # Functional

    base_url = 'https://www.pointsoflight.org/the-civic-50-honorees/'
    most_recent_url = find_most_recent_data(base_url)
    most_recent_year = find_most_recent_year(base_url)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(most_recent_url)

    time.sleep(10)

    # Find the ul element
    ul_element = driver.find_element(By.XPATH, '//*[@id="content"]/section[2]/div/ul')

    # Get all li elements within ul
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    # Extract text from each li element
    data = [li.text for li in li_elements]

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Companies"])
    df['Companies'] = df['Companies'].str.split('\n').str[0]

    df.to_csv(f"live_data/points_of_light_civic_50.csv", index=False)

    return most_recent_year

def find_cecp_affiliated(): # Needs work
    base_url = 'https://cecp.co/affiliation/affiliated-companies/'
    most_recent_url = find_most_recent_data(base_url)
    most_recent_year = find_most_recent_year(base_url)

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(most_recent_url)

    time.sleep(10)

    # Find the ul element
    ul_element = driver.find_element(By.XPATH, '//*[@id="panel-3526-0-0-0"]/section/div/ul')

    # Get all li elements within ul
    li_elements = ul_element.find_elements(By.TAG_NAME, "li")

    # Extract text from each li element
    data = [li.text for li in li_elements]

    # Create DataFrame
    df = pd.DataFrame(data, columns=["Companies"])
    df['Companies'] = df['Companies'].str.split('\n').str[0]
    print(df)

    # df.to_csv(f"live_data/cecp_affiliated.csv", index=False)

    return most_recent_year


def find_barrons_100_most_sustainable(): # Needs work

    base_url = 'https://www.barrons.com/lists-rankings/top-sustainable-companies/{current_year}?page=1&mod=faranking_{current_year}'

    
    most_recent_url = find_most_recent_data(base_url)
    most_recent_year = find_most_recent_year(base_url)

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(most_recent_url)

    time.sleep(10)

    table = driver.find_element("xpath", '//*[@id="ranking-table"]/div[2]/table')

    page_number = driver.find_element('xpath', '//*[@id="ranking-table"]/div[2]/table/tbody/tr[11]/td/div/div/div/div')
    page_number.click()


    return most_recent_year

    # # Convert all column names to uppercase
    # df.columns = df.columns.str.upper()

########################### Sustainability #######################################


# find_fortune_100_best_companies_to_work_for()
# find_newsweek_most_responsible()
# find_just_capitals_just_100()
# find_points_of_light_civic_50()
# find_cecp_affiliated()
# driver.quit()


