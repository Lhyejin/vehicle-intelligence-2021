import numpy as np
import random
from math import sqrt, pi, exp

def gaussian_prob(obs, mu, sig):
    # Calculate Gaussian probability given
    # - observation
    # - mean
    # - standard deviation
    num = (obs - mu) ** 2
    denum = 2 * sig ** 2
    norm = 1 / sqrt(2 * pi * sig ** 2)
    return norm * exp(-num / denum)

# Gaussian Naive Bayes class
class GNB():
    # Initialize classification categories
    def __init__(self):
        self.classes = ['left', 'keep', 'right']

    # Given a set of variables, preprocess them for feature engineering.
    def process_vars(self, vars):
        # The following implementation simply extracts the four raw values
        # given by the input data, i.e. s, d, s_dot, and d_dot.
        s, d, s_dot, d_dot = vars
        return s, d, s_dot, d_dot

    # Train the GNB using a combination of X and Y, where
    # X denotes the observations (here we have four variables for each) and
    # Y denotes the corresponding labels ("left", "keep", "right").
    def train(self, X, Y):
        '''
        Collect the data and calculate mean and standard variation
        for each class. Record them for later use in prediction.
        '''
        # x in [s, d, s', d']
        # y in label(left, keep, right)
        value_dict = {'left': {'s':[], 'd':[], 's_dot':[], 'd_dot':[]}, 'keep': {'s':[], 'd':[], 's_dot':[], 'd_dot':[]}, 'right': {'s':[], 'd':[], 's_dot':[], 'd_dot':[]}}
        for x, y in zip(X, Y):
            s, d, s_dot, d_dot = self.process_vars(x)
            value_dict[y]['s'].append(s)
            value_dict[y]['d'].append(d)
            value_dict[y]['s_dot'].append(s_dot)
            value_dict[y]['d_dot'].append(d_dot)
        self.mean = {'left':[0, 0, 0, 0], 'keep':[0, 0, 0, 0], 'right':[0, 0, 0, 0]}
        self.var = {'left':[0, 0, 0, 0], 'keep':[0, 0, 0, 0], 'right':[0, 0, 0, 0]}
        for key in value_dict.keys():
            for i, ele in enumerate(value_dict[key].keys()):
                self.mean[key][i] = np.mean(value_dict[key][ele])
                self.var[key][i] = np.std(value_dict[key][ele])


    # Given an observation (s, s_dot, d, d_dot), predict which behaviour
    # the vehicle is going to take using GNB.
    def predict(self, observation):
        '''
        Calculate Gaussian probability for each variable based on the
        mean and standard deviation calculated in the training process.
        Multiply all the probabilities for variables, and then
        normalize them to get conditional probabilities.
        Return the label for the highest conditional probability.
        '''
        probs = [1., 1., 1.]
        for i, key in enumerate(self.classes):
            for j in range(4):
                probs[i] *= gaussian_prob(observation[j], self.mean[key][j], self.var[key][j])
        # conditional probability를 적용해도 각 class가 선택될 확률이 같다면 해줄 필요가 없음 (현재로써는)
        # normalize
        condition_prob = [1/3, 1/3, 1/3]
        for i in range(len(probs)):
            probs[i] *= condition_prob[i]

        return self.classes[np.argmax(probs)]

