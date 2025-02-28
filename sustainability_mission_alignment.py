import pandas as pd
import unicodedata
import re
from cleanco import basename

#### BARRON'S 100 MOST SUSTAINABLE
barrons_100_most_sustainable_2024 = pd.read_csv("static_data/barrons_100_most_sustainable_2024.csv")
barrons_100_most_sustainable_2024.rename(columns={"2024 RANK": "BARRONS_100_MOST_SUSTAINABLE_2024_RANK"}, inplace=True)

# Find rank
barrons_100_most_sustainable_2024["BARRONS_100_MOST_SUSTAINABLE_2024_RANK"] = barrons_100_most_sustainable_2024.index + 1


