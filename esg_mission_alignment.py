import pandas as pd
import unicodedata
import re
from cleanco import basename
import data_collection

#### NEWSWEEK MOST RESPONSIBLE Adjustments
def adjust_newsweek_most_responsible():
    most_recent_year = data_collection.find_newsweek_most_responsible() # Updates live data
    newsweek_most_responsible = pd.read_csv(f"live_data/newsweek_most_responsible_{most_recent_year}.csv") # Load the CSV file into a DataFrame
    newsweek_most_responsible.rename(columns={"RANK": f"NEWSWEEK_MOST_RESPONSIBLE_{most_recent_year}_RANK"}, inplace=True) # Rename RANK column to a universally usable column for the final dataframe

    # Rank on the actual list contains asterisks that modify true length
    # Using row number allows for usable rank number with minimal computation
    newsweek_most_responsible[f"NEWSWEEK_MOST_RESPONSIBLE_{most_recent_year}_RANK"] = newsweek_most_responsible.index + 1

    # Calculate percentile of rank: 1 - (rank/ # of companies)
    # newsweek_most_responsible["(Percentile Rank) Newsweek Most Responsible Companies"] = 1 - (newsweek_most_responsible[f"NEWSWEEK_MOST_RESPONSIBLE_{most_recent_year}_RANK"] / len(newsweek_most_responsible))
    return newsweek_most_responsible

#### FORTUNE 100 BEST COMPANIES TO WORK FOR
def adjust_fortune_100_best_companies_to_work_for():
    most_recent_year = data_collection.find_fortune_100_best_companies_to_work_for()
    fortune_100_best_companies_to_work_for = pd.read_csv(f"live_data/fortune_100_best_companies_to_work_for_{most_recent_year}.csv")
    fortune_100_best_companies_to_work_for.rename(columns={"RANK": f"FORTUNE_100_BEST_COMPANIES_TO_WORK_FOR_{most_recent_year}_RANK"}, inplace=True)

    # Find rank
    fortune_100_best_companies_to_work_for[f"FORTUNE_100_BEST_COMPANIES_TO_WORK_FOR_{most_recent_year}_RANK"] = fortune_100_best_companies_to_work_for.index + 1
    fortune_100_best_companies_to_work_for = fortune_100_best_companies_to_work_for.drop(columns=["UNNAMED: 9"])

    return fortune_100_best_companies_to_work_for

#### JUST CAPITAL'S "JUST 100"
def adjust_just_capitals_just_100():
    most_recent_year = data_collection.find_just_capitals_just_100()
    just_capitals_just_100 = pd.read_csv("live_data/just_capitals_just_100.csv")
    just_capitals_just_100.rename(columns={"Rank": "JUST_CAPITALS_JUST_100_RANK"}, inplace=True)

    return just_capitals_just_100



#### POINTS OF LIGHT "CIVIC 50"
def adjust_find_points_of_light_civic_50():
    most_recent_year = data_collection.find_points_of_light_civic_50()
    points_of_light_civic_50 = pd.read_csv("live_data/points_of_light_civic_50.csv")
    points_of_light_civic_50.rename(columns={"Companies": "POINTS_OF_LIGHT_CIVIC_50"}, inplace=True)

    return points_of_light_civic_50
