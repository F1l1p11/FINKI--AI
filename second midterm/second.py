import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import warnings
warnings.filterwarnings("ignore")

from data.dataFirst import dataset
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

if __name__ == '__main__':
    C = int(input())
    N = int(input())
    S = int(input())

    new_dataset = []
    for row in dataset:
        new_row = row[:-1]
        if row[-1] >= 50:
            new_row.append(1)
        else:
            new_row.append(0)
        new_dataset.append(new_row)

    split = int(len(new_dataset) * 0.7)

    removed_anomaly = []

    for row in new_dataset:
        new_row = row[:]
        if row[3] > C:
            new_row[3] = C
        if row[4] > N:
            new_row[4] = N
        if row[5] > S:
            new_row[5] = S
        removed_anomaly.append(new_row)

    model = MLPClassifier (hidden_layer_sizes=(50,),activation='relu',learning_rate_init=0.001,max_iter=25)

    datasets = [new_dataset,removed_anomaly,new_dataset,removed_anomaly]
    accuracy = []
    for i in range(4):
        dataset = datasets[i]
        train_X = [row[:-1] for row in dataset[:split]]
        train_Y = [row[-1] for row in dataset[:split]]
        
        test_X = [row[:-1] for row in dataset[split:]]
        test_Y = [row[-1] for row in dataset[split:]]

        if i == 2 or i == 3:
            scaler = StandardScaler()
            scaler.fit(train_X)
            train_X = scaler.transform(train_X)
            test_X = scaler.transform(test_X)

        model = MLPClassifier(hidden_layer_sizes=(50,), activation='relu', learning_rate_init=0.001, max_iter=25, random_state=0)

        model.fit(train_X, train_Y)
        predictions = model.predict(test_X)
        accuracy.append(accuracy_score(test_Y, predictions))

    print("Accuracy with:")
    print(f'The original dataset: {accuracy[0]}')
    print(f'Removed anomalies: {accuracy[1]}')
    print(f'Scaled attributes: {accuracy[2]}')
    print(f'Removed anomalies and scaled attributes: {accuracy[3]}')
