import pandas as pd
import openai
import time
from tqdm import tqdm

# Questions: 
# What if 2025 sheets are not updated? -> Do we use all same year or most recent?

# Specify the CSV file name (ensure it's in the same folder as the script)
file_name = "EDOIJan17Sample.csv"

# Load the CSV file into a DataFrame
df = pd.read_csv(file_name)


## Previous strategy to determine rank below:
# # Replace single and double asterisks entries with null values
# newsweek_most_responsible_2025["NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"] = pd.to_numeric(
#     newsweek_most_responsible_2025["NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"].replace(['*', '**'], pd.NA), errors='coerce'
# )

# # Fill asterisks (now null values) with the value below
# newsweek_most_responsible_2025["NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"] = newsweek_most_responsible_2025["NEWSWEEK_MOST_RESPONSIBLE_2025_RANK"].fillna(method='bfill')

def get_legal_name(company_name):
    try:
        response =  client.chat.completions.create( # openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" or "gpt-3.5-turbo"
            messages=[{"role": "system", "content": "You are an AI that provides the full official legal name of registered companies."},
                      {"role": "user", "content": f"What is the full legal name of {company_name} as registered in official U.S. business records?"}],
            max_tokens=50,
            temperature=0.2
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error fetching legal name for {company_name}: {e}")
        return None

tqdm.pandas()  # For progress tracking

# df["Legal Name"] = df["Company Name"].progress_apply(get_legal_name)


edoi_index = df["EDO Index"]
company_name = df["Company Name"]
company_legal_name = df["Company Legal Name"]
industry = df["Industry"]
city = df["City"]
state = df["State"]
zip = df["Zip"]
website = df["Website"]
esg_commitment = df["ESG Commitment (high=3, medium=1, low=0)"]
newsweek_rank = df["(Rank) Newsweek Most Responsible Companies (1 - (Rank divided by 600))"]
newsweek_responsible = df["Newsweek Most Responsible Companies (Y = 1)"]
cecp_affiliated = df["CECP-affiliated company (Yes = 1)"]
fortune_best_workplaces = df["Fortune 100 Best Companies to Work For (Yes = 1)"]
forbes_just_100 = df['Forbes "Just 100" (Yes = 1)']
newsweek_loved_workplaces = df["Newsweek America's Most loved workplaces 2024"]
civic_50 = df['Points of Light "Civic 50" Honoree (Yes = 1)']
sustainability_top_250 = df["Sustainability Magazine Top 250 (Yes = 1)"]
barons_sustainable = df["Baron's 100 most sustainable companies (Yes = 1)"]
sustainability_consortium = df["Member of The Sustainability Consortium (Yes = 1)"]
instride_company = df["InStride Company (Yes=1)"]
guild_company = df["Guild Company (Yes=1)"]
edassist_company = df["EdAssist Company (Yes=1)"]
asu_industry_excellence = df["ASU Industry of Excellence (Yes=1))"]
most_innovative = df["Most Innovative Companies List  (Yes=1)"]
instride_icp = df["InStride ICP"]
companies_of_century = df['"Companies of a Century"']
fortune_500_priority = df["Fortune 500 Priority Region (A+=4, A=3, B=2, C=1)"]
pbj_top_50 = df["PBJ Top 50 Public Companies (Y=1)"]
tenx_corridor = df["10X Corridor (Y=1)"]
brand_lift = df["Brand Lift (1 = brand equity score is known and is above the median)"]
global_footprint = df["Global Footprint (Y=1))"]
fortune_500_rank = df["Fortune 500 Rank (1 - (Rank divided by 500))"]
fortune_500 = df["Fortune 500 (Y = 1)"]
cesp_2023_ranking = df["CESP 2023 Ranking (Platinum = 3, Gold = 2, Silver = 1)"]
active_asu_employer = df['"Active" ASU employer']
asu_supplier = df["ASU Supplier"]
sda_level_score = df['SDA Level score (4 is strongest relationship "Tier 1")']
c_suite_connection = df["C-Suite Connection (Y = 1))"]
c_suite_description = df["Description of C-Suite Connection"]
ceo = df["CEO"]
ticker = df["Ticker"]
price_2023 = df["12/27/2023 Price"]
price_2024 = df["12/27/2024 Price"]
yoy_stock_change = df["YoY change in Stock price (in %)"]
stock_performance_percentile = df["Stock Performance Percentile"]
desirability = df["Desirability"]
fortune_500_priority = df["Fortune 500 Priority"]
financial_readiness = df["Financial Readiness"]
asu_connection = df["ASU Connection"]
mmc_ch_c_suite = df["MMC/CH C-Suite Connection"]
cesp_level = df["CESP Level"]

# print(df.columns.tolist())


desirability_columns_to_sum = [
    "ESG Commitment (high=3, medium=1, low=0)",
    "(Rank) Newsweek Most Responsible Companies (1 - (Rank divided by 600))",
    "Newsweek Most Responsible Companies (Y = 1)",
    "CECP-affiliated company (Yes = 1)",
    "Fortune 100 Best Companies to Work For (Yes = 1)",
    'Forbes "Just 100" (Yes = 1)',
    "Newsweek America's Most loved workplaces 2024",
    'Points of Light "Civic 50" Honoree (Yes = 1)',
    "Sustainability Magazine Top 250 (Yes = 1)",
    "Baron's 100 most sustainable companies (Yes = 1)",
    "Member of The Sustainability Consortium (Yes = 1)",
    "InStride Company (Yes=1)",
    "Guild Company (Yes=1)",
    "EdAssist Company (Yes=1)",
    "ASU Industry of Excellence (Yes=1))",
    "Most Innovative Companies List  (Yes=1)",
    "InStride ICP",
    '"Companies of a Century"',
    "Fortune 500 Priority Region (A+=4, A=3, B=2, C=1)",
    "PBJ Top 50 Public Companies (Y=1)",
    "10X Corridor (Y=1)",
    "Brand Lift (1 = brand equity score is known and is above the median)",
    "Global Footprint (Y=1))",
    "Fortune 500 Rank (1 - (Rank divided by 500))",
    "Fortune 500 (Y = 1)",
    # "CESP 2023 Ranking (Platinum = 3, Gold = 2, Silver = 1)",
    '"Active" ASU employer',
    "ASU Supplier",
    'SDA Level score (4 is strongest relationship "Tier 1")',
]

# Ensure numeric columns are properly converted before summing
df["CALC Desirability"] = df[desirability_columns_to_sum].apply(pd.to_numeric, errors="coerce").sum(axis=1)
# Create the CESP Level column based on conditions
df["CALC CESP Level"] = df["CESP 2023 Ranking (Platinum = 3, Gold = 2, Silver = 1)"].apply(
    lambda x: "platinum" if x == 3 else "gold" if x == 2 else "silver" if x == 1 else "none"
)

df["Desirability"] = pd.to_numeric(df["Desirability"], errors="coerce")
df["Fortune 500 Priority"] = pd.to_numeric(df["Fortune 500 Priority"], errors="coerce")
df["Financial Readiness"] = pd.to_numeric(df["Financial Readiness"], errors="coerce")
df["MMC/CH C-Suite Connection"] = pd.to_numeric(df["MMC/CH C-Suite Connection"], errors="coerce")

# Handle division errors: Replace NaN or division errors with 1
df["Financial Readiness Adjusted"] = df["Financial Readiness"].apply(lambda x: x / 50.0 if pd.notna(x) and x != 0 else 1)
df["MMC/CH C-Suite Connection Adjusted"] = df["MMC/CH C-Suite Connection"].apply(lambda x: x if pd.notna(x) and x != 0 else 0)

# Compute the TEST EDOI Index
df["TEST EDOI Index"] = (
    (df["CALC Desirability"] + df["Fortune 500 Priority"]) * df["Financial Readiness Adjusted"]
) + df["MMC/CH C-Suite Connection Adjusted"]



# print(df["TEST EDOI Index"])
print(df[["CALC Desirability", "Financial Readiness", "Financial Readiness Adjusted",  "CALC CESP Level", "EDO Index", "TEST EDOI Index"]].head())


# Display the first few rows
# print(df.head())  # Default shows the first 5 rows
# print(finNum)

file_name_2 = 'newsweek_2024.csv'

df2 = pd.read_csv(file_name_2)
print(df2.head())
print(df2.tail())
print(len(df2))