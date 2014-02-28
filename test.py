import random


class Map1:
     def __init__(self, number):
         self.number = number

class Map2:
     def __init__(self, number):
         self.number = number

class Map3:
     def __init__(self, number):
         self.number = number

rooms = []

room = Map1(1)
rooms.append(room)
                        # How it is done.
room = Map2(1)
rooms.append(room)

room = Map3(1)
rooms.append(room)

for i in range(1, 4):
    room = Map[i](1)      # How I would like it if possible.
    rooms.append(room)