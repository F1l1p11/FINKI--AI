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

if __name__ == '__main__':

    # FIXED percentage
    percent = 70
    threshold = 0.9

    record = input().split()

    X = [row[:-1] for row in dataset]
    y = [row[-1] for row in dataset]

    n = len(X)
    split_index = int(n * percent / 100)

    encoder = OrdinalEncoder()
    X_enc = encoder.fit_transform(X)

    train_X = X_enc[:split_index]
    test_X = X_enc[split_index:]

    train_y = y[:split_index]
    test_y = y[split_index:]

    model = CategoricalNB()
    model.fit(train_X, train_y)

    # ---- NEW LOGIC ----
    probs_test = model.predict_proba(test_X)
    predictions_test = model.predict(test_X)

    confident_correct = 0
    confident_total = 0

    for i in range(len(test_X)):
        max_prob = max(probs_test[i])

        if max_prob >= threshold:
            confident_total += 1
            if predictions_test[i] == test_y[i]:
                confident_correct += 1

    if confident_total > 0:
        accuracy = confident_correct / confident_total
    else:
        accuracy = 0

    # ---- RECORD PREDICTION ----
    record_enc = encoder.transform([record])

    prediction_class = model.predict(record_enc)[0]
    probs = model.predict_proba(record_enc)[0]
    max_prob = max(probs)

    passes_threshold = max_prob >= threshold

    # ---- OUTPUT ----
    print(accuracy)
    print(prediction_class)
    print(probs)
    print(passes_threshold)

    # ---- SUBMIT ----
    # submit_train_data(train_X, train_y)
    # submit_test_data(test_X, test_y)
    # submit_classifier(model)
    # submit_encoder(encoder)