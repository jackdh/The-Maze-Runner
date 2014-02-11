import json

with open('questions.json') as f:
    questions = json.load(f)
    question_number= questions[2] # 0 For getting first question answer set
    print(question_number["question"])
f.close()

#Prints the correct question