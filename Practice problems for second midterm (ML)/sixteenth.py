import os

os.environ['OPENBLAS_NUM_THREADS'] = '1'

# from dataset_script import dataset
from sklearn.tree import DecisionTreeClassifier

dataset = [] # <- delete this in online compiler so the program works

if __name__ == '__main__':
    #first p percent for training

    p = int(input())
    criterion = input()
    max_leafs = int(input())

    split = int(len(dataset) * p / 100)

    train_X = [row[:-1] for row in dataset[:split]]
    train_Y = [row[-1] for row in dataset[:split]]

    test_X = [row[:-1] for row in dataset[split:]]
    test_Y = [row[-1] for row in dataset[split:]]

    model = DecisionTreeClassifier(criterion=criterion, max_leaf_nodes=max_leafs, random_state=0)
    model.fit(train_X, train_Y)
    prediction_DTC = model.predict(test_X)

    accuracy = sum (1 for v,p in zip(test_Y, prediction_DTC) if v == p) / len(test_Y)

    type_fish = {'Perch', 'Roach', 'Bream'}
    models = {}

    for fish in type_fish:
        temp_train_Y = [1 if value == fish else 0 for value in train_Y]
        model_temp = DecisionTreeClassifier(criterion=criterion, max_leaf_nodes=max_leafs, random_state=0)
        model_temp.fit(train_X, temp_train_Y)
        models[fish] = model_temp

    correct = 0

    for x, true_class in zip (test_X, test_Y):
        valid = True

        for fish in type_fish:
            prediction = models[fish].predict([x])[0]

            if fish == true_class:
                if prediction != 1:
                    valid = False
            else:
                 if prediction != 0:
                     valid = False
        if valid:
            correct += 1

    accuracy_2 = correct / len(test_Y)
    print (f'Tochnost so originalniot klasifikator: {accuracy}')
    print (f'Tochnost so kolekcija od klasifikatori: {accuracy_2}')
