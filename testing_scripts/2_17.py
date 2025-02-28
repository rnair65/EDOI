import pandas as pd
from name_matching.name_matcher import NameMatcher

keys = ["newsweek_most_responsible", "fortune_100_best_companies_to_work_for", "just_capitals_just_100", "points_of_light_civic_50"]

csv_suffix = ".csv"

values = [item + csv_suffix for item in keys]


for key, value in zip(keys, values):
    globals()[key] = pd.read_csv(f"up_to_date_data/{value}")

# print(newsweek_most_responsible, fortune_100_best_companies_to_work_for, just_capitals_just_100)  # Output: 1 2 3


# newsweek_most_responsible = pd.read_csv(f"live_data/newsweek_most_responsible_2025.csv") # Load the CSV file into a DataFrame
# fortune_100_best_companies_to_work_for = pd.read_csv(f"live_data/fortune_100_best_companies_to_work_for_2024.csv")
# just_capitals_just_100 = pd.read_csv("live_data/just_capitals_just_100.csv")
# # points_of_light_civic_500 = pd.read_csv("live_data/points_of_light_civic_500.csv")
# def adjust_find_points_of_light_civic_50():
#     # most_recent_year = data_collection.find_points_of_light_civic_50()
#     points_of_light_civic_50 = pd.read_csv("live_data/points_of_light_civic_50.csv")
points_of_light_civic_50.rename(columns={"Companies": "POINTS_OF_LIGHT_CIVIC_50"}, inplace=True)

    # return points_of_light_civic_50

# points_of_light_civic_50 = adjust_find_points_of_light_civic_50()




edoi_company_lists = {
    0: {'df': newsweek_most_responsible, 'company_col': 'COMPANY'},
    1: {'df': fortune_100_best_companies_to_work_for, 'company_col': 'NAME'},
    2: {'df': just_capitals_just_100, 'company_col': 'Company'},
    3: {'df': points_of_light_civic_50, 'company_col': 'POINTS_OF_LIGHT_CIVIC_50'}
}
# for i in edoi_company_lists:
#     print(edoi_company_lists[i]['df'][[edoi_company_lists[i]['company_col']]].head())

# list_to_variable_mapping = {
list_to_variable_mapping = {
    'newsweek_most_responsible': {
        'company_col': 'COMPANY',
        'standardized_col': 'STANDARDIZED_COMPANY',
        'df': newsweek_most_responsible
    },
    'fortune_100_best_companies': {
        'company_col': 'NAME', 
        'standardized_col': 'STANDARDIZED_COMPANY',
        'df': fortune_100_best_companies_to_work_for
    },
    'just_capitals': {
        'company_col': 'Company',
        'standardized_col': 'STANDARDIZED_COMPANY', 
        'df': just_capitals_just_100
    },
    'points_of_light_civic_50': {
        'company_col': 'POINTS_OF_LIGHT_CIVIC_50',
        'standardized_col': 'STANDARDIZED_COMPANY',
        'df': points_of_light_civic_50
    }
}

# Standardize company names across all dataframes
# First standardize company names in each dataframe
for list_name, list_info in list_to_variable_mapping.items():
    df = list_info['df']
    company_col = list_info['company_col']
    
    # Create standardized company name column
    df[list_info['standardized_col']] = (
        df[company_col].str.lower()  # Convert to lowercase
        .str.replace(r'[^\w\s]', '', regex=True)  # Remove special characters
        .str.strip()  # Remove leading/trailing whitespace
        .str.replace(r'\s+', ' ', regex=True)  # Normalize spaces
        # Remove common business suffixes and words
        .str.replace(r'\b(inc|incorporated|corp|corporation|ltd|limited|llc|llp|lp|co|company|group|holdings|holding|plc|ag|sa|nv|gmbh)\b', '', regex=True)
        .str.strip()
    )

# Now merge the dataframes based on standardized company names
merged_df = list_to_variable_mapping['newsweek_most_responsible']['df']

# Merge with Fortune 100
merged_df = pd.merge(
    merged_df,
    list_to_variable_mapping['fortune_100_best_companies']['df'],
    how='outer',
    left_on='STANDARDIZED_COMPANY',
    right_on='STANDARDIZED_COMPANY',
    suffixes=('_newsweek', '_fortune')
)

# Merge with Just Capitals
merged_df = pd.merge(
    merged_df,
    list_to_variable_mapping['just_capitals']['df'],
    how='outer',
    left_on='STANDARDIZED_COMPANY',
    right_on='STANDARDIZED_COMPANY',
    suffixes=('', '_just')
    )

# Merge with Points of Light Civic 50
merged_df = pd.merge(
    merged_df,
    list_to_variable_mapping['points_of_light_civic_50']['df'],
    how='outer',
    left_on='STANDARDIZED_COMPANY',
    right_on='STANDARDIZED_COMPANY',
    suffixes=('', '_points_of_light')
)

# Convert Points of Light column to binary (0/1)
merged_df['POINTS_OF_LIGHT_CIVIC_50'] = merged_df['POINTS_OF_LIGHT_CIVIC_50'].notna().astype(int)

print(merged_df)
merged_df.to_csv("2_20_output.csv", index=False)

# }

