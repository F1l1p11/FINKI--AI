import os

os.environ['OPENBLAS_NUM_THREADS'] = '1'
# from submission_script import *
# from dataset_script import dataset

from sklearn.preprocessing import OrdinalEncoder
from sklearn.naive_bayes import CategoricalNB

def read_dataset_from_csv(filepath):
    dataset_temp = []
    with open(filepath, 'r') as file:
        for row in file:
            temp = []
            for char in row:
                if char.isdigit() or char.isalpha():
                    temp.append(char)
            dataset_temp.append(temp)
    return dataset_temp

dataset = read_dataset_from_csv('zad1_dataset.csv')

dataset_sample = [['C', 'S', 'O', '1', '2', '1', '1', '2', '1', '2', '0'],
                  ['D', 'S', 'O', '1', '3', '1', '1', '2', '1', '2', '0'],
                  ['C', 'S', 'O', '1', '3', '1', '1', '2', '1', '1', '0'],
                  ['D', 'S', 'O', '1', '3', '1', '1', '2', '1', '2', '0'],
                  ['D', 'A', 'O', '1', '3', '1', '1', '2', '1', '2', '0'],]

if __name__ == '__main__':
    percent = int(input())
    record = input().split()

    X = [row[:-1] for row in dataset]
    y = [row[-1] for row in dataset]

    n = len(X)
    split_index = int(n * percent / 100)

    encoder = OrdinalEncoder()
    X_enc = encoder.fit_transform(X).tolist()

    train_X = X_enc[:split_index]
    test_X = X_enc[split_index:]

    train_y = y[:split_index]
    test_y = y[split_index:]

    model = CategoricalNB()
    model.fit(train_X, train_y)

    predictions = model.predict(test_X)

    correct = 0
    for p, t in zip(predictions, test_y):
        if p == t:
            correct += 1
    accuracy = correct / len(test_y)

    record_enc = encoder.transform([record])

    prediction_class = model.predict(record_enc)[0]
    probs = model.predict_proba(record_enc)

    print(accuracy)
    print(prediction_class)
    print(probs)


    #submit_train_data(train_X, train_y)
    #submit_test_data(test_X, test_y)
    #submit_classifier(model)
    #submit_encoder(encoder)
