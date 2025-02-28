
import pandas as pd
from name_matching.name_matcher import NameMatcher

# Create another script that dynamically modifies live data to up_to_date_data

keys = {"newsweek_most_responsible" : "COMPANY", 
        "fortune_100_best_companies_to_work_for" : "NAME", 
        "just_capitals_just_100" : "Company", 
        "points_of_light_civic_50" : "Companies"}

csv_suffix = ".csv"

# Create list of filenames by adding .csv suffix to keys
values = [key + csv_suffix for key in keys.keys()]

# # Load CSVs into DataFrames
# for key, value in zip(keys.keys(), values):
#     globals()[key] = pd.read_csv(f"up_to_date_data/{value}")

# Create dictionary mapping keys to their DataFrames and company column names
edoi_company_lists = {}
for i, (key, company_col) in enumerate(keys.items()):
    edoi_company_lists[i] = {
        'df': f"{key}",
        'company_col': company_col
    }


list_to_variable_mapping = {}
for key, company_col in keys.items():
    df_path = f"up_to_date_data/{key}.csv"
    list_to_variable_mapping[key] = {
        'company_col': company_col,
        'standardized_col': 'STANDARDIZED_COMPANY', 
        'df': df_path
    }

# # Standardize company names across all dataframes
# # First standardize company names in each dataframe
for list_name, list_info in list_to_variable_mapping.items():
    # Load CSV into DataFrame
    df = pd.read_csv(list_info['df'])
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
    
    # Update the DataFrame in the mapping
    list_to_variable_mapping[list_name]['df'] = df

# # Now merge the dataframes based on standardized company names
# # reference_column
reference_df = lists = next(iter(keys))
merged_df = list_to_variable_mapping['newsweek_most_responsible']['df']
print(merged_df)

# merged_df = list_to_variable_mapping['newsweek_most_responsible']['df']

# print(edoi_company_lists)

# print('\n')
# print(list_to_variable_mapping)