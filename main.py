import pandas as pd
import unicodedata
import re
from cleanco import basename
import esg_mission_alignment
import sustainability_mission_alignment
import influence
import data_collection
from fuzzywuzzy import process, fuzz


# 1. Check if datasets are recent
# 2. Collect new datasets
# 3. Combine datasets (use openAI gpt to find and join on legal name)
# 4. Calculate formulas

# TDL: Create weights incorporation for calculation

# Questions: Paywall; some websites have image listed, not name

### ESG
newsweek_most_responsible = esg_mission_alignment.adjust_newsweek_most_responsible()
fortune_100_best_companies_to_work_for = esg_mission_alignment.adjust_fortune_100_best_companies_to_work_for()
just_capitals_just_100 = esg_mission_alignment.adjust_just_capitals_just_100()
points_of_light_civic_50 = esg_mission_alignment.adjust_find_points_of_light_civic_50()

# newsweek_most_responsible["NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"] = newsweek_most_responsible["NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"].astype(str)
# newsweek_most_responsible.index = newsweek_most_responsible.index.astype(str)
newsweek_most_responsible["NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"] = newsweek_most_responsible["NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"].apply(str)



### Sustainability
barrons_100_most_sustainable_2024 = sustainability_mission_alignment.barrons_100_most_sustainable_2024

### Influence
fortune_500_2024 = influence.fortune_500_2024 

# Uncomment below to test NEWSWEEK MOST RESPONSIBLE
print(newsweek_most_responsible)
print(fortune_100_best_companies_to_work_for.columns)
print(just_capitals_just_100)
print(points_of_light_civic_50)


######################## WIP #########################

# Need to work on removing inc, ltd, and other abbreviations to improve matching

# Function to normalize company names
def normalize_name(name):
    return ''.join(e.lower() for e in name if e.isalnum() or e.isspace())


# Apply normalization to all datasets with unique column names
newsweek_most_responsible['normalized_name_nmr'] = newsweek_most_responsible['COMPANY'].apply(lambda x: basename(normalize_name(x)))
fortune_100_best_companies_to_work_for['normalized_name_f100'] = fortune_100_best_companies_to_work_for['NAME'].apply(lambda x: basename(normalize_name(x)))
just_capitals_just_100['normalized_name_jc100'] = just_capitals_just_100['Company'].apply(lambda x: basename(normalize_name(x)))
points_of_light_civic_50['normalized_name_c50'] = points_of_light_civic_50['POINTS_OF_LIGHT_CIVIC_50'].apply(lambda x: basename(normalize_name(x)))
# df6['normalized_name_6'] = df6['NAME'].apply(normalize_name)

# newsweek_most_responsible['normalized_name_nmr'] = newsweek_most_responsible['normalized_name_nmr'].apply(basename)
# fortune_100_best_companies_to_work_for['normalized_name_f100'] = fortune_100_best_companies_to_work_for['normalized_name_f100'].apply(basename)
# just_capitals_just_100['normalized_name_jc100'] = just_capitals_just_100['normalized_name_jc100'].apply(basename)
# points_of_light_civic_50['normalized_name_c50'] = points_of_light_civic_50['normalized_name_c50'].apply(basename)

# Fuzzy matching function
def match_names(row, choices, scorer=fuzz.ratio, cutoff=80):
    match = process.extractOne(row[1], choices, scorer=scorer)
    if match and match[1] >= cutoff:
        return match[0]
    return None

# Create a list of all unique normalized names from all datasets
all_names = pd.concat([
    newsweek_most_responsible['normalized_name_nmr'],
    fortune_100_best_companies_to_work_for['normalized_name_f100'],
    just_capitals_just_100['normalized_name_jc100'],
    points_of_light_civic_50['normalized_name_c50']
]).unique()

# Match names and create a common identifier for all datasets
newsweek_most_responsible['matched_name'] = newsweek_most_responsible.apply(lambda row: match_names(row, all_names), axis=1)
fortune_100_best_companies_to_work_for['matched_name'] = fortune_100_best_companies_to_work_for.apply(lambda row: match_names(row, all_names), axis=1)
just_capitals_just_100['matched_name'] = just_capitals_just_100.apply(lambda row: match_names(row, all_names), axis=1)
points_of_light_civic_50['matched_name'] = points_of_light_civic_50.apply(lambda row: match_names(row, all_names), axis=1)
# df6['matched_name'] = df6.apply(lambda row: match_names(row, all_names), axis=1)

