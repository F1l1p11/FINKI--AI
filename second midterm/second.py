import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier

import warnings
warnings.filterwarnings("ignore")

from data.dataFirst import dataset

if __name__ == '__main__':
    C = int(input())
    N = int(input())
    S = int(input())

    original_data = []
    for row in dataset:
        new_row = row[:-1]
        if row[-1] >= 50:
            new_row.append(1)
        else:
            new_row.append(0)
        original_data.append(new_row)

    split = int(len(original_data) * 0.7)

    train_X_org = [row[:-1] for row in original_data[:split]]
    train_Y_org = [row[-1] for row in original_data[:split]]

    test_X_org = [row[:-1] for row in original_data[split:]]
    test_Y_org = [row[-1] for row in original_data[split:]]

    removed_anomalies = []
    for row in original_data:
        new_row = row[:]
        if row[3] > C:
            new_row[3] = C
        if row[4] > N:
            new_row[4] = N
        if row[5] > S:
            new_row[5] = S
        removed_anomalies.append(new_row)

    train_X_rm = [row[:-1] for row in removed_anomalies[:split]]
    train_Y_rm = [row[-1] for row in removed_anomalies[:split]]

    test_X_rm = [row[:-1] for row in removed_anomalies[split:]]
    test_Y_rm = [row[-1] for row in removed_anomalies[split:]]

    # scaled

    train_X_sc = [row[:-1] for row in original_data[:split]]
    train_Y_sc = [row[-1] for row in original_data[:split]]

    test_X_sc = [row[:-1] for row in original_data[split:]]
    test_Y_sc = [row[-1] for row in original_data[split:]]

    scaler = StandardScaler()
    scaler.fit(train_X_sc)
    train_X_sc = scaler.transform(train_X_org)
    test_X_sc = scaler.transform(test_X_org)

    train_X_rm_sc = [row[:-1] for row in removed_anomalies[:split]]
    train_Y_rm_sc = [row[-1] for row in removed_anomalies[:split]]

    test_X_rm_sc = [row[:-1] for row in removed_anomalies[split:]]
    test_Y_rm_sc = [row[-1] for row in removed_anomalies[split:]]

    scaler = StandardScaler()
    scaler.fit(train_X_rm_sc)
    train_X_rm_sc = scaler.transform(train_X_rm_sc)
    test_X_rm_sc = scaler.transform(test_X_rm_sc)

    dictionary_something = {0: [train_X_org, train_Y_org, test_X_org, test_Y_org],
                            1: [train_X_rm, train_Y_rm, test_X_rm, test_Y_rm],
                            2: [train_X_sc, train_Y_sc, test_X_sc, test_Y_sc],
                            3: [train_X_rm_sc, train_Y_rm_sc, test_X_rm_sc, test_Y_rm_sc]}

    accuracies = []

    for i in range(4):
        model = MLPClassifier(hidden_layer_sizes=(50,), activation='relu', learning_rate_init=0.001,
                              max_iter=25, random_state=0)
        train_X = dictionary_something[i][0]
        train_Y = dictionary_something[i][1]
        test_X = dictionary_something[i][2]
        test_Y = dictionary_something[i][3]
        model.fit(train_X, train_Y)
        prediction = model.predict(test_X)
        accuracies.append(sum(1 for v, t in zip(prediction, test_Y) if v == t) / len(test_Y))

    print("Accuracy with:")
    print(f'The original dataset: {accuracies[0]}')
    print(f'Removed anomalies: {accuracies[1]}')
    print(f'Scaled attributes: {accuracies[2]}')
    print(f'Removed anomalies and scaled attributes: {accuracies[3]}')
