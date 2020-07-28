# CS121: Analyzing Election Tweets

# Thomas Wilson, Tyson Miller

# Interface the algorithms in the previous part to the dataset
# of tweets. Every tweet is represented as a JSON file. Functions to implement:
# find_top_k_entities, find_min_count_entities, find_frequent_entities,
# find_top_k_ngrams, find_min_count_ngrams, find_frequent_ngrams
# find_top_k_ngrams_by_month

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg=missing-docstring, wildcard-import, invalid-name
# pylint: disable-msg=redefined-outer-name, broad-except, unused-import
# pylint: disable-msg=unused-wildcard-import

import argparse
import json
import string

from clean import *
from util import get_json_from_file, grab_year_month, pretty_print_by_month
from basic_algorithms import find_top_k, find_min_count, find_frequent

# Tweets are represented as dictionaries that has the same keys and
# values as the JSON returned by Twitter's search interface.

# ####################  MODIFY THIS CODE #####################

# PUT YOUR AUXILIARY FUNCTIONS HERE

def hashtager(tweets, entity_key):
    '''
    Create a list of all hastags.

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc.
        k: integer

    Returns top_hashtags: list of strings (each is a hashtag)
    '''
    top_hashtags = []
    a = entity_key[0]
    b = entity_key[1]
    for tweet in tweets:
        for i in range(len(tweet['entities'][a])):
            c = tweet['entities'][a][i][b].lower()
            top_hashtags.append(c)
    return top_hashtags

def lowercase(tweets):
    '''
    Turns all tweets lowercase.

    Inputs:
        tweets: a list of tweets

    Returns tweets
    '''
    for tweet in tweets:
        tweet['user']['description'] = tweet['user']['description'].lower()
    return tweets

def find_ngrams(tweets, n):
    '''
    Get a list of all n grams that occur in tweets.

    Inputs:
        tweets: a list of tweets
        n: integer

    Returns: ngrams: a list of all ngrams
    '''
    ngrams = []
    for tweet in tweets:
        lst = []
        t = tweet['text'].split()
        for i in range(len(t)):
            t[i] = t[i].lower()
            t[i] = t[i].strip(PUNCTUATION)
            if t[i] not in STOP_WORDS and t[i] and not t[i]\
            .startswith(STOP_PREFIXES):
                lst.append(t[i])
        for j in range(len(lst)):
            pair = tuple(lst[j:(j + n)])
            if len(pair) == n:
                ngrams.append(pair)
    return ngrams

# Task 1
def find_top_k_entities(tweets, entity_key, k):
    '''
    Find the K most frequently occurring entities.

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc.
        k: integer

    Returns: list of entity, count pairs

    '''

    """
    Your code goes here
    """

    top_hashtags = hashtager(tweets, entity_key)
    a = find_top_k(top_hashtags, k)

    return a

# Task 2
def find_min_count_entities(tweets, entity_key, min_count):
    '''
    Find the entities that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc
        min_count: integer

    Returns: list of entity, count pairs
    '''

    """
    Your code goes here
    """
    lst = hashtager(tweets, entity_key)
    a = find_min_count(lst, min_count)
    return a

# Task 3
def find_frequent_entities(tweets, entity_key, k):
    '''
    Find entities where the number of times the specific entity occurs
    is at least 1/k * the number of entities in across the tweets.

    Input:
        tweets: list of tweets
        entity_key: a pair ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc.
        k: integer

    Returns: list of entity, count pairs
    '''

    """
    Your code goes here
    """

    lst = hashtager(tweets, entity_key)
    a = find_frequent(lst, k)
    return a

# Task 4
def find_top_k_ngrams(tweets, n, k):
    '''
    Find k most frequently occurring n-grams.

    Inputs:
        tweets: a list of tweets
        n: integer
        k: integer

    Returns: list of key/value pairs
    '''

    #Your code goes here

    top_k = find_ngrams(tweets, n)
    a = find_top_k(top_k, k)
    return a
    
