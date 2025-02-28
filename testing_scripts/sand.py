from fuzzywuzzy import process
import pandas as pd

import pandas as pd
from name_matching.name_matcher import NameMatcher
import pandas as pd
import unicodedata
import re
from cleanco import basename
# import data_collection

import requests
from bs4 import BeautifulSoup
import pandas as pd


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


# most_recent_year = data_collection.find_newsweek_most_responsible() # Updates live data
newsweek_most_responsible = pd.read_csv("static_data/newsweek_most_responsible_2025.csv") # Load the CSV file into a DataFrame
newsweek_most_responsible.rename(columns={"RANK": f"NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"}, inplace=True) # Rename RANK column to a universally usable column for the final dataframe

# Rank on the actual list contains asterisks that modify true length
# Using row number allows for usable rank number with minimal computation
newsweek_most_responsible[f"NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"] = newsweek_most_responsible.index + 1

# Calculate percentile of rank: 1 - (rank/ # of companies)
newsweek_most_responsible["(Percentile Rank) Newsweek Most Responsible Companies"] = 1 - (newsweek_most_responsible[f"NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"] / len(newsweek_most_responsible))
# Standardize column names
newsweek_most_responsible["STANDARDIZED_COMPANY"] = newsweek_most_responsible["COMPANY"].str.lower() # Make everything lowercase
newsweek_most_responsible["STANDARDIZED_COMPANY"] = newsweek_most_responsible["STANDARDIZED_COMPANY"].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode()) # Ignore ASCII
newsweek_most_responsible["STANDARDIZED_COMPANY"] = newsweek_most_responsible["STANDARDIZED_COMPANY"].apply(lambda x: re.sub(r'[^\w\s]','',x)) # Remove punctuation
# Fix below
newsweek_most_responsible["STANDARDIZED_COMPANY"] = newsweek_most_responsible["STANDARDIZED_COMPANY"].apply(lambda x: basename(x)) # Remove business suffixes
print(newsweek_most_responsible["STANDARDIZED_COMPANY"])
# newsweek_most_responsible["STANDARDIZED_COMPANY"] = newsweek_most_responsible["STANDARDIZED_COMPANY"].apply(lambda x: ' '.join(re.sub(r'\b{}\b'.format(re.escape(suffix)), '', x).split()))


fortune_100_best_companies_to_work_for = pd.read_csv(f"static_data/fortune_100_best_companies_to_work_for_2024.csv")
fortune_100_best_companies_to_work_for.rename(columns={"RANK": f"FORTUNE_100_BEST_COMPANIES_TO_WORK_FOR_2024_RANK"}, inplace=True)

# Find rank
fortune_100_best_companies_to_work_for[f"FORTUNE_100_BEST_COMPANIES_TO_WORK_FOR_2024_RANK"] = fortune_100_best_companies_to_work_for.index + 1


fortune_100_best_companies_to_work_for["STANDARDIZED_COMPANY"] = fortune_100_best_companies_to_work_for["NAME"].str.lower() # Make everything lowercase
fortune_100_best_companies_to_work_for["STANDARDIZED_COMPANY"] = fortune_100_best_companies_to_work_for["STANDARDIZED_COMPANY"].apply(lambda x: unicodedata.normalize('NFKD', x).encode('ASCII', 'ignore').decode()) # Ignore ASCII
fortune_100_best_companies_to_work_for["STANDARDIZED_COMPANY"] = fortune_100_best_companies_to_work_for["STANDARDIZED_COMPANY"].apply(lambda x: re.sub(r'[^\w\s]','',x)) # Remove punctuation
# Fix below
fortune_100_best_companies_to_work_for["STANDARDIZED_COMPANY"] = fortune_100_best_companies_to_work_for["STANDARDIZED_COMPANY"].apply(lambda x: basename(x)) # Remove business suffixes
print(fortune_100_best_companies_to_work_for["STANDARDIZED_COMPANY"])

def fuzzy_merge(df1, df2, key1, key2, threshold=90):
    matches = []
    for row1 in df1[key1]:
        match, score, _ = process.extractOne(row1, df2[key2])
        if score >= threshold:
            matches.append(match)
        else:
            matches.append(None)
    df1['match'] = matches
    return pd.merge(df1, df2, left_on='match', right_on=key2, how='left')

merged_df = fuzzy_merge(newsweek_most_responsible, fortune_100_best_companies_to_work_for, 'STANDARDIZED_COMPANY', 'STANDARDIZED_COMPANY')

# Clean up
# merged_df = merged_df.drop(columns=['STANDARDIZED_COMPANY', 'match'])

# print(merged_df)
mini_df = merged_df[["STANDARDIZED_COMPANY_x", "STANDARDIZED_COMPANY_y", "match", "COMPANY", "NAME", "NEWSWEEK_MOST_RESPONSIBLE_2025_RANK", "FORTUNE_100_BEST_COMPANIES_TO_WORK_FOR_2024_RANK"]]

print(merged_df.columns.tolist())
mini_df.to_csv("testingFuzzyWuzzy_.csv", index=False)

# # driver = webdriver.Chrome()
# chrome_options = webdriver.ChromeOptions()

# chrome_options.add_argument("--disable-notifications")

# # Initialize WebDriver with options
# driver = webdriver.Chrome(options=chrome_options)

# driver.get("https://fortune.com/ranking/best-companies/2024/")

# time.sleep(10)

# rows_listed = driver.find_element("xpath", '//*[@id="search-section"]/div/div[3]/div[2]/div[2]/span[2]/div/button')
# rows_listed.click()
# # rows_listed.send_keys(Keys.ENTER)

# time.sleep(3)

# set_100_rows = driver.find_element("xpath", "//li[contains(text(), '100 Rows')]")
# set_100_rows.click()
# set_100_rows.send_keys(Keys.ENTER)

# time.sleep(5)


# table = driver.find_element('xpath', '//*[@id="search-section"]/div/div[3]/div[1]/table')
# df = pd.read_html(table.get_attribute('outerHTML'))[0]  # Convert to DataFrame
# df.columns = df.columns.str.replace(r'^Remove', '', regex=True)

# df.to_csv("output.csv", index=False)
# # df = pd.read_html(table.get_attribute('outerHTML'))[0]  # Convert to DataFrame
# # df.to_csv("output.csv", index=False)
# time.sleep(5)

# driver.quit()



# # response = requests.get('https://fortune.com/ranking/best-companies/2024/')
# # response.raise_for_status()
# # soup = BeautifulSoup(response.content, 'html.parser')
# # # <div class=​"sc-617fa5cf-0 dffoiv">
# # # Find the components table
# # table = soup.find('div', {'class': 'sc-617fa5cf-0 dffoiv'})
# # print(table)
# # if not table:
# #     raise ValueError("Components table not found on TradingView page")

# # # Extract symbols from the table
# # constituents = set()
# # rows = table.find_all('tr', {'class': 'row-RdUXZpkv'})