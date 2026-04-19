import numpy as np

arr = np.random.randint(-100, 101, 200)

print("Початковий масив:")
print(arr)

positive_numbers = arr[arr > 0]

print("\nДодатні числа:")
print(positive_numbers)

arr[arr < 0] = 0

print("\nМасив після заміни від’ємних значень на 0:")
print(arr)

average = np.mean(arr)

print("\nСереднє значення масиву:", average)