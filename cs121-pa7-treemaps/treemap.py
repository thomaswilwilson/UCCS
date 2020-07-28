# CS121: PA 7 - Diversity Treemap
# Thomas Wilson
# Code for constructing a treemap.

import argparse
import pandas as pd
import sys
import tree
import drawing
import click

###############
#             #
#  Your code  #
#             #
###############

def load_diversity_data(filename, debug=False):
    '''
    Load Silicon Valley diversity data and print summary

    Inputs:
        filename: (string) the name pf the file with the data

    Returns: a pandas dataframe
    '''
    data = pd.read_csv(filename)
    ### Add print statements here (if debug is True)
    if debug == True:
        print('########')
        print('companies')
        print('########')
        companies = []
        for i in data['company']:
                if i not in companies:
                    companies.append(i)
        print('diversity data comes from the following', len(companies),\
         'companies', companies)
        print('')
        print('########')
        print('gender')
        print('########')
        gender = {'male': 0, 'female': 0}
        for i in data['gender']:
            gender[i] = gender[i] + 1
        for y, z in gender.items():
            print(y, z)
        print('')
        print('########')
        print('race')
        print('########')
        race = {'American_Indian_Alaskan_Native': 0, 'Asian': 0, \
        'Black_or_African_American': 0, 'Latino': 0, \
        'Native_Hawaiian_or_Pacific_Islander': 0, 'Two_or_more_races': 0,\
         'White':0}
        for i in data['race']:
            race[i] = race[i] + 1
        for a, b in race.items():
            print(a, b)
        print('')
        print('########')
        print('job category')
        print('########')
        job_category = {'Administrative support': 0, 'Craft workers': 0, \
        'Executive/Senior officials & Mgrs': 0, 'First/Mid officials & Mgrs':\
         0, 'Professionals': 0, 'Sales workers': 0, 'Service workers': 0,\
          'Technicians': 0, 'laborers and helpers': 0, 'operatives': 0}
        for i in data['job_category']:
            job_category[i] = job_category[i] + 1
        for q, w in job_category.items():
            print(q, w)
    return data
    
def compute_internal_counts(t):
    '''
    Assign a count to the interior nodes.  The count of the leaves
    should already be set.  The count of an internal node is the sum
    of the counts of its children.

    Inputs:
        t (Tree): a tree

    Returns:
        The input tree t should be modified so that every internal node's
        count is set to be the sum of the counts of its children.

        The return value will be:
        - If the tree has no children: the value of the count attribute
        - If the tree has children: the sum of the counts of the children
    '''

    ### Replace 0 with the appropriate return value
    d = {'count': 0}
    if t.count:
        return t.count
    elif t.num_children() > 0:
        for i in t.children:
            d['count'] = d['count'] + compute_internal_counts(i)
    t.count = d['count']
    return t.count


def compute_verbose_labels(t, prefix=None):
    '''
    Assign a verbose label to non-root nodes. Verbose labels contain the 
    full path to that node through the tree. For example, following the 
    path "Google" --> "female" --> "white" should create the verbose label 
    "Google: female: white"

    Inputs:
        t (Tree): a tree

    Outputs:
        Nothing. The input tree t should be modified to contain
            verbose labels for all non-root nodes
    '''


    ### YOUR CODE HERE
    if prefix:
        t.verbose_label = prefix + ': ' + t.label
    else:
        t.verbose_label = t.label

    if t.num_children() > 0:
        for i in t.children:
            compute_verbose_labels(i, t.verbose_label)
    # Do not modify this return statement.
    # This function doesn't return anything!
    return None


def prune_tree(t, values_to_discard):
    '''
    Returns a tree with any node whose label is in the list values_to_discard
    (and thus all of its children) pruned. This function should return a copy
    of the original tree and should not destructively modify the original tree.
    The pruning step must be recursive.

    Inputs:
        t (Tree): a tree
        values_to_discard (list of strings): A list of strings specifying the
                  labels of nodes to discard

    Returns: a new Tree object representing the pruned tree
    '''

    ### YOUR CODE HERE
    cut = tree.Tree(t.label)
    if t.num_children() == 0:
        cut.count = t.count
        
    else:
        for i in t.children:
            if i.label not in values_to_discard:
                cut.add_child(prune_tree(i, values_to_discard))
    ### Replace t with the appropriate return value
    return cut


