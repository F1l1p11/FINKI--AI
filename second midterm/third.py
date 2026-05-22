import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

from data.dataSecond import dataset

if __name__ == '__main__':
    N = int(input())
    M = int(input())

    new_dataset = []
    for row in dataset:
        if row[-1] == 'Perch' or row[-1] == 'Roach' or row[-1] == 'Bream':
            new_dataset.append(row)

    split = int (len(new_dataset) / 3)

    first_subset = new_dataset[:split]
    second_subset = new_dataset[split:split*2]
    third_subset = new_dataset[split*2:]

    sets = [first_subset, second_subset, third_subset]

    accuracy_trees = []
    accuracy_bayes_tree = []
    for i in range(3):
        training_set = []
        testing_set = []
        for j in range(3):
            if j != i:
                training_set += sets[j]
            else:
                testing_set += sets[j]
        train_X = [row[:-1] for row in training_set]
        train_Y = [row[-1] for row in training_set]

        test_X = [row[:-1] for row in testing_set]
        test_Y = [row[-1] for row in testing_set]

        model_tree = RandomForestClassifier(criterion='gini',n_estimators=N,random_state=0)
        model_tree.fit(train_X, train_Y)
        prediction_tree = model_tree.predict(test_X)
        accuracy_trees.append(accuracy_score(test_Y, prediction_tree))


        model_bayes = GaussianNB()
        model_second_tree = DecisionTreeClassifier(criterion='gini',max_depth=M,random_state=0)
        model_bayes.fit(train_X, train_Y)
        model_second_tree.fit(train_X, train_Y)
        prediction_bayes = model_bayes.predict(test_X)
        prediction_second_tree = model_second_tree.predict(test_X)

        temp_accuracy = 0
        for index,true in enumerate(test_Y):
            proba_1 = model_bayes.predict_proba([test_X[index]])[0]
            proba_2 = model_second_tree.predict_proba([test_X[index]])[0]
            if prediction_bayes[index] == prediction_second_tree[index] and prediction_second_tree[index] == true:
                temp_accuracy += 1
            else:
                if prediction_bayes[index] == true and max(proba_1) > max(proba_2):
                    temp_accuracy += 1
                elif prediction_second_tree[index] == true and max(proba_1) < max(proba_2):
                    temp_accuracy += 1

        accuracy_bayes_tree.append(temp_accuracy/len(test_Y))

    print(f'Accuracy with random forest: {sum(accuracy_trees) / len(accuracy_trees)}')
    print(f'Accuracy with naive bayes and decision tree: {sum(accuracy_bayes_tree) / len(accuracy_bayes_tree)}')