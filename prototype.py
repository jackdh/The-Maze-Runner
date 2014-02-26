import pygame
import json
import random

"""
Global constants
"""

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (124, 252, 0)
RED = (255, 0, 0)
# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.RESIZABLE)

# Set the title of the window
pygame.display.set_caption('Prototype')


# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls. """

    # Set speed vector
    change_x = 0
    change_y = 0

    # Constructor function
    def __init__(self, start_y, start_x):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.reset_position_y = start_y
        self.reset_position_x = start_x

        # Set height, width
        self.image = pygame.Surface([15, 15])
        self.image.fill(RED)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = self.reset_position_y
        self.rect.x = self.reset_position_x

        self.deaths = 0
        self.answered = 0

    def changespeed(self, x, y):
        """ Change the speed of the player. """
        self.change_x += x
        self.change_y += y

    def update(self):
        """ Update the player position. """
        # Move left/right
        self.rect.x += self.change_x

        # Did this update cause us to hit a wall?
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            self.deaths += 1
            self.rect.y = self.reset_position_y
            self.rect.x = self.reset_position_x

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            self.deaths += 1
            self.rect.y = self.reset_position_y
            self.rect.x = self.reset_position_x

        if pygame.sprite.spritecollide(self, self.end_zone_answer, False):
            self.answered += 1
            self.rect.y = self.reset_position_y
            self.rect.x = self.reset_position_x
            global current_room_no

            if current_room_no == 2:
                current_room_no = 0
            else:
                current_room_no += 1

            global current_question_no
            current_question_no += 1

    def death_counter(self):
        font = pygame.font.Font(None, 20)
        text = font.render("deaths: "+str(self.deaths), 1, WHITE)
        textpos = (500, 110)
        screen.blit(text, textpos)

    def questions_answered(self):
        font = pygame.font.Font(None, 20)
        text = font.render("Answered: "+str(self.answered), 1, WHITE)
        textpos = (500, 90)
        screen.blit(text, textpos)

class Wall(pygame.sprite.Sprite):
    """ Wall the player can run into. """

    def __init__(self, x, y, width, height, color):
        """ Constructor for the wall that the player can run into.
        :rtype : object
        """
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        # Make a blue wall, of the size specified in the parameters
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class EndZone(pygame.sprite.Sprite):

    def __init__(self, x, y, letter):
        """ Constructor for the Endzone """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        if letter == "a":
            self.image = pygame.image.load("a.jpg").convert()
        elif letter == "b":
            self.image = pygame.image.load("b.jpg").convert()
        elif letter == "c":
            self.image = pygame.image.load("c.jpg").convert()
        elif letter == "d":
            self.image = pygame.image.load("d.jpg").convert()

        # Make a green box

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Question:
    def __init__(self, number):

        self.answer_letter = ""

        self.question_list = []
        self.number = number

        with open('questions.json') as f:
            questions = json.load(f)
            q = questions[self.number]  # 0 For getting first question answer set
            self.question_text = q["question"]
            self.answer_text = q["answer"]
            self.fake_one = q["fake1"]
            self.fake_two = q["fake2"]
            self.fake_three = q["fake3"]
        f.close()

        self.position = {"a": (30, 50), "b": (30, 70), "c": (30, 90), "d": (30, 110)}

        self.list_fake_questions = [self.fake_one, self.fake_two, self.fake_three]

        self.font = pygame.font.Font(None, 20)

        self.position_question()

        self.letters = ["a", "b", "c", "d"]
        self.make_answer()
        for i in range(3):
            self.make_fake(i)

    def position_text(self, letter, render_text):
        text = self.font.render(letter.upper()+": " + render_text, 1, WHITE)
        textpos = text.get_rect()
        textpos.topleft = (self.position[letter])
        self.question_list.append([text, textpos])

    def position_question(self):
        text = self.font.render(self.question_text, 1, WHITE)
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = 30
        self.question_list.append([text, textpos])

    def print_question(self):
        for i in self.question_list:
            screen.blit(i[0], i[1])

    def make_answer(self):
        letter = self.letters.pop(random.randint(0, len(self.letters)-1))  # Get a random letter and remove it
        self.position_text(letter, self.answer_text)  # Give it to position text to store in the list
        self.answer_letter = letter

    def get_answer(self):
        print(self.answer_letter)
        return self.answer_letter

    def make_fake(self, number):
        letter = self.letters.pop(random.randint(0, len(self.letters)-1))
        self.position_text(letter, self.list_fake_questions[number])

    def get_question_number(self):
        return self.number