# Merge datasets based on matched names
merged_df = newsweek_most_responsible
for df in [fortune_100_best_companies_to_work_for, just_capitals_just_100, points_of_light_civic_50]:
    merged_df = pd.merge(merged_df, df, on='matched_name', how='outer', suffixes=('', '_y'))
    merged_df.drop(merged_df.filter(regex='_y$').columns.tolist(), axis=1, inplace=True)

final_df = merged_df[[
    # 'COMPANY', 
    'matched_name',
    'HQ CITY','HQ STATE','INDUSTRY', 'NEWSWEEK_MOST_RESPONSIBLE_2025_RANK', 
    'FORTUNE_100_BEST_COMPANIES_TO_WORK_FOR_2024_RANK', 'JUST_CAPITALS_JUST_100_RANK', 
    'POINTS_OF_LIGHT_CIVIC_50',  
    'normalized_name_nmr', 'normalized_name_f100',
    'normalized_name_jc100', 'normalized_name_c50'
    ]]

final_df.to_csv("2_13_output.csv", index=False)
merged_df.to_csv("Full_output.csv", index=False)
# Count rows in each DataFrame
rows_df1 = len(newsweek_most_responsible)
rows_df3 = len(fortune_100_best_companies_to_work_for)
rows_df4 = len(just_capitals_just_100)
rows_df5 = len(points_of_light_civic_50)
# rows_df6 = len(df6)

# Calculate the total number of rows
total_rows = rows_df1  + rows_df3 + rows_df4 + rows_df5 

print(f'Total number of rows in all DataFrames: {total_rows}')





# print(newsweek_most_responsible_2025[["COMPANY", "STANDARDIZED_COMPANY","NEWSWEEK_MOST_RESPONSIBLE_2025_RANK", "(Percentile Rank) Newsweek Most Responsible Companies"]].head())
# print(fortune_100_best_companies_to_work_for_2024[["NAME", "FORTUNE_100_BEST_COMPANIES_TO_WORK_FOR_2024_RANK"]])
# print(just_capitals_just_100_2024[["JUST_CAPITALS_JUST_100_2024_RANK", "COMPANY", "TICKER"]].head())
# print(barrons_100_most_sustainable_2024[["2023 RANK", "BARRONS_100_MOST_SUSTAINABLE_2024_RANK", "COMPANY"]].head())
# print(points_of_light_civic_50_2024.head())





# print(len(newsweek_most_responsible_2025))

# df["CALC CESP Level"] = df["CESP 2023 Ranking (Platinum = 3, Gold = 2, Silver = 1)"].apply(
#     lambda x: "platinum" if x == 3 else "gold" if x == 2 else "silver" if x == 1 else "none"
# )

