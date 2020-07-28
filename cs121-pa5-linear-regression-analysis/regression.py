import numpy as np
import util

from sklearn.model_selection import train_test_split
'''
Thomas Wilson
'''

class DataSet(object):
    '''
    Class for representing a data set.
    '''

    def __init__(self, dir_path):
        '''
        Constructor
        Inputs:
            dir_path: (string) path to the directory that contains the
              file
        '''

        # REPLACE pass WITH YOUR CODE
        self.data = util.load_numpy_array(dir_path, 'data.csv')
        self.parameters = util.load_json_file(dir_path, 'parameters.json')

        self.training_data, self.testing_data = train_test_split(self.data[1], test_size=(1 - self.parameters['training_fraction']), random_state=self.parameters['seed'])

class Model(object):
    '''
    Class for representing a model.
    '''

    def __init__(self, dataset, pred_vars):
        '''
        Construct a data structure to hold the model.
        Inputs:
            dataset: an dataset instance
            pred_vars: a list of the indices for the columns used in
              the model.
        '''

        # REPLACE pass WITH YOUR CODE
        self.dep_var =  dataset.parameters['dependent_var']
        self.pred_vars = pred_vars
        self.X = dataset.training_data[:, pred_vars]
        self.y = dataset.training_data[:, dataset.parameters['dependent_var']]
        self.beta = util.linear_regression(self.X, self.y)
        self.yhat = util.apply_beta(self.beta, self.X)

        self.R2 = self.find_R2()
        self.adj_R2 = self.find_adj_R2()
        self.dataset = dataset

    ### Additional methods here
    def find_R2(self):
        '''
        returns the variance

        input: model object
        returns: (float) an R2 value

        '''
        num = np.sum((self.y - self.yhat) **2)
        denom = np.sum((self.y - self.y.mean()) ** 2)
        self.R2 = 1 - (num / denom)
        return self.R2

    def find_adj_R2(self):
        '''
        returns the adjusted variece

        input: model object
        returns: (float) an R2 value
        '''
        self.adj_R2 = self.R2 - (1-self.R2) * (len(self.pred_vars) / \
            (len(self.X) - len(self.pred_vars) - 1))
        return self.adj_R2


def compute_single_var_models(dataset):
    '''
    Computes all the single-variable models for a dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        List of Model objects, each representing a single-variable model
    '''
    lst = []
    for i in range(len(dataset.parameters['predictor_vars'])):
        model = Model(dataset, [i])
        lst.append(Model(dataset, [i]))
    # Replace [] with the list of models
    return lst


def compute_all_vars_model(dataset):
    '''
    Computes a model that uses all the predictor variables in the dataset

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object that uses all the predictor variables
    '''

    # Replace None with a model object
    model = Model(dataset, dataset.parameters['predictor_vars'])

    return model


def compute_best_pair(dataset):
    '''
    Find the bivariate model with the best R2 value

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object for the best bivariate model
    '''
    best_pair = None

    for i in dataset.parameters['predictor_vars']:
        for j in range(i, len(dataset.parameters['predictor_vars'])):
            if i != j:
                model = Model(dataset, [i, j])
                R2 = model.find_R2()
                if best_pair == None or best_pair.find_R2() < R2:
                    best_pair = model



    # Replace None with a model object
    return best_pair


def backward_selection(dataset):
    '''
    Given a dataset with P predictor variables, uses backward selection to
    compute the best models for every value of K between 1 and P.

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A list (of length P) of Model objects. The first element is the
        model where K=1, the second element is the model where K=2, and so on.
    '''
    p = dataset.parameters['predictor_vars'][:]
    lst = []
    lst.append(Model(dataset, p[:]))
    for i in range(1, len(dataset.parameters['predictor_vars'])):
        r2 = [None, None, 0]
        for j in range(len(p)):
            q = p[:j] + p[j+1:]
            model = Model(dataset, q)
            if model.R2 > r2[2]:
                r2[2] = model.R2
                r2[0] = model
                r2[1] = j

        p = p[:r2[1]] + p[r2[1] + 1:]
        lst.append(r2[0])
    return lst

def choose_best_model(dataset):
    '''
    Given a dataset, choose the best model produced
    by backwards selection (i.e., the model with the highest
    adjusted R2)

    Inputs:
        dataset: (DataSet object) a dataset

    Returns:
        A Model object
    '''

    # Replace None with a model object
    a = backward_selection(dataset)
    top_adj_R2 = [None, 0]
    for i in a:
        if i.adj_R2 > top_adj_R2[1]:
            top_adj_R2 = [i, i.adj_R2]
    return top_adj_R2[0]


def validate_model(dataset, model):
    '''
    Given a dataset and a model trained on the training data,
    compute the R2 of applying that model to the testing data.

    Inputs:
        dataset: (DataSet object) a dataset
        model: (Model object) A model that must have been trained
           on the dataset's training data.

    Returns:
        (float) An R2 value
    '''
    yhat = util.apply_beta(model.beta, dataset.testing_data[:, \
        model.pred_vars])
    num = np.sum((dataset.testing_data[:, dataset.parameters['dependent_var']]\
     - yhat) **2)
    denom = np.sum((dataset.testing_data[:, dataset.parameters\
        ['dependent_var']] - dataset.testing_data[:, dataset.parameters\
        ['dependent_var']].mean()) ** 2)

    # Replace 0.0 with the correct R2 value
    return 1 - (num / denom)

