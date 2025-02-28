from emm import PandasEntityMatching
from emm.data.create_data import create_example_noised_names

# generate example ground-truth names and matching noised names, with typos and missing words.
ground_truth, noised_names = create_example_noised_names(random_seed=42)
train_names, test_names = noised_names[:5000], noised_names[5000:]

print(ground_truth)
print(noised_names)
print(train_names)
print(test_names)

# two example name-pair candidate generators: character-based cosine similarity and sorted neighbouring indexing
indexers = [
  {
      'type': 'cosine_similarity',
      'tokenizer': 'characters',   # character-based cosine similarity. alternative: 'words'
      'ngram': 2,                  # 2-character tokens only
      'num_candidates': 5,         # max 5 candidates per name-to-match
      'cos_sim_lower_bound': 0.2,  # lower bound on cosine similarity
  },
  {'type': 'sni', 'window_length': 3}  # sorted neighbouring indexing window of size 3.
]
em_params = {
  'name_only': True,         # only consider name information for matching
  'entity_id_col': 'Index',  # important to set both index and name columns to pick up
  'name_col': 'Name',
  'indexers': indexers,
  'supervised_on': False,    # no supervided model (yet) to select best candidates
  'with_legal_entity_forms_match': True,   # add feature that indicates match of legal entity forms (e.g. ltd != co)
}

# 1. initialize the entity matcher
p = PandasEntityMatching(em_params)

# 2. fitting: prepare the indexers based on the ground truth names, eg. fit the tfidf matrix of the first indexer.
p.fit(ground_truth)

# 3. create and fit a supervised model for the PandasEntityMatching object, to pick the best match (this takes a while)
#    input is "positive" names column 'Name' that are all supposed to match to the ground truth,
#    and an id column 'Index' to check with candidate name-pairs are matching and which not.
#    A fraction of these names may be turned into negative names (= no match to the ground truth).
#    (internally, candidate name-pairs are automatically generated, these are the input to the classification)
p.fit_classifier(train_names, create_negative_sample_fraction=0.5)

# 4. scoring: generate pandas dataframe of all name-pair candidates.
#    The classifier-based probability of match is provided in the column 'nm_score'.
#    Note: can also call p.transform() without training the classifier first.
candidates_scored_pd = p.transform(test_names)

# 5. scoring: for each name-to-match, select the best ground-truth candidate.
best_candidates = candidates_scored_pd[candidates_scored_pd.best_match]
print(best_candidates.head())