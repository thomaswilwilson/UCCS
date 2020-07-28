import csv
import pandas as pd



def get_pandas(a):
    '''
    turns restaurant list and menu dictionary into a pandas dataframes
    inputs:
        a (tuple): The restaurant list and the menu dictionary

    output:
        rest_df (dataframe): The restaurant dataframe
        menu_df (dataframe): The Menu dataframe
    '''

    m_columns = ['name', 'dish', 'synset_ingredient', 'synset_dish', 'other_words', 'price']
    lst = []


    for key, value in a[1].items():
        for k2, v2 in value.items():
            lst.append([key, k2, v2[1], v2[0], v2[2], v2[3]])

  
    menu_df = pd.DataFrame(lst, columns = m_columns)
    rest_df = pd.DataFrame(a[0])

    return rest_df, menu_df