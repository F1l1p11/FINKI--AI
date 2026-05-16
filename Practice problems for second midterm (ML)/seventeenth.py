import os

os.environ['OPENBLAS_NUM_THREADS'] = '1'


# from dataset_script import dataset
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import MinMaxScaler

dataset = [] # <- delete this in online compiler so the program works
if __name__ == '__main__':
    criterion = int(input())
    p = int(input())
    # c == 0 first percent for training
    # c == 1 first percent for testing

    new_dataset = []
    for row in dataset:
        sum_temp = row[0] + row[10]
        new_row = [sum_temp] + row[1:10] + [row[-1]]
        new_dataset.append(new_row)

    if criterion == 0:
        class_bad = [row for row in new_dataset if row[-1] == "bad"]
        class_good = [row for row in new_dataset if row[-1] == "good"]

        split_bad = int (len(class_bad) * p / 100)
        split_good = int (len(class_good) * p / 100)

        train_X = [row[:-1] for row in class_bad[:split_bad]] + [row[:-1] for row in class_good[:split_good]]
        train_Y = [row[-1] for row in class_bad[:split_bad]] + [row[-1] for row in class_good[:split_good]]

        test_X = [row[:-1] for row in class_bad[split_bad:]] + [row[:-1] for row in class_good[split_good:]]
        test_Y = [row[-1] for row in class_bad[split_bad:]] + [row[-1] for row in class_good[split_good:]]
    else:
        class_bad = [row for row in new_dataset if row[-1] == "bad"]
        class_good = [row for row in new_dataset if row[-1] == "good"]

        split_bad = int (len(class_bad) * (100 - p) / 100)
        split_good = int (len(class_good) * (100 - p) / 100)

        train_X = [row[:-1] for row in class_bad[split_bad:]] + [row[:-1] for row in class_good[split_good:]]
        train_Y = [row[-1] for row in class_bad[split_bad:]] + [row[-1] for row in class_good[split_good:]]

        test_X = [row[:-1] for row in class_bad[:split_bad]] + [row[:-1] for row in class_good[:split_good]]
        test_Y = [row[-1] for row in class_bad[:split_bad]] + [row[-1] for row in class_good[:split_good]]

    scaler = MinMaxScaler(feature_range=(-1, 1))

    train_X_scaled = scaler.fit_transform(train_X)
    test_X_scaled = scaler.transform(test_X)

    model1 = GaussianNB()
    model1.fit(train_X, train_Y)
    prediction_1 = model1.predict(test_X)

    accuracy_1 = sum(1 for a, b in zip(test_Y, prediction_1) if a == b) / len(test_Y)

    model2 = GaussianNB()
    model2.fit(train_X_scaled, train_Y)
    prediction_2 = model2.predict(test_X_scaled)

    accuracy_2 = sum(1 for a, b in zip(test_Y, prediction_2) if a == b) / len(test_Y)

    print (f'Tochnost so zbir na koloni: {accuracy_1}')
    print (f'Tochnost so zbir na koloni i skaliranje: {accuracy_2}')