def validate_tuple_param(p, name):
    assert isinstance(p, (list, tuple)) and len(p) == 2 \
        and isinstance(p[0], float) and isinstance(p[1], float), \
        name + " parameter to Rectangle must be a tuple or list of two floats"

    assert p[0] >= 0.0 and p[1] >= 0.0, \
        "Incorrect value for rectangle {}: ({}, {}) ".format(name, p[0], p[1]) + \
        "(both values must be >= 0)"


class Rectangle:
    '''
    Simple class for representing rectangles
    '''
    def __init__(self, origin, size, label, verbose_label):
        # Validate parameters
        validate_tuple_param(origin, "origin")
        validate_tuple_param(origin, "size")
        assert label is not None, "Rectangle label can't be None"
        assert isinstance(label, str), "Rectangle label must be a string"
        assert verbose_label is not None, "Rectangle verbose_label can't be None"
        assert isinstance(verbose_label, str), "Rectangle verbose_label must be a string"

        self.x, self.y = origin
        self.width, self.height = size
        self.label = label
        self.verbose_label = verbose_label

    def __str__(self):
        if self.verbose_label is None:
            label = self.label
        else:
            label = self.verbose_label

        return "RECTANGLE {:.4f} {:.4f} {:.4f} {:.4f} {}".format(self.x, self.y,
                                                                 self.width, self.height,
                                                                 label)

    def __repr__(self):
        return str(self)


def set_vert(y_i, width_i, height_i, width, height, frac):
    '''
    set's y as well as height and width node
    '''
    y_i += height_i
    width_i = width
    height_i = height * frac
    return y_i, width_i, height_i

def set_hor(x_i, width_i, height_i, width, height, frac):
    '''
    set's x as well as height and width node
    '''
    x_i += width_i
    width_i = width * frac
    height_i = height
    return x_i, width_i, height_i


def design_rectangles(t, x, y, width, height, rects, vert=False):
    '''
    Recurrsively adds rectangle objects to a list. The list will be used to draw rectangles for the treemap
    Inputs:
        t(Tree): a tree
        x(float): starting x coordinate
        y(float): starting y coordinate
        width(float): width of rectangle
        height(float): height of rectangle
        rects: an empty list

        Returns: 
            '''
    
    if t.count > 0 and t.num_children() > 0:
        x_i = x
        y_i = y
        width_i = 0.0
        height_i = 0.0
        for i in t.children:
            frac = i.count / t.count
            if vert == True:
                y_i += height_i
                width_i = width
                height_i = height * frac
            else:
                x_i += width_i
                width_i = width * frac
                height_i = height
            design_rectangles(i, x_i, y_i, width_i, height_i, rects, vert=(not vert))
    elif t.num_children() == 0:
        a = Rectangle((x, y), (width, height), t.label, t.verbose_label)
        rects.append(a)
            
    

def compute_rectangles(t, bounding_rec_height=1.0, bounding_rec_width=1.0):
    '''
    Computes the rectangles for drawing a treemap of the provided tree

    Inputs:
        t (Tree): a tree
        bounding_rec_height, bounding_rec_width (floats): the size of
           the bounding rectangle.

    Returns: a list of Rectangle objects
    '''

    # Do not remove these function calls
    compute_internal_counts(t)
    compute_verbose_labels(t)

    ### YOUR CODE HERE

    rects = []
    design_rectangles(t, 0.0, 0.0, bounding_rec_width, bounding_rec_height, rects)
    # Replace [] with the appropriate return value
    return  rects


#############################
#                           #
#  Our code: DO NOT MODIFY  #
#                           #
#############################

@click.command(name="treemap")
@click.argument('diversity_file', type=click.Path(exists=True))
@click.option('--categories', '-c', type=str)
@click.option('--prune', '-p', type=str)
@click.option('--output', '-o', type=str)
def cmd(diversity_file, categories, prune, output):

    data = load_diversity_data(diversity_file)

    if categories is not None:
        categories = categories.split(",")

    if prune is not None:
        prune = prune.split(",")

    data_tree = tree.data_to_tree(data, categories)

    compute_internal_counts(data_tree)

    compute_verbose_labels(data_tree)

    if prune is not None:
        data_tree = prune_tree(data_tree, prune)

    rectangles = compute_rectangles(data_tree)

    if output == "-":
        for rect in rectangles:
            print(rect)
    else:
        drawing.draw_rectangles(rectangles, output)

if __name__ == "__main__":
    cmd() # pylint: disable=no-value-for-parameter