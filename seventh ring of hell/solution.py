from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

from data.dataFirst import dataset
import warnings
warnings.filterwarnings("ignore")
if __name__ == '__main__':
    N = int(input())
    M = int(input())

    new_dataset = []
    for row in dataset:
        new_row = []
        temp_row = row[:-1]
        max_element = max(temp_row)
        mean = sum(temp_row)/len(temp_row)
        length = len(temp_row)
        random_first = (sum((element * mean) for element in temp_row)) / length
        temp_up = 0
        for i in range(1,length):
            temp_up += abs(temp_row[i] - temp_row[i-1])
        random_second = temp_up / mean
        new_row.append(max_element)
        new_row.append(mean)
        new_row.append(length)
        new_row.append(random_first)
        new_row.append(random_second)
        new_row.append(row[-1])
        new_dataset.append(new_row)

    split = int(len(new_dataset) * 0.7)

    train_X = [row[:-1] for row in new_dataset[:split]]
    train_Y = [row[-1] for row in new_dataset[:split]]

    test_X = [row[:-1] for row in new_dataset[split:]]
    test_Y = [row[-1] for row in new_dataset[split:]]

    model_tree = DecisionTreeClassifier(max_depth=M, random_state=0)
    model_MLP = MLPClassifier(hidden_layer_sizes=(N,), random_state=0)
    model_tree.fit(train_X, train_Y)
    model_MLP.fit(train_X, train_Y)

    accuracy_max_tree = accuracy_score(test_Y, model_tree.predict(test_X))
    accuracy_max_MLP = accuracy_score(test_Y, model_MLP.predict(test_X))

    accuracies_tree = []
    accuracies_MLP = []

    accuracies_tree.append(accuracy_max_tree)
    accuracies_MLP.append(accuracy_max_MLP)

    index_max_tree = 0
    index_max_MLP = 0

    dataset_max_tree = new_dataset [:]
    dataset_max_MLP = new_dataset [:]

    for i in range (5):
        removed_element_dataset = []
        for row in new_dataset:
            new_row = [element for index,element in enumerate(row) if index != i]
            removed_element_dataset.append(new_row)
        train_X = [row[:-1] for row in removed_element_dataset[:split]]
        train_Y = [row[-1] for row in removed_element_dataset[:split]]

        test_X = [row[:-1] for row in removed_element_dataset[split:]]
        test_Y = [row[-1] for row in removed_element_dataset[split:]]

        model_tree.fit(train_X, train_Y)
        model_MLP.fit(train_X, train_Y)

        accuracy_tree_temp = accuracy_score(test_Y, model_tree.predict(test_X))
        accuracy_MLP_temp = accuracy_score(test_Y, model_MLP.predict(test_X))

        accuracies_tree.append(accuracy_tree_temp)
        accuracies_MLP.append(accuracy_MLP_temp)

        if accuracy_tree_temp > accuracy_max_tree:
            accuracy_max_tree = accuracy_tree_temp
            index_max_tree = i + 1
            dataset_max_tree = removed_element_dataset[:]

        if accuracy_MLP_temp > accuracy_max_MLP:
            accuracy_max_MLP = accuracy_MLP_temp
            index_max_MLP = i + 1
            dataset_max_MLP = removed_element_dataset[:]


    names = ['with all the features','with the first feature removed','with the second feature removed','with the third feature removed','with the fourth feature removed','with the fifth feature removed']

    scaler = StandardScaler()

    train_X = [row[:-1] for row in dataset_max_tree[:split]]
    train_Y = [row[-1] for row in dataset_max_tree[:split]]
    test_X = [row[:-1] for row in dataset_max_tree[split:]]
    test_Y = [row[-1] for row in dataset_max_tree[split:]]

    train_X = scaler.fit_transform(train_X)
    test_X = scaler.transform(test_X)

    model_tree.fit(train_X, train_Y)
    scaled_accuracy_tree = accuracy_score(test_Y, model_tree.predict(test_X))

    train_X = [row[:-1] for row in dataset_max_MLP[:split]]
    train_Y = [row[-1] for row in dataset_max_MLP[:split]]
    test_X = [row[:-1] for row in dataset_max_MLP[split:]]
    test_Y = [row[-1] for row in dataset_max_MLP[split:]]

    train_X = scaler.fit_transform(train_X)
    test_X = scaler.transform(test_X)

    model_MLP.fit(train_X, train_Y)
    scaled_accuracy_MLP = accuracy_score(test_Y, model_MLP.predict(test_X))

    print(f"Best tree accuracy was {max(accuracies_tree)} {names[index_max_tree]}")
    print(f"Best MLP accuracy was {max(accuracies_MLP)} {names[index_max_MLP]}")
    print(f"Scaled tree accuracy was {scaled_accuracy_tree}")
    print(f"Scaled MLP accuracy was {scaled_accuracy_MLP}")