class Map():
    wall_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()

        four_sides = [(0, 150, 10, 600, BLUE),
                      (10, 150, 580, 10, BLUE),
                      (0, 590, 600, 10, BLUE),
                      (590, 150, 10, 600, BLUE)
                      ]

        for item in four_sides:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        self.letters = ["a", "b", "c", "d"]



        self.answer_letter = questions[0].get_answer()  # Currently working here
        self.letters.pop(self.letters.index(self.answer_letter))
        random.shuffle(self.letters)

        self.fake1 = self.letters.pop()
        self.fake2 = self.letters.pop()
        self.fake3 = self.letters.pop()

    def make_endzones(self, possible_endzones):
        random.shuffle(possible_endzones)
        one = possible_endzones.pop()
        two = possible_endzones.pop()
        three = possible_endzones.pop()
        return [(one[0], one[1], self.fake1), (two[0], two[1], self.fake2), (three[0], three[1], self.fake3)]


class Map1(Map):
    def __init__(self):
        Map.__init__(self)

        walls_to_make = [(10, 250, 450, 10, WHITE),
                         (150, 350, 10, 175, WHITE),
                         (300, 350, 10, 175, WHITE),
                         (450, 350, 10, 175, WHITE),
                         (600, 350, 10, 175, WHITE),
                         ]

        for item in walls_to_make:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        possible_endzones = [(70, 450), (220, 450), (370, 450), (520, 450)] #edit this

        EndZone_to_make = self.make_endzones(possible_endzones)
        four = possible_endzones.pop()

        for i in range(len(EndZone_to_make)):
            end_zone = EndZone(*EndZone_to_make[i])
            self.wall_list.add(end_zone)

        answer_zone = EndZone(four[0], four[1], self.answer_letter)

        end_zone_answer.add(answer_zone)


class Map2(Map):
    def __init__(self):
        Map.__init__(self)

        walls_to_make = [(10, 250, 450, 10, WHITE)]

        for item in walls_to_make:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        possible_endzones = [(70, 450), (220, 450), (370, 450), (520, 450)] #edit this

        EndZone_to_make = self.make_endzones(possible_endzones)
        four = possible_endzones.pop()

        for i in range(len(EndZone_to_make)):
            end_zone = EndZone(*EndZone_to_make[i])
            self.wall_list.add(end_zone)

        answer_zone = EndZone(four[0], four[1], self.answer_letter)

        end_zone_answer.add(answer_zone)

class Map3(Map):
    def __init__(self):
        Map.__init__(self)

        walls_to_make = [(450, 350, 10, 175, WHITE),
                         (600, 350, 10, 175, WHITE),
                         ]

        for item in walls_to_make:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

        possible_endzones = [(70, 450), (220, 450), (370, 450), (520, 450)]  # edit this

        EndZone_to_make = self.make_endzones(possible_endzones)
        four = possible_endzones.pop()

        for i in range(len(EndZone_to_make)):
            end_zone = EndZone(*EndZone_to_make[i])
            self.wall_list.add(end_zone)

        answer_zone = EndZone(four[0], four[1], self.answer_letter)

        end_zone_answer.add(answer_zone)




# Call this function so the Py game library can initialize itself

# List to hold all the sprites

all_sprite_list = pygame.sprite.Group()

player_list = pygame.sprite.Group()

end_zone_list = pygame.sprite.Group()

end_zone_answer = pygame.sprite.Group()

global questions
questions = []

question = Question(0)
questions.append(question)

question = Question(1)
questions.append(question)

question = Question(2)
questions.append(question)

question = Question(3)
questions.append(question)

current_question_no = 0


rooms = []

room = Map1()
rooms.append(room)

room = Map2()
rooms.append(room)

room = Map3()
rooms.append(room)


current_room_no = 0
current_room = rooms[current_room_no]

# Create the player paddle object
player = Player(200, 70)
player.walls = current_room.wall_list
player.end_zone_answer = end_zone_answer
player_list.add(player)

clock = pygame.time.Clock()

speed = 7

done = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.changespeed(-speed, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(speed, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, -speed)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, speed)
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player.changespeed(speed, 0)
            elif event.key == pygame.K_RIGHT:
                player.changespeed(-speed, 0)
            elif event.key == pygame.K_UP:
                player.changespeed(0, speed)
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, -speed)

    screen.fill(BLACK)

    questions[current_question_no].print_question()

    player.death_counter()

    player.questions_answered()

    player_list.update()

    player_list.draw(screen)



    end_zone_answer.draw(screen)

    rooms[current_room_no].wall_list.update()
    rooms[current_room_no].wall_list.draw(screen)
    player.walls = rooms[current_room_no].wall_list

    pygame.display.flip()

    pygame.display.update()

    clock.tick(60)

pygame.quit()

