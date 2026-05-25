def read_dataset_from_csv(filepath):
    dataset = []
    with open(filepath, 'r') as file:
        for row in file:
            temp = []
            t = 0
            for char in row:
                if char:
                    temp.append(char)
            dataset.append(temp)
    return dataset

dataset = read_dataset_from_csv('zad2_dataset.csv')
print(dataset)