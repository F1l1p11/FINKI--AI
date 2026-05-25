import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'

import warnings
warnings.filterwarnings("ignore")

from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MaxAbsScaler
from sklearn.metrics import accuracy_score

dataset = [[180.0, 23.6, 25.2, 27.9, 25.4, 14.0, 'Roach'],
           [12.2, 11.5, 12.2, 13.4, 15.6, 10.4, 'Smelt'],
           [135.0, 20.0, 22.0, 23.5, 25.0, 15.0, 'Perch'],
           [1600.0, 56.0, 60.0, 64.0, 15.0, 9.6, 'Pike'],
           [120.0, 20.0, 22.0, 23.5, 26.0, 14.5, 'Perch'],
           [273.0, 23.0, 25.0, 28.0, 39.6, 14.8, 'Silver Bream'],
           [320.0, 27.8, 30.0, 31.6, 24.1, 15.1, 'Perch'],
           [160.0, 21.1, 22.5, 25.0, 25.6, 15.2, 'Roach'],
           [700.0, 30.4, 33.0, 38.3, 38.8, 13.8, 'Bream'],
           [500.0, 29.5, 32.0, 37.3, 37.3, 13.6, 'Bream'],
           [290.0, 24.0, 26.3, 31.2, 40.0, 13.8, 'Bream'],
           [650.0, 31.0, 33.5, 38.7, 37.4, 14.8, 'Bream'],
           [500.0, 26.8, 29.7, 34.5, 41.1, 15.3, 'Bream'],
           [260.0, 25.4, 27.5, 28.9, 24.8, 15.0, 'Perch'],
           [80.0, 17.2, 19.0, 20.2, 27.9, 15.1, 'Perch'],
           [850.0, 32.8, 36.0, 41.6, 40.6, 14.9, 'Bream'],
           [345.0, 36.0, 38.5, 41.0, 15.6, 9.7, 'Pike'],
           [567.0, 43.2, 46.0, 48.7, 16.0, 10.0, 'Pike'],
           [55.0, 13.5, 14.7, 16.5, 41.5, 14.1, 'Silver Bream'],
           [78.0, 16.8, 18.7, 19.4, 26.8, 16.1, 'Perch'],
           [950.0, 38.0, 41.0, 46.5, 37.9, 13.7, 'Bream'],
           [306.0, 25.6, 28.0, 30.8, 28.5, 15.2, 'Whitewish'],
           [6.7, 9.3, 9.8, 10.8, 16.1, 9.7, 'Smelt'],
           [714.0, 32.7, 36.0, 41.5, 39.8, 14.1, 'Bream'],
           [197.0, 23.5, 25.6, 27.0, 24.3, 15.7, 'Perch'],
           [1000.0, 41.1, 44.0, 46.6, 26.8, 16.3, 'Perch'],
           [685.0, 34.0, 36.5, 39.0, 27.9, 17.6, 'Perch'],
           [169.0, 22.0, 24.0, 27.2, 27.7, 14.1, 'Roach'],
           [125.0, 19.0, 21.0, 22.5, 25.3, 16.3, 'Perch'],
           [1000.0, 33.5, 37.0, 42.6, 44.5, 15.5, 'Bream'],
           [900.0, 36.5, 39.0, 41.4, 26.9, 18.1, 'Perch'],
           [19.7, 13.2, 14.3, 15.2, 18.9, 13.6, 'Smelt'],
           [150.0, 20.4, 22.0, 24.7, 23.5, 15.2, 'Roach'],
           [120.0, 17.5, 19.0, 21.3, 39.4, 13.7, 'Silver Bream'],
           [140.0, 19.0, 20.7, 23.2, 36.8, 14.2, 'Silver Bream'],
           [290.0, 24.0, 26.0, 29.2, 30.4, 15.4, 'Roach'],
           [725.0, 31.8, 35.0, 40.9, 40.0, 14.8, 'Bream'],
           [1000.0, 40.2, 43.5, 46.0, 27.4, 17.7, 'Perch'],
           [188.0, 22.6, 24.6, 26.2, 25.7, 15.9, 'Perch'],
           [242.0, 23.2, 25.4, 30.0, 38.4, 13.4, 'Bream'],
           [475.0, 28.4, 31.0, 36.2, 39.4, 14.1, 'Bream'],
           [700.0, 30.4, 33.0, 38.5, 38.8, 13.5, 'Bream'],
           [120.0, 18.6, 20.0, 22.2, 28.0, 16.1, 'Roach'],
           [820.0, 36.6, 39.0, 41.3, 30.1, 17.8, 'Perch'],
           [540.0, 28.5, 31.0, 34.0, 31.6, 19.3, 'Whitewish'],
           [150.0, 20.5, 22.5, 24.0, 28.3, 15.1, 'Perch'],
           [161.0, 22.0, 23.4, 26.7, 25.9, 13.6, 'Roach'],
           [60.0, 14.3, 15.5, 17.4, 37.8, 13.3, 'Silver Bream'],
           [840.0, 32.5, 35.0, 37.3, 30.8, 20.9, 'Perch'],
           [300.0, 24.0, 26.0, 29.0, 39.2, 14.6, 'Silver Bream'],
           [300.0, 25.2, 27.3, 28.7, 29.0, 17.9, 'Perch'],
           [180.0, 23.0, 25.0, 26.5, 24.3, 13.9, 'Perch'],
           [85.0, 18.2, 20.0, 21.0, 24.2, 13.2, 'Perch'],
           [130.0, 20.5, 22.5, 24.0, 24.4, 15.1, 'Perch'],
           [900.0, 37.0, 40.0, 42.5, 27.6, 17.0, 'Perch'],
           [9.9, 11.3, 11.8, 13.1, 16.9, 8.9, 'Smelt'],
           [620.0, 31.5, 34.5, 39.7, 39.1, 13.3, 'Bream'],
           [720.0, 32.0, 35.0, 40.6, 40.3, 15.0, 'Bream'],
           [270.0, 23.6, 26.0, 28.7, 29.2, 14.8, 'Whitewish'],
           [40.0, 13.8, 15.0, 16.0, 23.9, 15.2, 'Perch'],
           [5.9, 7.5, 8.4, 8.8, 24.0, 16.0, 'Perch'],
           [115.0, 19.0, 21.0, 22.5, 26.3, 14.7, 'Perch'],
           [110.0, 20.0, 22.0, 23.5, 23.5, 17.0, 'Perch'],
           [300.0, 26.9, 28.7, 30.1, 25.2, 15.4, 'Perch'],
           [363.0, 26.3, 29.0, 33.5, 38.0, 13.3, 'Bream'],
           [690.0, 34.6, 37.0, 39.3, 26.9, 16.2, 'Perch'],
           [820.0, 37.1, 40.0, 42.5, 26.2, 15.6, 'Perch'],
           [19.9, 13.8, 15.0, 16.2, 18.1, 11.6, 'Smelt'],
           [40.0, 12.9, 14.1, 16.2, 25.6, 14.0, 'Roach'],
           [390.0, 27.6, 30.0, 35.0, 36.2, 13.4, 'Bream'],
           [1250.0, 52.0, 56.0, 59.7, 17.9, 11.7, 'Pike'],
           [87.0, 18.2, 19.8, 22.2, 25.3, 14.3, 'Roach'],
           [9.8, 10.7, 11.2, 12.4, 16.8, 10.3, 'Smelt'],
           [13.4, 11.7, 12.4, 13.5, 18.0, 9.4, 'Smelt'],
           [975.0, 37.4, 41.0, 45.9, 40.6, 14.7, 'Bream'],
           [1100.0, 39.0, 42.0, 44.6, 28.7, 15.4, 'Perch'],
           [130.0, 20.0, 22.0, 23.5, 26.0, 15.0, 'Perch'],
           [450.0, 27.6, 30.0, 35.1, 39.9, 13.8, 'Bream'],
           [200.0, 30.0, 32.3, 34.8, 16.0, 9.7, 'Pike'],
           [340.0, 23.9, 26.5, 31.1, 39.8, 15.1, 'Bream'],
           [700.0, 34.0, 36.0, 38.3, 27.7, 17.6, 'Perch'],
           [170.0, 21.5, 23.5, 25.0, 25.1, 14.9, 'Perch'],
           [500.0, 29.1, 31.5, 36.4, 37.8, 12.0, 'Bream'],
           [150.0, 18.4, 20.0, 22.4, 39.7, 14.7, 'Silver Bream'],
           [145.0, 20.7, 22.7, 24.2, 24.6, 15.0, 'Perch'],
           [85.0, 17.8, 19.6, 20.8, 24.7, 14.6, 'Perch'],
           [600.0, 29.4, 32.0, 37.2, 40.2, 13.9, 'Bream'],
           [300.0, 34.8, 37.3, 39.8, 15.8, 10.1, 'Pike'],
           [456.0, 40.0, 42.5, 45.5, 16.0, 9.5, 'Pike'],
           [540.0, 40.1, 43.0, 45.8, 17.0, 11.2, 'Pike'],
           [12.2, 12.1, 13.0, 13.8, 16.5, 9.1, 'Smelt'],
           [100.0, 16.2, 18.0, 19.2, 27.2, 17.3, 'Perch'],
           [300.0, 32.7, 35.0, 38.8, 15.3, 11.3, 'Pike'],
           [700.0, 31.9, 35.0, 40.5, 40.1, 13.8, 'Bream'],
           [610.0, 30.9, 33.5, 38.6, 40.5, 13.3, 'Bream'],
           [700.0, 34.5, 37.0, 39.4, 27.5, 15.9, 'Perch'],
           [70.0, 15.7, 17.4, 18.5, 24.8, 15.9, 'Perch'],
           [955.0, 35.0, 38.5, 44.0, 41.1, 14.3, 'Bream'],
           [514.0, 30.5, 32.8, 34.0, 29.5, 17.7, 'Perch'],
           [51.5, 15.0, 16.2, 17.2, 26.7, 15.3, 'Perch'],
           [272.0, 25.0, 27.0, 30.6, 28.0, 15.6, 'Roach'],
           [500.0, 28.5, 30.7, 36.2, 39.3, 13.7, 'Bream'],
           [9.8, 11.4, 12.0, 13.2, 16.7, 8.7, 'Smelt'],
           [510.0, 40.0, 42.5, 45.5, 15.0, 9.8, 'Pike'],
           [925.0, 36.2, 39.5, 45.3, 41.4, 14.9, 'Bream'],
           [1015.0, 37.0, 40.0, 42.4, 29.2, 17.6, 'Perch'],
           [1550.0, 56.0, 60.0, 64.0, 15.0, 9.6, 'Pike'],
           [1000.0, 37.3, 40.0, 43.5, 28.4, 15.0, 'Whitewish'],
           [920.0, 35.0, 38.5, 44.1, 40.9, 14.3, 'Bream'],
           [140.0, 21.0, 22.5, 25.0, 26.2, 13.3, 'Roach'],
           [218.0, 25.0, 26.5, 28.0, 25.6, 14.8, 'Perch'],
           [9.7, 10.4, 11.0, 12.0, 18.3, 11.5, 'Smelt'],
           [69.0, 16.5, 18.2, 20.3, 26.1, 13.9, 'Roach'],
           [110.0, 19.0, 21.0, 22.5, 25.3, 15.8, 'Perch'],
           [150.0, 21.0, 23.0, 24.5, 21.3, 14.8, 'Perch'],
           [160.0, 20.5, 22.5, 25.3, 27.8, 15.1, 'Roach'],
           [7.0, 10.1, 10.6, 11.6, 14.9, 9.9, 'Smelt'],
           [78.0, 17.5, 18.8, 21.2, 26.3, 13.7, 'Roach'],
           [450.0, 26.8, 29.7, 34.7, 39.2, 14.2, 'Bream'],
           [556.0, 32.0, 34.5, 36.5, 28.1, 17.5, 'Perch'],
           [1650.0, 59.0, 63.4, 68.0, 15.9, 11.0, 'Pike'],
           [110.0, 19.1, 20.8, 23.1, 26.7, 14.7, 'Roach'],
           [685.0, 31.4, 34.0, 39.2, 40.8, 13.7, 'Bream'],
           [200.0, 22.1, 23.5, 26.8, 27.6, 15.4, 'Roach'],
           [770.0, 44.8, 48.0, 51.2, 15.0, 10.5, 'Pike'],
           [7.5, 10.0, 10.5, 11.6, 17.0, 10.0, 'Smelt'],
           [8.7, 10.8, 11.3, 12.6, 15.7, 10.2, 'Smelt'],
           [500.0, 42.0, 45.0, 48.0, 14.5, 10.2, 'Pike'],
           [170.0, 19.0, 20.7, 23.2, 40.5, 14.7, 'Silver Bream'],
           [120.0, 20.0, 22.0, 23.5, 24.0, 15.0, 'Perch'],
           [145.0, 19.8, 21.5, 24.1, 40.4, 13.1, 'Silver Bream'],
           [130.0, 19.3, 21.3, 22.8, 28.0, 15.5, 'Perch'],
           [850.0, 36.9, 40.0, 42.3, 28.2, 16.8, 'Perch'],
           [265.0, 25.4, 27.5, 28.9, 24.4, 15.0, 'Perch'],
           [0.0, 19.0, 20.5, 22.8, 28.4, 14.7, 'Roach'],
           [680.0, 31.8, 35.0, 40.6, 38.1, 15.1, 'Bream'],
           [90.0, 16.3, 17.7, 19.8, 37.4, 13.5, 'Silver Bream'],
           [575.0, 31.3, 34.0, 39.5, 38.3, 14.1, 'Bream'],
           [390.0, 29.5, 31.7, 35.0, 27.1, 15.3, 'Roach'],
           [225.0, 22.0, 24.0, 25.5, 28.6, 14.6, 'Perch'],
           [10.0, 11.3, 11.8, 13.1, 16.9, 9.8, 'Smelt'],
           [1000.0, 39.8, 43.0, 45.2, 26.4, 16.1, 'Perch'],
           [500.0, 28.7, 31.0, 36.2, 39.7, 13.3, 'Bream'],
           [120.0, 19.4, 21.0, 23.7, 25.8, 13.9, 'Roach'],
           [430.0, 35.5, 38.0, 40.5, 18.0, 11.3, 'Pike'],
           [200.0, 21.2, 23.0, 25.8, 40.1, 14.2, 'Silver Bream'],
           [250.0, 25.9, 28.0, 29.4, 26.6, 14.3, 'Perch'],
           [800.0, 33.7, 36.4, 39.6, 29.7, 16.6, 'Whitewish'],
           [32.0, 12.5, 13.7, 14.7, 24.0, 13.6, 'Perch'],
           [430.0, 26.5, 29.0, 34.0, 36.6, 15.1, 'Bream'],
           [145.0, 20.5, 22.0, 24.3, 27.3, 14.6, 'Roach'],
           [950.0, 48.3, 51.7, 55.1, 16.2, 11.2, 'Pike'],
           [300.0, 31.7, 34.0, 37.8, 15.1, 11.0, 'Pike'],
           [250.0, 25.4, 27.5, 28.9, 25.2, 15.8, 'Perch'],
           [650.0, 36.5, 39.0, 41.4, 26.9, 14.5, 'Perch'],
           [270.0, 24.1, 26.5, 29.3, 27.8, 14.5, 'Whitewish'],
           [600.0, 29.4, 32.0, 37.2, 41.5, 15.0, 'Bream'],
           [145.0, 22.0, 24.0, 25.5, 25.0, 15.0, 'Perch'],
           [1100.0, 40.1, 43.0, 45.5, 27.5, 16.3, 'Perch']]

