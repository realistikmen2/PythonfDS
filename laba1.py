import random

# 1. Створення двовимірного масиву 3x3 з випадкових чисел (1–100)
matrix = [[random.randint(1, 100) for j in range(3)] for i in range(3)]

print("Початковий масив:")
for row in matrix:
    print(row)

# 2. Сума всіх елементів
total_sum = sum(sum(row) for row in matrix)
print("\nСума всіх елементів:", total_sum)

# 3. Пошук max, min та їх індексів
max_val = matrix[0][0]
min_val = matrix[0][0]
max_index = (0, 0)
min_index = (0, 0)

for i in range(3):
    for j in range(3):
        if matrix[i][j] > max_val:
            max_val = matrix[i][j]
            max_index = (i, j)
        if matrix[i][j] < min_val:
            min_val = matrix[i][j]
            min_index = (i, j)

print("\nМаксимальне значення:", max_val, "Індекс:", max_index)
print("Мінімальне значення:", min_val, "Індекс:", min_index)

# 4. Сортування кожного рядка
for row in matrix:
    row.sort()

print("\nМасив після сортування рядків:")
for row in matrix:
    print(row)
