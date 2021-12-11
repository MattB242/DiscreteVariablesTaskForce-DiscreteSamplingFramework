# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 14:28:12 2021

@author: efthi
"""

from discretesampling import decision_tree as dt
from discretesampling.algorithms import DiscreteVariableMCMC, DiscreteVariableSMC

from sklearn import datasets
from sklearn.model_selection import train_test_split
import copy
import random
import math
import numpy as np

data = datasets.load_wine()

X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.30,random_state=5)

a = 0.01
b = 5
target = dt.TreeTarget(a,b)
initialProposal = dt.TreeInitialProposal(X_train, y_train)

dtMCMC = DiscreteVariableMCMC(dt.Tree, target, initialProposal)
treeSamples = dtMCMC.sample(5000)

mcmcLabels = [dt.stats(x, X_test).predict(X_test) for x in treeSamples]
mcmcAccuracy = [dt.accuracy(y_test, x) for x in mcmcLabels]

print("MCMC mean accuracy: ", np.mean(mcmcAccuracy[2500:4999]))

dtSMC = DiscreteVariableSMC(dt.Tree, target, initialProposal)
treeSMCSamples = dtSMC.sample(10,1000)

smcLabels = [dt.stats(x, X_test).predict(X_test) for x in treeSMCSamples]
smcAccuracy = [dt.accuracy(y_test, x) for x in smcLabels]

print("SMC mean accuracy: ", np.mean(smcAccuracy))