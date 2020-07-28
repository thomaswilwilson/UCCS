# CS122: Linking restaurant records in Zagat and Fodor's data sets
#
# Thomas Wilson


import numpy as np
import pandas as pd
import jellyfish
import util

possible_combinations = {
    ('low', 'low', 'low'): 0,
    ('low', 'low', 'medium'): 0,
    ('low', 'low', 'high'): 0,
    ('low', 'medium', 'low'): 0, 
    ('low', 'medium', 'medium'): 0,
    ('low', 'medium', 'high'): 0,
    ('low', 'high', 'medium'): 0,
    ('low', 'high', 'high'): 0,
    ('low', 'high', 'low'): 0,
    ('medium', 'low', 'low'): 0,
    ('medium', 'low', 'medium'): 0,
    ('medium', 'low', 'high'): 0,
    ('medium', 'medium', 'low'): 0,
    ('medium', 'low', 'medium'): 0,
    ('medium', 'medium', 'medium'): 0,
    ('medium', 'medium', 'high'): 0,
    ('medium', 'high', 'low'): 0,
    ('medium', 'high', 'medium'): 0,
    ('medium', 'high', 'high'): 0,
    ('high', 'low', 'low'): 0,
    ('high', 'low', 'medium'): 0,
    ('high', 'low', 'high'): 0,
    ('high', 'medium','low'): 0,
    ('high', 'medium','medium'): 0,
    ('high', 'medium','high'): 0,
    ('high', 'high','low'): 0,
    ('high', 'high','medium'): 0,
    ('high', 'high','high'): 0,
}

def find_matches(mu, lambda_, block_on_city=False):
    # WRITE YOUR CODE HERE
    zagat, fodors = get_dataframes()
    matches = get_matches_or_unmatches(zagat, fodors)
    unmatches = get_matches_or_unmatches(zagat, fodors, matches=False)
    match_tuples = get_jw_category(matches, possible_combinations)
    unmatch_tuples = get_jw_category(unmatches, possible_combinations)
    m_tuples, u_tuples, p_tuples = sort_tuples(match_tuples, unmatch_tuples,\
     mu, lambda_)

    if block_on_city == True:
        return get_block_on_city(zagat, fodors, m_tuples,u_tuples, p_tuples)

    return partition_tuples(zagat, fodors,m_tuples,u_tuples, p_tuples)

def get_block_on_city(zagat, fodors, m_tuples,u_tuples, p_tuples):
    '''
    Iterates through all possible combinations of entries from zagat and
     fodors dataframes where the cities are identical and computes tuples.
      Sends each possible combination to its respective dataframe
      
    Inputs:
        zagat(Pandas Dataframe): zagat dataframe
        fodors(Pandas Dataframe): fodors dataframe
        match_tuples(list): list of tuples to be classified as matches
        unmatch_tuples(list): list of tuples to be classified as unmatches
        possible_tuples(list): list of tuples to be classified as possible
         matches

    Outputs:
        matches_df: dataframe of matches
        possible_df: dataframe of possible matches
        unmatches_df: dataframe of non matches
    '''
    column_index = (['z_restaurant', 'z_city', 'z_address', 'f_restaurant',\
     'f_city', 'f_address'])

    city_dataframes = []

    z_dict = dict(tuple(zagat.groupby('city')))
    f_dict = dict(tuple(fodors.groupby('city')))

    for z_key in z_dict.keys():

        for f_key in f_dict.keys():

            if z_key == f_key:
                city_dataframes.append((z_key, f_key))

    first_time = True
    for tup in city_dataframes:

        
        zagat = z_dict[tup[0]].reset_index()
        fodors = f_dict[tup[1]].reset_index()
        cmatch_dataframe, cpossible_dataframe, cunmatch_dataframe =\
         partition_tuples(zagat, fodors, m_tuples, u_tuples, p_tuples)

        if first_time:
            match_dataframe = pd.DataFrame(data=cmatch_dataframe, \
                columns=column_index)

            possible_dataframe = pd.DataFrame(data=cpossible_dataframe, \
                columns=column_index)

            unmatch_dataframe = pd.DataFrame(data=cunmatch_dataframe, \
                columns=column_index)

            first_time = False
        else:
            match_dataframe = pd.concat([match_dataframe, cmatch_dataframe])
            possible_dataframe = pd.concat([possible_dataframe,\
             cpossible_dataframe])

            unmatch_dataframe = pd.concat([unmatch_dataframe,\
             cunmatch_dataframe])


    return match_dataframe, possible_dataframe, unmatch_dataframe


