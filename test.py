from random import randint, sample
from math import factorial

slot_symbols = ["seven", "cherry", "bell", "bar"]
slot_line = ['seven', 'bell', 'bell', 'cherry', 'cherry', 'bar', 'bell', 'cherry', 'bell', 'seven', 'bell', 'bell', 'seven', 'cherry', 'cherry', 'bell', 'bell', 'cherry', 'bar', 'seven', 'bar', 'bar', 'bell', 'bar', 'cherry', 'bell', 'cherry', 'seven', 'seven', 'bar', 'bell', 'bell', 'bell', 'bar', 'seven', 'cherry', 'bar', 'bar', 'bell', 'bell', 'bar', 'cherry', 'bell', 'bell', 'bar', 'bar', 'cherry', 'cherry', 'seven', 'bell', 'bar', 'bar', 'bell', 'bell', 'cherry', 'bell', 'bell', 'bell', 'cherry', 'cherry', 'cherry', 'cherry', 'bar', 'bar', 'bell', 'bar', 'cherry', 'cherry', 'bell', 'bell', 'bell', 'seven', 'cherry', 'bell', 'cherry', 'cherry', 'cherry', 'cherry', 'seven', 'cherry', 'cherry', 'bell', 'seven', 'cherry', 'cherry', 'seven', 'bell', 'bar', 'bell', 'seven', 'bell', 'bar', 'bar', 'seven', 'bell', 'cherry', 'bell', 'seven', 'cherry', 'bell']
slot_generator = {'bell': 35, 'cherry': 30, 'bar': 20, 'seven': 15}
slot_line = sample(slot_line, 100)


b, c, ba, s = 0.32, 0.27, 0.19, 0.22
n = 3
k = 3
binom = factorial(n) / (factorial(k) * factorial(n - k))
for key, value in zip(slot_generator.keys(), slot_generator.values()):
    p = value / 100
    out = binom * (p ** k) * (1 - p) ** (n - k)
    print(key, int((round(100 / (out * 100), 3)) * 1 / 10 * 100))

# def my_map(func, array):
#     out = []
#     for elem in array:
#         out.append(func(elem))
#     print(out)

# my_map(int, ["1", "2", "3"])
print(800 % 14)