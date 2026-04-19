import numpy as np

# 1. Створення одновимірного масиву з 200 випадкових чисел (-100..100)
arr = np.random.randint(-100, 101, 200)

print("Початковий масив:")
print(arr)

# 2. Маска для додатних чисел
positive_mask = arr > 0
positive_numbers = arr[positive_mask]

print("\nДодатні числа:")
print(positive_numbers)

# 3. Замінюємо всі від’ємні значення на 0
arr[arr < 0] = 0

print("\nМасив після заміни від’ємних значень на 0:")
print(arr)

# 4. Обчислення середнього значення
average = np.mean(arr)

print("\nСереднє значення масиву:", average)
