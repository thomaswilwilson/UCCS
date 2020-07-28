'''
Scoring Algorithm

'''

from nltk.corpus import wordnet as wn
import pandas as pd
import normalize as nor
import operator

def calc_score(restaurants, menu_items, inputs, names, num_return=5):
    '''
    Finds best restaurants given their menu items and input preferences

    Inputs:
        restaurants: df with restaurant information
        menu_items: df with menu items
        inputs: dict of preferences for each person
        names: individual names
        num_return: number of restaurants options to return

    Returns: num_return number of best fit restaurants
    '''
    food_prefs, num_people, columns = handle_input(inputs, names)
    item_scores = relativity_index(menu_items, food_prefs)
    r_scores = aggregated_score(restaurants, menu_items, inputs, 
                                item_scores, num_people) 
    columns.insert(0, "restaurant name")
    r = 0
    best_restaurants = []
    while r < num_return:
        row = r_scores[r]
        restaurant =[row[0]]
        for k,v in row[2].items():
            restaurant.extend([v[1], v[0], v[2]])
        best_restaurants.append(restaurant)
        r += 1
    best_restaurants = pd.DataFrame(best_restaurants, columns = columns)
    return best_restaurants


def handle_input(inputs, names):
    '''
    Reads input and separates individual preferences

    Inputs:
        inputs: individudal preferences
        names: individual names

    Returns: food preferences, number of people, and columns for final df
    '''
    prefs = []
    columns = []
    num_people = 0
    for p, v in inputs["people"].items():
        num_people += 1
        columns.extend([names[p-1], "Dish score", "Cost"])
        food_pref = v[0].split()
        indiv_pref = []
        [indiv_pref.append(i) for i in food_pref if nor.clean(i)]
        prefs.append(indiv_pref)
    return prefs, num_people, columns

def relativity_index(menu_items, food_prefs):
    '''
    This generates a relativity score for each menu item

    Inputs: 
        menu_items: menu df
        food_prefs: list of individual food preferences

    Returns: dictionary with ordered score for each menu item
    '''
    items = {}
    for m in menu_items.itertuples():
        synset_dish = m.synset_dish
        synset_ingredient = m.synset_ingredient
        item_cost = m.price
        item_name = m.dish 
        items[item_name] = []
        for i in food_prefs:
            real_food = 0
            in_synset = 0
            missing_descriptive = 0 
            for w in i:
                food = nor.is_food(w)
                if not food:
                    if not w in m.other_words:
                        missing_descriptive += 1 
                else:
                    real_food += 1
                    if food[0] in synset_dish: 
                        in_synset += 1
                    elif food[1] in synset_ingredient:
                        in_synset += 1
            if real_food > 0:
                items[item_name].append((in_synset / real_food) * 
                                        (.9 ** missing_descriptive))
            else: 
                items[item_name].append(0)
        items[item_name].append(item_cost)
    return items


def aggregated_score(restaurants, menu_items, input, item_scores, num_people):
    '''
    Generates the score for a restaurant

    Inputs:
        restaurants: restaurant df
        menu_items: menu df
        input: dict of preferences
        item_scores: dict with ordered score for each item
        num_people: number of group members
    '''
    r_scores = []
    for r in restaurants.itertuples():
        r_name = r.name
        r_menu = menu_items.loc[menu_items["name"] == r_name]
        r_score = 0
        best_dishes = {i: [-.01, None] for i in range(1, num_people + 1)}
        for i in r_menu.itertuples():
            dish_name = i.dish
            dish_scores = item_scores[dish_name] 
            for p in range(num_people):
                if dish_scores[p] > best_dishes[p+1][0]:
                    if input["people"][p+1][2] > float(dish_scores[-1]):
                        best_dishes[p+1] = [dish_scores[p], 
                                        dish_name, dish_scores[-1]]
        overall_strength_of_pref = 0
        for k,v in input["people"].items():
            strength = v[1]
            cost = v[2]
            if best_dishes[k][0]:
                d_score = (best_dishes[k][0])
            else:
                d_score = 0
            r_score += strength * (d_score)
            overall_strength_of_pref += strength 
        if input["delivery_time"] >= r.maxDeliveryTime:
            delivery_score = 1
        elif r.minDeliveryTime <= input["delivery_time"] <= r.maxDeliveryTime:
            delivery_score = 1 - (r.maxDeliveryTime - 
                                        input["delivery_time"]) * .01
        else:
            delivery_score = .25
        r_scores.append((r_name, ((r_score * delivery_score)/
                                    overall_strength_of_pref), best_dishes))
    return sorted(r_scores, key=lambda x: x[1], reverse = True)