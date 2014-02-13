import random
letters = ["A", "B", "C", "D"]
random.shuffle(letters)
numbers = [1, 2, 3, 4]
dic = dict(zip(numbers, letters))
print(dic)
