import pygame

class QuestionOne():

    def __init__(self):
        self.question = "What is 2*2?"
        self.answer = "4"
        self.fake_one = "12"
        self.fake_two = "35"
        self.fake_three = "I dunno 5 maybe?"

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def get_fake_one(self):
        return self.fake_one

    def get_fake_two(self):
        return self.fake_two

    def get_fake_three(self):
        return self.fake_three

class QuestionTwo():

    def __init__(self):
        self.question = "What is five * five?"
        self.answer = "Sqiggles"
        self.fake_one = "25"
        self.fake_two = "Omegle?"
        self.fake_three = "I dunno 5 maybe?"

    def get_question(self):
        return self.question

    def get_answer(self):
        return self.answer

    def get_fake_one(self):
        return self.fake_one

    def get_fake_two(self):
        return self.fake_two

    def get_fake_three(self):
        return self.fake_three
