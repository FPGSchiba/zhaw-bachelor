test_list = [1, 2, 3, 4, 5]

print([i * 2 for i in test_list if i % 2 == 0])

data = {
    'key': 'value',
    1: 'test',
    'int': 2
}

for key, value in data.items():
    print(f'{key}: {value}')