if __name__ == '__main__':
    inputs = [1,5,10,20,30]
    for inputs in inputs:
        number_neurons = inputs
        #first split 80 20
        split = int(len(dataset) * 0.8)
        training_set = [row for row in dataset[:split]]
        testing_set = [row for row in dataset[split:]]

        #splitting training set in 3 subsets
        split_second = int(len(training_set) / 3)
        training_set_first = training_set[:split_second]
        training_set_second = training_set[split_second:split_second*2]
        training_set_third = training_set[split_second*2:]

        training_sets = [training_set_first, training_set_second, training_set_third]

        best_scaler_regular = None
        best_classifier_regular = None
        best_accuracy_regular = 0
        accuracy_regular = []

        best_scaler_ensemble = None
        best_classifier_ensemble = None
        best_accuracy_ensemble = 0
        accuracy_ensemble = []


        for i in range(3):
            train_X = []
            train_Y = []
            test_X = []
            test_Y = []
            for j in range(3):
                if j != i:
                    train_X += [row[:-1] for row in training_sets[j]]
                    train_Y += [row[-1] for row in training_sets[j]]
                else:
                    test_X = [row[:-1] for row in training_sets[i]]
                    test_Y = [row[-1] for row in training_sets[i]]
            scaler = MaxAbsScaler()
            train_X = scaler.fit_transform(train_X)
            test_X = scaler.transform(test_X)

            model_regular = MLPClassifier(hidden_layer_sizes=(number_neurons,),learning_rate_init=0.001,max_iter=20,random_state=0)
            model_regular.fit(train_X, train_Y)
            prediction_regular = model_regular.predict(test_X)
            accuracy_reg = accuracy_score(test_Y, prediction_regular)
            accuracy_regular.append(accuracy_reg)
            if accuracy_reg > best_accuracy_regular:
                best_accuracy_regular = accuracy_reg
                best_scaler_regular = scaler
                best_classifier_regular = model_regular

            model_ensemble_first = MLPClassifier(hidden_layer_sizes=(5,), learning_rate_init=0.001, max_iter=20,random_state=0)
            model_ensemble_second = MLPClassifier(hidden_layer_sizes=(10,), learning_rate_init=0.001, max_iter=40,random_state=0)

            model_ensemble_first.fit(train_X, train_Y)
            model_ensemble_second.fit(train_X, train_Y)

            prediction_ens_first = model_ensemble_first.predict(test_X)
            prediction_ens_second = model_ensemble_second.predict(test_X)
            probability_ens_first = model_ensemble_first.predict_proba(test_X)
            probability_ens_second = model_ensemble_second.predict_proba(test_X)

            temp_correct = 0
            for index,element in enumerate(test_Y):
                if max(probability_ens_first[index]) >= max(probability_ens_second[index]) and prediction_ens_first[index] == element:
                    temp_correct += 1
                elif max(probability_ens_first[index]) < max(probability_ens_second[index]) and prediction_ens_second[index] == element:
                    temp_correct += 1
            accuracy_ens = temp_correct / len(test_Y)
            accuracy_ensemble.append(accuracy_ens)
            if accuracy_ens > best_accuracy_ensemble:
                best_accuracy_ensemble = accuracy_ens
                best_scaler_ensemble = scaler
                best_classifier_ensemble = (model_ensemble_first,model_ensemble_second)

        average_regular = sum(accuracy_regular) / len(accuracy_regular)
        average_ensemble = sum(accuracy_ensemble) / len(accuracy_ensemble)

        test_accuracy = 0

        if average_regular >= average_ensemble:
            test_X = [row[:-1] for row in dataset[split:]]
            test_Y = [row[-1] for row in dataset[split:]]
            test_X = best_scaler_regular.transform(test_X)
            test_accuracy = accuracy_score(test_Y, best_classifier_regular.predict(test_X))
        else:
            test_X = [row[:-1] for row in dataset[split:]]
            test_Y = [row[-1] for row in dataset[split:]]
            test_X = best_scaler_ensemble.transform(test_X)

            model_first, model_second = best_classifier_ensemble
            prediction_first = model_first.predict(test_X)
            prediction_second = model_second.predict(test_X)
            probability_first = model_first.predict_proba(test_X)
            probability_second = model_second.predict_proba(test_X)
            temp_correct = 0
            for index,element in enumerate(test_Y):
                if max(probability_first[index]) >= max(probability_second[index]) and prediction_first[index] == element:
                    temp_correct += 1
                elif max(probability_first[index]) < max(probability_second[index]) and prediction_second[index] == element:
                    temp_correct += 1
            test_accuracy = temp_correct / len(test_Y)


        print (f'Average accuracy of a regular neural network: {average_regular}')
        print (f'Average accuracy of a ensemble neural network: {average_ensemble}')
        print (f'Accuracy on the testing set: {test_accuracy}')

        if int(inputs) == 1:
            temp_1 = 0.03156146179401993
            temp_2 = 0.2364341085271318
            temp_3 = 0.15625
            if temp_1 == average_regular and temp_2 == average_ensemble and temp_3 == test_accuracy:
                print(f"Correct solution for input {inputs}")
            else:
                print(f"Incorrect solution for input {inputs}")
            print()
            print()
        elif int(inputs) == 5:
            temp_1 = 0.2364341085271318
            temp_2 = 0.2364341085271318
            temp_3 = 0.15625
            if temp_1 == average_regular and temp_2 == average_ensemble and temp_3 == test_accuracy:
                print(f"Correct solution for input {inputs}")
            else:
                print(f"Incorrect solution for input {inputs}")
            print()
            print()
        elif int(inputs) == 10:
            temp_1 = 0.007936507936507936
            temp_2 = 0.2364341085271318
            temp_3 = 0.15625
            if temp_1 == average_regular and temp_2 == average_ensemble and temp_3 == test_accuracy:
                print(f"Correct solution for input {inputs}")
            else:
                print(f"Incorrect solution for input {inputs}")
            print()
            print()
        elif int(inputs) == 20:
            temp_1 = 0.34699150978220744
            temp_2 = 0.2364341085271318
            temp_3 = 0.375
            if temp_1 == average_regular and temp_2 == average_ensemble and temp_3 == test_accuracy:
                print(f"Correct solution for input {inputs}")
            else:
                print(f"Incorrect solution for input {inputs}")
            print()
            print()
        elif int(inputs) == 30:
            temp_1 = 0.13381321520856404
            temp_2 = 0.2364341085271318
            temp_3 = 0.15625
            if temp_1 == average_regular and temp_2 == average_ensemble and temp_3 == test_accuracy:
                print(f"Correct solution for input {inputs}")
            else:
                print(f"Incorrect solution for input {inputs}")
            print()
            print()