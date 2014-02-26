import random

position = {"a": ["A: ", (30, 50)], "b": ["B: ", (30, 70)], "c": ["C: ", (30, 90)], "d": ["D: ", (30, 110)]}

question_text = "question"
answer_text = "answer"
fake_one = "fake1"
fake_two = "fake2"
fake_three = "fake3"

list_questions = [answer_text, fake_one, fake_two, fake_three]

letters = ["A", "B", "C", "D"]
random.shuffle(letters)


get_letter = dict(zip(list_questions, letters))  # Make the dictionary

#print(position["a"][1])

print(letters.pop())
print(letters)