# edoi_index = df["EDO Index"]
# company_name = df["Company Name"]
# company_legal_name = df["Company Legal Name"]
# industry = df["Industry"]
# city = df["City"]
# state = df["State"]
# zip = df["Zip"]
# website = df["Website"]
# esg_commitment = df["ESG Commitment (high=3, medium=1, low=0)"]
# newsweek_rank = df["(Rank) Newsweek Most Responsible Companies (1 - (Rank divided by 600))"]
# newsweek_responsible = df["Newsweek Most Responsible Companies (Y = 1)"]
# cecp_affiliated = df["CECP-affiliated company (Yes = 1)"]
# fortune_best_workplaces = df["Fortune 100 Best Companies to Work For (Yes = 1)"]
# forbes_just_100 = df['Forbes "Just 100" (Yes = 1)']
# newsweek_loved_workplaces = df["Newsweek America's Most loved workplaces 2024"]
# civic_50 = df['Points of Light "Civic 50" Honoree (Yes = 1)']
# sustainability_top_250 = df["Sustainability Magazine Top 250 (Yes = 1)"]
# barons_sustainable = df["Baron's 100 most sustainable companies (Yes = 1)"]
# sustainability_consortium = df["Member of The Sustainability Consortium (Yes = 1)"]
# instride_company = df["InStride Company (Yes=1)"]
# guild_company = df["Guild Company (Yes=1)"]
# edassist_company = df["EdAssist Company (Yes=1)"]
# asu_industry_excellence = df["ASU Industry of Excellence (Yes=1))"]
# most_innovative = df["Most Innovative Companies List  (Yes=1)"]
# instride_icp = df["InStride ICP"]
# companies_of_century = df['"Companies of a Century"']
# fortune_500_priority = df["Fortune 500 Priority Region (A+=4, A=3, B=2, C=1)"]
# pbj_top_50 = df["PBJ Top 50 Public Companies (Y=1)"]
# tenx_corridor = df["10X Corridor (Y=1)"]
# brand_lift = df["Brand Lift (1 = brand equity score is known and is above the median)"]
# global_footprint = df["Global Footprint (Y=1))"]
# fortune_500_rank = df["Fortune 500 Rank (1 - (Rank divided by 500))"]
# fortune_500 = df["Fortune 500 (Y = 1)"]
# cesp_2023_ranking = df["CESP 2023 Ranking (Platinum = 3, Gold = 2, Silver = 1)"]
# active_asu_employer = df['"Active" ASU employer']
# asu_supplier = df["ASU Supplier"]
# sda_level_score = df['SDA Level score (4 is strongest relationship "Tier 1")']
# c_suite_connection = df["C-Suite Connection (Y = 1))"]
# c_suite_description = df["Description of C-Suite Connection"]
# ceo = df["CEO"]
# ticker = df["Ticker"]
# price_2023 = df["12/27/2023 Price"]
# price_2024 = df["12/27/2024 Price"]
# yoy_stock_change = df["YoY change in Stock price (in %)"]
# stock_performance_percentile = df["Stock Performance Percentile"]
# desirability = df["Desirability"]
# fortune_500_priority = df["Fortune 500 Priority"]
# financial_readiness = df["Financial Readiness"]
# asu_connection = df["ASU Connection"]
# mmc_ch_c_suite = df["MMC/CH C-Suite Connection"]
# cesp_level = df["CESP Level"]

# print(df.columns.tolist())


# desirability_columns_to_sum = [
#     "ESG Commitment (high=3, medium=1, low=0)",
#     "(Rank) Newsweek Most Responsible Companies (1 - (Rank divided by 600))",
#     "Newsweek Most Responsible Companies (Y = 1)",
#     "CECP-affiliated company (Yes = 1)",
#     "Fortune 100 Best Companies to Work For (Yes = 1)",
#     'Forbes "Just 100" (Yes = 1)',
#     "Newsweek America's Most loved workplaces 2024",
#     'Points of Light "Civic 50" Honoree (Yes = 1)',
#     "Sustainability Magazine Top 250 (Yes = 1)",
#     "Baron's 100 most sustainable companies (Yes = 1)",
#     "Member of The Sustainability Consortium (Yes = 1)",
#     "InStride Company (Yes=1)",
#     "Guild Company (Yes=1)",
#     "EdAssist Company (Yes=1)",
#     "ASU Industry of Excellence (Yes=1))",
#     "Most Innovative Companies List  (Yes=1)",
#     "InStride ICP",
#     '"Companies of a Century"',
#     "Fortune 500 Priority Region (A+=4, A=3, B=2, C=1)",
#     "PBJ Top 50 Public Companies (Y=1)",
#     "10X Corridor (Y=1)",
#     "Brand Lift (1 = brand equity score is known and is above the median)",
#     "Global Footprint (Y=1))",
#     "Fortune 500 Rank (1 - (Rank divided by 500))",
#     "Fortune 500 (Y = 1)",
#     # "CESP 2023 Ranking (Platinum = 3, Gold = 2, Silver = 1)",
#     '"Active" ASU employer',
#     "ASU Supplier",
#     'SDA Level score (4 is strongest relationship "Tier 1")',
# ]

# # Ensure numeric columns are properly converted before summing
# df["CALC Desirability"] = df[desirability_columns_to_sum].apply(pd.to_numeric, errors="coerce").sum(axis=1)
# # Create the CESP Level column based on conditions
# df["CALC CESP Level"] = df["CESP 2023 Ranking (Platinum = 3, Gold = 2, Silver = 1)"].apply(
#     lambda x: "platinum" if x == 3 else "gold" if x == 2 else "silver" if x == 1 else "none"
# )


# # # Compute the EDO Index
# df["TEST EDOI Index"] = (
#     (df["CALC Desirability"] + df["Fortune 500 Priority"]) * df["Financial Readiness Adjusted"]
# ) + df["MMC/CH C-Suite Connection Adjusted"]