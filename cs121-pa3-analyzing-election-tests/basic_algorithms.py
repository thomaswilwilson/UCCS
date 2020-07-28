# CS121: Analyzing Election Tweets

# Thomas Wilson, Tyson Miller

# Algorithms for efficiently counting and sorting distinct
# `entities`, or unique values, are widely used in data
# analysis. Functions to implement: count_items, find_top_k,
# find_min_count, find_frequent

# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg=missing-docstring

from util import sort_count_pairs

def count_items(items):
    '''
    Counts each distinct item (entity) in a list of items

    Inputs:
        items: list of items (must be hashable/comparable)

    Returns: list (item, number of occurrences).
    '''


    # YOUR CODE GOES HERE
    dic = {}
    temp = []
    lst = []
    for item in items:
        if (item in dic):
            dic[item] += 1
        else:
            dic[item] = 1

    for key, value in dic.items():
        return dic

        temp = [key,value]
        lst.append(temp)
    # REPLACE RETURN VALUE WITH AN APPROPRIATE VALUE
    return lst


def find_top_k(items, k):
    '''
    Find the K most frequently occurring items

    Inputs:
        items: list of items (must be hashable/comparable)
        k: a non-negative integer

    Returns: sorted list of the top K tuples

    '''

    # Error checking (DO NOT MODIFY)
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    # Runs the helper function for you (DO NOT MODIFY)
    item_counts = count_items(items)

    temp = []
    lst = []
    counts = {}
    for item in items:
        if (item in counts):
            counts[item] += 1
        else:
            counts[item] = 1

    for key, value in counts.items():
        temp = (key, value)

        lst.append(temp)

    lst1 = sort_count_pairs(lst)

    # YOUR CODE GOES HERE
    # REPLACE RETURN VALUE WITH AN APPROPRIATE VALUE
    return lst1[:k]


def find_min_count(items, min_count):
    '''
    Find the items that occur at least min_count times

    Inputs:
        items: a list of items  (must be hashable/comparable)
        min_count: integer

    Returns: sorted list of tuples
    '''

    # Runs the helper function for you (DO NOT MODIFY)

    # YOUR CODE HERE
    item_counts = count_items(items)

    temp = []
    lst = []
    counts = {}
    for item in items:
        if (item in counts):
            counts[item] += 1
        else:
            counts[item] = 1

    for key, value in counts.items():
        if value >= min_count:
            temp = (key, value)
            lst.append(temp)

    lst1 = sort_count_pairs(lst)

    # REPLACE RETURN VALUE WITH AN APPROPRIATE VALUE
    return lst1


def decr_and_remove(d):
    '''
    Given a dictionary that maps keys to positive integer,
    decrement the values and remove any key-value pair in which
    the decremented value becomes zero. From Textbook.


    Input:
        d (dictionary): maps keys to positive integers
    '''

    # YOUR CODE HERE
    keys_to_remove = []
    for key, value in d.items():
        d[key] = value - 1
        if d[key] == 0 and key not in keys_to_remove:
            keys_to_remove.append(key)
    for key in keys_to_remove:
        del d[key]
    # REPLACE RETURN VALUE WITH AN APPROPRIATE VALUE
    return


def find_frequent(items, k):
    '''
    Find items where the number of times the item occurs is at least
    1/k * len(items).

    Input:
        items: a list of items  (must be hashable/comparable)
        k: integer

    Returns: sorted list of tuples
    '''



    # YOUR CODE HERE
    counter = {}

    keys_to_remove = []
    for item in items:
        if item in counter:
            counter[item] += 1
        if item not in counter:
            if len(counter) < k - 1:
                counter[item] = 1
            else:
                decr_and_remove(counter)

    for item in items:

        if len(counter) > k - 1:
            raise ValueError(
                "The number of elements stored in counter" +
                " should not exceed (k-1)=" + str(k-1))
        # WRITE THE APPROPRIATE UPDATE LOGIC FOR COUNTER

    return sort_count_pairs(counter.items())
