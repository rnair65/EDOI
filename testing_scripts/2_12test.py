import pandas as pd
from fuzzywuzzy import process, fuzz




import pandas as pd
from fuzzywuzzy import process, fuzz

# Sample datasets
df1 = pd.read_csv('static_data/newsweek_most_responsible_2025.csv')
df1 = df1[['RANK', 'COMPANY']]
df3 = pd.read_csv('static_data/just_capitals_just_100_2024.csv')

df4 = pd.read_csv('static_data/fortune_500_2024.csv')
df4 = df4[['Rank', 'Company']]
df5 = pd.read_csv('static_data/barrons_100_most_sustainable_2024.csv')
df5 = df5[['2024 RANK', 'COMPANY', 'TICKER']]
df6 = pd.read_csv('static_data/fortune_100_best_companies_to_work_for_2024.csv')
df6 = df6[['RANK', 'NAME']]

df1.rename(columns={"RANK": f"NEWSWEEK_MOST_RESPONSIBLE_RANK"}, inplace=True)
df3.rename(columns={"RANK": f"JUST_CAPITALS_RANK"}, inplace=True)
df4.rename(columns={"Rank": f"FORTUNE_500_RANK"}, inplace=True)
df5.rename(columns={"2024 RANK": f"BARRONS_100_RANK"}, inplace=True)
df6.rename(columns={"RANK": f"FORTUNE_100_BEST_COMPANIES_RANK"}, inplace=True)



# Function to normalize company names
def normalize_name(name):
    return ''.join(e for e in name if e.isalnum()).lower()

# Apply normalization to all datasets with unique column names
df1['normalized_name_1'] = df1['COMPANY'].apply(normalize_name)
df3['normalized_name_3'] = df3['COMPANY'].apply(normalize_name)
df4['normalized_name_4'] = df4['Company'].apply(normalize_name)
df5['normalized_name_5'] = df5['COMPANY'].apply(normalize_name)
df6['normalized_name_6'] = df6['NAME'].apply(normalize_name)

# Fuzzy matching function
def match_names(row, choices, scorer=fuzz.ratio, cutoff=80):
    match = process.extractOne(row[1], choices, scorer=scorer)
    if match and match[1] >= cutoff:
        return match[0]
    return None

# Create a list of all unique normalized names from all datasets
all_names = pd.concat([
    df1['normalized_name_1'],
    df3['normalized_name_3'],
    df4['normalized_name_4'],
    df5['normalized_name_5'],
    df6['normalized_name_6']
]).unique()

# Match names and create a common identifier for all datasets
df1['matched_name'] = df1.apply(lambda row: match_names(row, all_names), axis=1)
df3['matched_name'] = df3.apply(lambda row: match_names(row, all_names), axis=1)
df4['matched_name'] = df4.apply(lambda row: match_names(row, all_names), axis=1)
df5['matched_name'] = df5.apply(lambda row: match_names(row, all_names), axis=1)
df6['matched_name'] = df6.apply(lambda row: match_names(row, all_names), axis=1)

# Merge datasets based on matched names
merged_df = df1
for df in [df3, df4, df5, df6]:
    merged_df = pd.merge(merged_df, df, on='matched_name', how='outer', suffixes=('', '_y'))
    merged_df.drop(merged_df.filter(regex='_y$').columns.tolist(), axis=1, inplace=True)

merged_df.to_csv("2_12_output.csv", index=False)

# Count rows in each DataFrame
rows_df1 = len(df1)
rows_df3 = len(df3)
rows_df4 = len(df4)
rows_df5 = len(df5)
rows_df6 = len(df6)

# Calculate the total number of rows
total_rows = rows_df1  + rows_df3 + rows_df4 + rows_df5 + rows_df6

print(f'Total number of rows in all DataFrames: {total_rows}')



# # Sample datasets
# # data1 = {'company_name': ['Acme Inc.', 'Global Tech', 'SuperMega Corp']}
# # data2 = {'company_name': ['ACME Incorporated', 'GlobalTech', 'Super Mega Corp.']}
# newsweek_most_responsible = pd.read_csv("static_data/newsweek_most_responsible_2025.csv") # Load the CSV file into a DataFrame
# fortune_100_best_companies_to_work_for = pd.read_csv(f"static_data/fortune_100_best_companies_to_work_for_2024.csv")


# df1 = pd.DataFrame(newsweek_most_responsible)
# df2 = pd.DataFrame(fortune_100_best_companies_to_work_for)

# # Function to normalize company names
# def normalize_name(name):
#     return ''.join(e for e in name if e.isalnum()).lower()

# # Apply normalization
# df1['normalized_name'] = df1['COMPANY'].apply(normalize_name)
# df2['normalized_name'] = df2['NAME'].apply(normalize_name)

# # Fuzzy matching
# def match_names(row, choices, scorer=fuzz.ratio, cutoff=80):
#     match = process.extractOne(row['normalized_name'], choices, scorer=scorer)
#     if match and match[1] >= cutoff:
#         return match[0]
#     return None

# choices = df2['normalized_name'].tolist()
# df1['matched_name'] = df1.apply(match_names, axis=1, choices=choices)

# # Merge datasets based on matched names
# merged_df = pd.merge(df1, df2, left_on='matched_name', right_on='normalized_name', how='left', suffixes=('_1', '_2'))



# print(merged_df)