# Task 5
def find_min_count_ngrams(tweets, n, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        min_count: integer

    Returns: list of ngram/value pairs
    '''

    """
    Your code goes here
    """

    top_k = find_ngrams(tweets, n)
    a = find_min_count(top_k, min_count)

    return a

# Task 6
def find_frequent_ngrams(tweets, n, k):
    '''
    Find the most frequently-occurring n-grams.

    Inputs:
        tweets: a list of tweets
        n: integer
        k: integer

    Returns: list of ngram/value pairs
    '''

    """
    Your code goes here
    """
    lst = find_ngrams(tweets, n)
    a = find_frequent(lst, k)
    return a

# Task 7
def find_top_k_ngrams_by_month(tweets, n, k):
    '''
    Find common n-grams used by two Twitter users.

    Inputs:
        tweets: list of tweet dictionaries
        n: integer
        k: integer

    Returns: list of pairs w/ month and the top-k n-grams for that month
    '''

    """
    Your code goes here
    """
    date_dict = {}
    date_lst = []
    for tweet in tweets:
        date = grab_year_month(tweet['created_at'])
        if date not in date_dict:
            date_dict[date] = []
            date_dict[date].append(tweet)
        else:
            date_dict[date].append(tweet)

    for key in date_dict.keys():
        top_k = find_top_k_ngrams(date_dict.get(key), n, k)
        date_lst.append((key, top_k))
    return sorted(date_lst, reverse = False)

"""
DO NOT MODIFY PAST THIS POINT
"""

def parse_args(args):
    '''
    Parse the arguments.

    Inputs:
        args: list of strings

    Result: parsed argument object.

    '''
    s = 'Analyze presidential candidate tweets.'
    parser = argparse.ArgumentParser(description=s)
    parser.add_argument('-t', '--task', nargs=1,
                        help="<task number>",
                        type=int, default=[0])
    parser.add_argument('-k', '--k', nargs=1,
                        help="value for k",
                        type=int, default=[1])
    parser.add_argument('-c', '--min_count', nargs=1,
                        help="min count value",
                        type=int, default=[1])
    parser.add_argument('-n', '--n', nargs=1,
                        help="number of words in an n-gram",
                        type=int, default=[1])
    parser.add_argument('-e', '--entity_key', nargs=1,
                        help="entity key for task 1",
                        type=str, default=["hashtags"])
    parser.add_argument('file', nargs=1,
                        help='name of JSON file with tweets')

    try:
        return parser.parse_args(args[1:])
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


def go(args):
    '''
    Call the right function(s) for the task(s) and print the result(s).

    Inputs:
        args: list of strings
    '''

    task = args.task[0]
    if task <= 0 or task > 7:
        print("The task number needs to be a value between 1 and 7 inclusive.",
              file=sys.stderr)
        sys.exit(1)

    if task in [1, 2, 3]:
        ek2vk = {"hashtags":"text", 
                 "urls":"url", 
                 "user_mentions":"screen_name"}
        entity_type = (args.entity_key[0], ek2vk.get(args.entity_key[0], ""))

    tweets = get_json_from_file(args.file[0])

    if task == 1:
        print(find_top_k_entities(tweets, entity_type, args.k[0]))
    elif task == 2:
        print(find_min_count_entities(tweets, entity_type, args.min_count[0]))
    elif task == 3:
        print(find_frequent_entities(tweets, entity_type, args.k[0]))
    elif task == 4:
        print(find_top_k_ngrams(tweets, args.n[0], args.k[0]))
    elif task == 5:
        print(find_min_count_ngrams(tweets, args.n[0], args.min_count[0]))
    elif task == 6:
        print(find_frequent_ngrams(tweets, args.n[0], args.k[0]))
    else:
        result = find_top_k_ngrams_by_month(tweets, args.n[0], args.k[0])
        pretty_print_by_month(result)
        

if __name__=="__main__":
    args = parse_args(sys.argv)
    go(args)