def partition_tuples(zagat, fodors, match_tuples,\
 unmatch_tuples, possible_tuples):

    '''
    Iterates through all possible combinations of entries from zagat and
     fodors dataframes and computes tuples. Sends each possible combination
      to its respective dataframe

    Inputs:
        zagat(Pandas Dataframe): zagat dataframe
        fodors(Pandas Dataframe): fodors dataframe
        match_tuples(list): list of tuples to be classified as matches
        unmatch_tuples(list): list of tuples to be classified as unmatches
        possible_tuples(list): list of tuples to be classified as possible
         matches

    Outputs:
        matches_df: dataframe of matches
        possible_df: dataframe of possible matches
        unmatches_df: dataframe of non matches

    '''
    column_index = (['z_restaurant', 'z_city', 'z_address',\
     'f_restaurant', 'f_city', 'f_address'])
    matches_rows = []
    unmatches_rows = []
    possible_rows = []

    for i in range(len(zagat) - 1):

        for j in range(len(fodors) - 1):

            z_restaurant = zagat['restaurant'][i]
            f_restaurant = fodors['restaurant'][j]

            z_city = zagat['city'][i]
            f_city = fodors['city'][j]

            z_address = zagat['address'][i]
            f_address = fodors['address'][j]

            r_score = jellyfish.jaro_winkler(z_restaurant, f_restaurant)
            c_score = jellyfish.jaro_winkler(z_city, f_city)
            a_score = jellyfish.jaro_winkler(z_address, f_address)

            tup = (util.get_jw_category(r_score), util.get_jw_category\
                (c_score), util.get_jw_category(a_score))

            if tup in match_tuples:
                matches_rows.append([z_restaurant, z_city, z_address,\
                 f_restaurant, f_city, f_address])

            elif tup in unmatch_tuples:
                unmatches_rows.append([z_restaurant, z_city, z_address,\
                 f_restaurant, f_city, f_address])

            elif tup in possible_tuples:
                possible_rows.append([z_restaurant, z_city, z_address,\
                 f_restaurant, f_city, f_address])

    matches_df = pd.DataFrame(data=matches_rows, columns=column_index)
    unmatches_df = pd.DataFrame(data=unmatches_rows, columns=column_index)
    possible_df = pd.DataFrame(data=possible_rows, columns=column_index)

    return matches_df, possible_df, unmatches_df


def get_dataframes():
    '''
    Creates dataframes for zagat and fodors data

    Inputs:
        None

    Outputs:
        zagat(Pandas Dataframe): zagat dataframe
        fodors(Pandas Dataframe): fodors dataframe
    '''
    column_index = (['id', 'restaurant', 'city', 'address'])

    zagat = pd.read_csv('zagat.csv', names=column_index, index_col='id')
    fodors = pd.read_csv('fodors.csv', names=column_index, index_col='id')

    return zagat, fodors


