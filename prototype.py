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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

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
            self.rect.y = self.reset_position_y
            self.rect.x = self.reset_position_x

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:
            self.rect.y = self.reset_position_y
            self.rect.x = self.reset_position_x

        block_win_list = pygame.sprite.spritecollide(self, self.end_zone_answer, False)
        for block in block_win_list:
            current_room_no = 1


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

    def __init__(self, x, y, color):
        """ Constructor for the Endzone """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([15, 15])
        self.image.fill(color)

        # Make a green box

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


class Question:
    def __init__(self, number):
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

        self.position = {"A": ["A: ", (30, 60)], "B": ["B: ", (30, 120)], "C": ["C: ", (300, 60)], "D": ["D: ", (300, 120)]}

        self.font = pygame.font.Font(None, 20)

        self.position_question()

        self.letters = ["A", "B", "C", "D"]
        random.shuffle(self.letters)  # This makes shuffles the letters so the answers will land on separate questions
        self.numbers = [1, 2, 3, 4]  # These are used to make the dictionary and will link with the randomised letters
        self.get_letter = dict(zip(self.numbers, self.letters))  # Make the dictionary

        self.position_text(self.get_letter[1], self.answer_text)  # Print answer to the screen

        self.position_text(self.get_letter[2], self.fake_one)

        self.position_text(self.get_letter[3], self.fake_two)

        self.position_text(self.get_letter[4], self.fake_three)

    def position_text(self, letter, render_text):
        text = self.font.render(self.position[letter][0]+render_text, 1, WHITE)
        textpos = text.get_rect()
        textpos.topleft = (self.position[letter][1])
        self.question_list.append([text, textpos])

    def position_question(self):
        text = self.font.render(self.question_text, 1, WHITE)
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = 30
        self.question_list.append([text, textpos])

    def print_question(self):
        for i in self.question_list:
            screen.blit(i[0],i[1])


class Map():
    wall_list = None

    def __init__(self):
        self.wall_list = pygame.sprite.Group()

        four_sides = [(0, 200, 10, 600, BLUE),
              (10, 200, 790, 10, BLUE),
              (0, 790, 800, 10, BLUE),
              (790, 200, 10, 600, BLUE)
              ]

        for item in four_sides:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Map1(Map):
    def __init__(self):
        Map.__init__(self)

        walls_to_make = [(10, 300, 700, 10, WHITE),
             (150, 450, 10, 340, WHITE),
             (300, 450, 10, 340, WHITE),
             (450, 450, 10, 340, WHITE),
             (600, 450, 10, 340, WHITE),
             ]

        for item in walls_to_make:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


class Map2(Map):
    def __init__(self):
        Map.__init__(self)

        walls_to_make = [(10, 300, 700, 10, WHITE),
                        (150, 450, 10, 340, WHITE),
                        ]

        for item in walls_to_make:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)


def main():
    # Call this function so the Py game library can initialize itself

    # List to hold all the sprites

    all_sprite_list = pygame.sprite.Group()

    end_zone_list = pygame.sprite.Group()

    end_zone_answer = pygame.sprite.Group()

    rooms = []
    room = Map1()
    rooms.append(room)
    room = Map2()
    rooms.append(room)

    current_room_no = 0
    current_room = rooms[current_room_no]

    current_question_no = 0
    current_question = Question(current_question_no)

    EndZone_to_make = [(70, 720, GREEN), (220, 720, GREEN), (370, 720, GREEN)]
    for i in range(len(EndZone_to_make)):
        end_zone = EndZone(*EndZone_to_make[i])
        current_room.wall_list.add(end_zone)
        all_sprite_list.add(end_zone)

    EndZone_to_make_answer = EndZone(520, 720, WHITE)

    all_sprite_list.add(EndZone_to_make_answer)
    end_zone_answer.add(EndZone_to_make_answer)

    # Create the player paddle object
    player = Player(250, 50)
    player.walls = current_room.wall_list
    player.end_zone_answer = end_zone_answer
    all_sprite_list.add(player)



    clock = pygame.time.Clock()

    done = False
    x = 1
    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changespeed(-3, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(3, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, -3)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, 3)
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changespeed(3, 0)
                elif event.key == pygame.K_RIGHT:
                    player.changespeed(-3, 0)
                elif event.key == pygame.K_UP:
                    player.changespeed(0, 3)
                elif event.key == pygame.K_DOWN:
                    player.changespeed(0, -3)

        screen.fill(BLACK)

        current_question.print_question()

        all_sprite_list.update()

        all_sprite_list.draw(screen)

        current_room.wall_list.draw(screen)

        pygame.display.flip()

        pygame.display.update()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()