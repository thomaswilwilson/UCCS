from nltk.corpus import wordnet as wn, stopwords
import re
import nltk
import collections

def clean(word, to_list = False):
    '''
    Normalizes a word by making it lowercase, removing excess punctuation,
    and putting the word, if possible, into a form which wordnet recognizes.
    Stop words (are, the, on, etc) are not counted.
    Inputs:
        word: string, word to be normalized

    Returns a string when word can be normalized and is not a stop word, returns
    nothing if given punctuation or a stop word
    '''
    words = re.sub(r'[-\n]', ' ', word.lower()).split(' ')
    if to_list:
        processed = []
        for w in words:
            to_check = re.sub(r'[^a-z]', '', w)
            if to_check != None and len(to_check) != 0 and to_check not in\
             stopwords.words('english'):
                morph = wn.morphy(to_check)
                if morph:
                    processed.append(morph)
                else:
                    processed.append(to_check)
        return processed
    else:
        processed = set()
        for w in words:
            to_check = re.sub(r'[^a-z]', '', w)
            if to_check != None and len(to_check) != 0 and to_check not in\
             stopwords.words('english'):
                morph = wn.morphy(to_check)
                if morph:
                    processed.add(morph)
                else:
                    processed.add(to_check)
        return processed

def get_hypo(synset):
    '''
    given a synset, returns a set hyponyms with given synset in their
    hypernym path 

    Inputs:
        synset: synset object to get all hyponyms of
    
    Returns a set containing all hyponyms
    '''
    hypos = set()
    hypos.update(*[get_hypo(h) for h in synset.hyponyms()])
    return hypos | set(synset.hyponyms())

def relevant_hyper(synset, axis):
    '''
    Given a synset, finds relevant hypernyms, ie pasta for lasagna
    
    Inputs:
        synset: synset object to get hypernyms of
        axis: boolean representing which foodsynset given synset is a member of
            false represents n1, dishes, true represents n2, ingredients 
        submit: part of recursive step, way to know 

    Returns set of hypernyms with relevant search terms of submitted synset
    '''
    if axis:
        for word in synset.hypernyms():
            if word == wn.synset('food.n.02'):
                return set((synset,))
            to_add = relevant_hyper(word, axis)
            if to_add:
                return set((synset,))|to_add
    else:
        for word in synset.hypernyms():
            if word.hypernyms():
                if word.hypernyms()[0] == wn.synset('food.n.01'):
                    return set((synset,))
            to_add = relevant_hyper(word, axis)
            if to_add:
                return set((synset,))|to_add
    food_list = (get_hypo(wn.synset('food.n.01')),\
    get_hypo(wn.synset('food.n.02')))

def is_food(item):
    '''
    finds synsets if item is food, for both food synsets. the first one corresponds more
    to dishes and the second more to ingredients.

    Inputs:
        item: string to be searched. multiple words must be 

    Returns tuple containing relevant synsets, will return empty if there are none
    '''
    synsets = wn.synsets(item, 'n')
    food = [None,None]
    for s in synsets:
        if not food[0] and s in food_list[0]:
            food[0] = s
        if not food[1] and s in food_list[1]:
            food[1] = s
        elif food[0] and food[1]:
            break
    if food[0] or food[1]:
        return food

def categorize(dict):
    '''
    Categorizes items based on the dictionary provided from crawler
    Inputs:
        dict: dictionary from crawler, containing item name as the key
        and item description as the value.
    Return: a dictionary containing item name as the key. The value is a length
    3 tuple containing a set synsets of any food-dish hyponyms, a set of synsets
    of any food-ingredient hyponym, and a set of all other words, normalized.

    '''
    columns = {}
    for key, value in dict.items():
        sort = (set(),set(),set(), value[1])
        if value[0]:
            words = clean(value[0] + ' ' + key)
        else:
            words = clean(key)
        for w in words:
            to_add = is_food(w)
            if to_add:
                if to_add[0]:
                    hypers = relevant_hyper(to_add[0], False)
                    if hypers:
                        sort[0].update(hypers)
                if to_add[1]:
                    sort[1].update(relevant_hyper(to_add[1], True))
            else:
                sort[2].add(w)
        columns[key] = sort
    return columns