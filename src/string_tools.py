from thefuzz import fuzz, process


def select_most_likely_matches(string_to_match, df, column_name, threshold):

    df['match_score'] = df[column_name].apply(lambda x: fuzz.token_sort_ratio(string_to_match, x))

    likely_match = df[df["match_score"] > threshold]


    return likely_match
