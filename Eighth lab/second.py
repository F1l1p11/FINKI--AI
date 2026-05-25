import os

os.environ['OPENBLAS_NUM_THREADS'] = '1'
# from submission_script import *
# from dataset_script import dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Ova e primerok od podatochnoto mnozestvo, za treniranje/evaluacija koristete ja
# importiranata promenliva dataset
dataset_sample = [[180.0, 23.6, 25.2, 27.9, 25.4, 14.0, 'Roach'],
                  [12.2, 11.5, 12.2, 13.4, 15.6, 10.4, 'Smelt'],
                  [135.0, 20.0, 22.0, 23.5, 25.0, 15.0, 'Perch'],
                  [1600.0, 56.0, 60.0, 64.0, 15.0, 9.6, 'Pike'],
                  [120.0, 20.0, 22.0, 23.5, 26.0, 14.5, 'Perch']]

if __name__ == '__main__':

    col_index = int(input())
    n_trees = int(input())
    criterion = input()

    sample = list(map(float, input().split()))

    new_dataset = []

    # remove selected column
    for row in dataset_sample:
        new_row = row[:col_index] + row[col_index + 1:]
        new_dataset.append(new_row)

    # split features and labels
    X = [row[:-1] for row in new_dataset]
    Y = [row[-1] for row in new_dataset]

    # 85% train, 15% test
    split = int(0.85 * len(X))

    train_X = X[:split]
    train_Y = Y[:split]

    test_X = X[split:]
    test_Y = Y[split:]

    # remove same column from sample
    sample = sample[:col_index] + sample[col_index + 1:]

    # classifier
    classifier = RandomForestClassifier(
        n_estimators=n_trees,
        criterion=criterion,
        random_state=0
    )

    classifier.fit(train_X, train_Y)

    # predictions on test set
    predictions = classifier.predict(test_X)

    accuracy = accuracy_score(test_Y, predictions)

    # prediction for new sample
    predicted_class = classifier.predict([sample])[0]

    probabilities = classifier.predict_proba([sample])[0]

    print(f'Accuracy: {accuracy}')
    print(predicted_class)
    print(probabilities)

    # submit na trenirachkoto mnozestvo
    # submit_train_data(train_X, train_Y)

    # submit na testirachkoto mnozestvo
    # submit_test_data(test_X, test_Y)

    # submit na klasifikatorot
    # submit_classifier(classifier)