from fuzzywuzzy import process
import pandas as pd

import pandas as pd
from name_matching.name_matcher import NameMatcher


import requests
from bs4 import BeautifulSoup
import pandas as pd


from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# URL of the webpage
url = "https://fortune.com/ranking/best-companies/2024/"

# Set up the WebDriver (e.g., Chrome)
driver = webdriver.Chrome()  # Replace with the path to your WebDriver if needed

# Open the webpage
driver.get(url)

# Wait for the page to load (adjust the sleep time as needed)
time.sleep(10)

# Locate the table container using the provided class
table_container = driver.find_element(By.CLASS_NAME, 'sc-617fa5cf-1.dNTwEz')  # Adjust if needed

if table_container:
    # Extract table headers (if available)
    headers = [header.text for header in table_container.find_elements(By.TAG_NAME, 'th')]
    
    # Extract table rows
    rows = []
    for row in table_container.find_elements(By.TAG_NAME, 'tr'):  # Adjust if rows use a different tag
        cells = [cell.text for cell in row.find_elements(By.TAG_NAME, 'td')]
        if cells:  # Skip empty rows
            rows.append(cells)
    
    # Create a DataFrame from the extracted data
    df = pd.DataFrame(rows, columns=headers)
    
    # Display the DataFrame
    print(df)
    
    # Optionally, save the DataFrame to a CSV file
    df.to_csv('companies_table.csv', index=False)
else:
    print("Table container not found. The page structure may have changed.")

# Close the WebDriver
driver.quit()

# # URL of the webpage
# url = "https://fortune.com/ranking/best-companies/2024/"

# # Send a GET request to fetch the webpage content
# response = requests.get(url)
# # "table" class="sc-617fa5cf-1 dNTwEz">

# # Check if the request was successful
# if response.status_code == 200:
#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(response.content, 'html.parser')
    
#     # Locate the table (you may need to inspect the webpage to find the correct table tag)
#     table = soup.find('table', class_='sc-617fa5cf-1 dNTwEz')
    
#     # Extract table headers
#     headers = [header.text.strip() for header in table.find_all('th')]
    
#     # Extract table rows
#     rows = []
#     for row in table.find_all('tr')[1:]:  # Skip the header row
#         cells = [cell.text.strip() for cell in row.find_all('td')]
#         rows.append(cells)
    
#     # Create a DataFrame from the extracted data
#     df = pd.DataFrame(rows, columns=headers)
    
#     # Display the DataFrame
#     print(df)
    
#     # Optionally, save the DataFrame to a CSV file
#     df.to_csv('companies_table.csv', index=False)
# else:
#     print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# # define a dataset with bank names
# df_companies_a = pd.DataFrame({'Company name': [
#         'Industrial and Commercial Bank of China Limited',
#         'China Construction Bank',
#         'Agricultural Bank of China',
#         'Bank of China',
#         'JPMorgan Chase',
#         'Mitsubishi UFJ Financial Group',
#         'Bank of America',
#         'HSBC',
#         'BNP Paribas',
#         'Crédit Agricole']})

# # alter each of the bank names a bit to test the matching
# df_companies_b = pd.DataFrame({'name': [
#         'Bank of China Limited',
#         'Mitsubishi Financial Group',
#         'Construction Bank China',
#         'Agricultural Bank',
#         'Bank of Amerika',
#         'BNP Parisbas',
#         'JP Morgan Chase',
#         'HSCB',
#         'Industrial and Commercial Bank of China',
#         'Credite Agricole']})

# # initialise the name matcher
# matcher = NameMatcher(number_of_matches=1, 
#                       legal_suffixes=True, 
#                       common_words=False, 
#                       top_n=50, 
#                       verbose=True)

# # adjust the distance metrics to use
# matcher.set_distance_metrics(['bag', 'typo', 'refined_soundex'])

# # load the data to which the names should be matched
# matcher.load_and_process_master_data(column='Company name',
#                                      df_matching_data=df_companies_a, 
#                                      transform=True)

# # perform the name matching on the data you want matched
# matches = matcher.match_names(to_be_matched=df_companies_b, 
#                               column_matching='name')

# # combine the datasets based on the matches
# combined = pd.merge(df_companies_a, matches, how='left', left_index=True, right_on='match_index')
# combined = pd.merge(combined, df_companies_b, how='left', left_index=True, right_index=True)
# print(combined)


# import yfinance as yf

# data = yf.download("AAPL", start="2020-01-01", end="2021-01-01")
# print(data.head())

# Example datasets
# df1 = pd.DataFrame({'Company': ['Apple Inc', 'Microsoft Corp', 'Tesla'], 'Value': [1, 2, 3]})
# df2 = pd.DataFrame({'Company': ['Apple', 'Mcrosoft Corporation', 'Tesla Motors'], 'Score': [10, 20, 30]})

# # Function to find best match
# def fuzzy_merge(df1, df2, key1, key2, threshold=80):
#     matches = df1[key1].apply(lambda x: process.extractOne(x, df2[key2], score_cutoff=threshold))
#     df1['Best Match'] = matches.apply(lambda x: x[0] if x else None)
#     return df1.merge(df2, left_on='Best Match', right_on=key2, how='left')

# # Apply fuzzy matching
# merged_df = fuzzy_merge(df1, df2, 'Company', 'Company')
# print(merged_df)
