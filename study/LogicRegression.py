import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


def get_data():
    cancer = load_breast_cancer()
    x = cancer.data
    y = cancer.target
    print ("data shape: {0}; positive: {1}, negative: {2}".format(x.shape, y[y == 1].shape[0], y[y == 0].shape[0]))
    print (cancer.data[0])
    print cancer.feature_names
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2)
    model = LogisticRegression()
    model.fit(x_train, y_train)
    train_score = model.score(x_train, y_train)
    test_score = model.score(x_test, y_test)
    print ('train score: {train:.6f} and test score: {test:.6f}'.format(train = train_score, test = test_score))
    y_pred = model.predict(x_test)
    y_pred_proba = model.predict_proba(x_test)
    print y_pred_proba
    # print y_pred_proba
    y_pred_proba_0 = y_pred_proba[:, 0] > 0.1
    result = y_pred_proba[y_pred_proba_0]
    print y_pred_proba_0
    print '---------------------------'
    print result
if __name__ == '__main__':
    get_data()