def get_matches_or_unmatches(zagat, fodors, matches=True):
    '''
    returns either the matches dataframe or the unmatches dataframs
    depending on whether matches is set to true or false

    Inputs:
        zagat(Pandas Dataframe): zagat dataframe
        fodors(Pandas Dataframe): fodors dataframe
        matches(boolean): if true constructs matches df if false unmatches df

    Outputs:
        df(Pandas Dataframs): dataframe containing wither matches or unmatches

    '''
    column_index = (['z_id', 'z_restaurant', 'z_city', 'z_address', 'f_id',\
     'f_restaurant', 'f_city', 'f_address'])

    if matches:
        known_links = pd.read_csv('known_links.csv', names=['zagat', 'fodors'])
        zs = zagat.iloc[known_links['zagat']].reset_index(level=0)
        fs = fodors.iloc[known_links['fodors']].reset_index(level=0)

    else:
        zs = zagat.sample(1000, replace = True, random_state = 1234)\
        .reset_index(level=0)
        fs = fodors.sample(1000, replace = True, random_state = 5678)\
        .reset_index(level=0)

    df = pd.concat([zs, fs], axis=1)
    df.columns = column_index
    del df['z_id']
    del df['f_id']

    return df

def get_jw_category(df, possible_combinations):
    '''
    Computes relative frequencies for the 27 combinations of possible tuples

    inputs:
        df (Pandas Dataframe): either matches or unmatches dataframe
        possible_combinations (dict): dictionary of all possible tuple 
          combinations. Value pair is 0 for each tuple key

    outputs:
        new_d (dict): dictionary maping tuple combinations to relative
          frequencies
    '''
    new_d = possible_combinations.copy()
    for i in range(len(df) - 1):

        r_score = jellyfish.jaro_winkler(df['z_restaurant'][i],\
         df['f_restaurant'][i])

        c_score = jellyfish.jaro_winkler(df['z_city'][i], df['f_city'][i])

        a_score = jellyfish.jaro_winkler(df['z_address'][i],\
         df['f_address'][i])

        tup = (util.get_jw_category(r_score), util.get_jw_category(c_score),\
         util.get_jw_category(a_score))
        new_d[tup] += 1/len(df) 

    return new_d


def sort_tuples(match_dict, unmatch_dict, mu, lambda_):
    '''
    returns list of possible tuples, match tuples and unmatch tuples

    inputs:
        match_dict: dictionary of relative frequencies for match tuples
        unmatch_dict: dictionary of relative frequencies for unmatch tuples
        mu: false positive rate
        lamda_: false negative rate

    returns:
        match_tuples: list of match tuples
        unmatch_tuples: list of tuples that are unmatches
        possible tuples: list of possible tuples
    '''
    match_tuples = []
    possible_tuples = []
    unmatch_tuples = []

    ratio_dne = []
    ratio_e = []

    for w in match_dict:
        m = match_dict[w]
        u = unmatch_dict[w]

        if u == 0:
            ratio = None

        else:
            ratio = m / u
        
        if m == 0 and u == 0:
            possible_tuples.append(w)

        elif ratio == None:
            ratio_dne.append([w, ratio])

        else:
            ratio_e.append([w, ratio])

    ratio_e.sort(key = lambda x: x[1], reverse=True)  
    sorted_list = ratio_dne + ratio_e


    false_positive_rate = 0
    for i in sorted_list:

        tup = i[0]
        u = unmatch_dict[tup]

        false_positive_rate += u

        if false_positive_rate <= mu:
            match_tuples.append(tup)


    false_negative_rate = 0
    for j in reversed(sorted_list):
        tup = j[0]
        m = match_dict[tup]

        false_negative_rate += m

        if false_negative_rate <= lambda_:
            unmatch_tuples.append(tup)

    for k in sorted_list:
        in_matches = k[0] in match_tuples
        in_unmatches = k[0] in unmatch_tuples

        if in_matches and in_unmatches:
            unmatch_tuples.remove(k[0])

        elif not in_matches and not in_unmatches:
            possible_tuples.append(k[0])




    return match_tuples, unmatch_tuples, possible_tuples


if __name__ == '__main__':
    matches, possibles, unmatches = \
        find_matches(0.005, 0.005, block_on_city=False)

    print("Found {} matches, {} possible matches, and {} "
          "unmatches with no blocking.".format(matches.shape[0],
                                               possibles.shape[0],
                                               unmatches.shape[0]))
