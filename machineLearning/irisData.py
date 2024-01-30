import pandas as pd
import numpy as np
import sklearn
from sklearn import datasets

if __name__ == '__main__':
    iris = datasets.load_iris()
    print(type(iris))
    # print(iris)
    print(type(iris.data))
    print(iris.data)
    sklearn.utils.Bunch