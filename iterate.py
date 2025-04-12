import pandas as pd
from name_matching.name_matcher import NameMatcher
import weights

# Create another script that dynamically modifies live data to up_to_date_data

keys = {"newsweek_most_responsible" : "COMPANY", 
        "fortune_100_best_companies_to_work_for" : "NAME", 
        "just_capitals_just_100" : "Company", 
        "points_of_light_civic_50" : "Companies"}

csv_suffix = ".csv"

def define_file_paths():
    # Create list of filenames by adding .csv suffix to keys
    values = [key + csv_suffix for key in keys.keys()]
    print(f'Values: {values} \n')

    return values

def create_edoi_company_lists():
    # Create dictionary mapping keys to their DataFrames and company column names
    edoi_company_lists = {}
    for i, (key, company_col) in enumerate(keys.items()):
        edoi_company_lists[i] = {
            'df': f"{key}",
            'company_col': company_col
        }

    return edoi_company_lists

def create_list_to_variable_mapping():
    list_to_variable_mapping = {}
    for key, company_col in keys.items():
        df_path = f"up_to_date_data/{key}.csv"
        list_to_variable_mapping[key] = {
            'company_col': company_col,
            'standardized_col': 'STANDARDIZED_COMPANY', 
            'df': df_path
                }
        



################## Calculations ##########################
def gather_weights():
    algorithm = weights.return_algorithm()

# ORacle: ASUEDOIndex25
    
def main():
    # 1. Connect to database
    # 2a. If Database lists all match with keys then continue to calculation
    # 2b. If there are new lists, add them to the Database
    # 3. Calculate EDOI Index based on lists

    return None
    
if __name__ == "__main__":
    main()
# print(f'List to Variable Mapping: {list_to_variable_mapping} \n')

# Standardize compan