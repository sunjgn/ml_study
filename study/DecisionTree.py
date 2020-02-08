#coding:utf-8
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

def read_file(file_name):
    # 第一列作为索引
    data = pd.read_csv(file_name, index_col= 0)

    data.drop(['Name', 'Ticket', 'Cabin'], axis = 1, inplace = True)

    data['Sex'] = (data['Sex'] == 'male').astype('int')

    labels = data['Embarked'].unique().tolist()

    data['Embarked'] = data['Embarked'].apply(lambda n: labels.index(n))

    data = data.fillna(0)

    return data

def process_data(data):
    y = data['Survived'].values
    x = data.drop(['Survived'], axis =1).values

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    clf = DecisionTreeClassifier()
    clf.fit(x_train, y_train)
    train_score = clf.score(x_train, y_train)
    test_score = clf.score(x_test, y_test)

    print ('train score: {0}\ntest score: {1}'.format(train_score, test_score))

if __name__ == '__main__':
    file_name = '/Users/sunjian13/Downloads/titanic/train.csv'
    data = read_file(file_name)
    process_data(data)



