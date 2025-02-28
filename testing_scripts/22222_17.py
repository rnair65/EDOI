import pandas as pd
from name_matching.name_matcher import NameMatcher

def match_and_merge_dataframes(master_df, dfs_to_match, column_master, column_match, score_threshold=85):
    matcher = NameMatcher(
        number_of_matches=1,
        top_n=10,
        lowercase=True,
        punctuations=True,
        remove_ascii=True,
        legal_suffixes=True,
        common_words=False,
        verbose=True)
    
    # Adjust the distance metrics to use
    matcher.set_distance_metrics(['discounted_levenshtein', 'SSK', 'fuzzy_wuzzy_token_sort'])

    # Load and process the master data
    matcher.load_and_process_master_data(column=column_master, df_matching_data=master_df, transform=True)
    
    combined_df = master_df.copy()

    for df in dfs_to_match:
        # Perform the name matching
        matches = matcher.match_names(to_be_matched=df, column_matching=column_match)
        matches = matches[matches['score'] >= score_threshold]

        # Combine the datasets based on the matches
        combined_df = pd.merge(combined_df, matches, how='left', left_index=True, right_on='match_index')
        combined_df = pd.merge(combined_df, df, how='left', left_index=True, right_index=True)
    
    return combined_df

# Define the master dataset and dataframes to match
newsweek_most_responsible = pd.read_csv(f"live_data/newsweek_most_responsible_2025.csv") # Load the CSV file into a DataFrame
fortune_100_best_companies_to_work_for = pd.read_csv(f"live_data/fortune_100_best_companies_to_work_for_2024.csv")
another_df_to_match = pd.read_csv('live_data/just_capitals_just_100.csv')  # Example additional dataframe

master_df = newsweek_most_responsible
dfs_to_match = [fortune_100_best_companies_to_work_for, another_df_to_match]

# Apply the matching and merging process
combined = match_and_merge_dataframes(master_df, dfs_to_match, column_master='COMPANY', column_match='NAME')
print(combined)
combined.to_csv("2_17_output.csv", index=False)
