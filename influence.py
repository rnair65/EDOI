import pandas as pd
import unicodedata
import re
from cleanco import basename

#### FORTUNE 500 Adjustments
fortune_500_2024 = pd.read_csv("static_data/fortune_500_2024.csv") # Load the CSV file into a DataFrame
fortune_500_2024.rename(columns={"Rank": "FORTUNE_500_2024_RANK"}, inplace=True) # Rename RANK column to a universally usable column for the final dataframe

# Rank on the actual list contains asterisks that modify true length
# Using row number allows for usable rank number with minimal computation
fortune_500_2024["FORTUNE_500_2024_RANK"] = fortune_500_2024.index + 1
