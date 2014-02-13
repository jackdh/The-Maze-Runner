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


# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls. """

    # Set speed vector
    change_x = 0
    change_y = 0
    walls = None

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

    def __init__(self, x, y,):
        """ Constructor for the Endzone """

        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([15, 15])
        self.image.fill(GREEN)

        # Make a green box

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


def question(number):
    question_area = pygame.Surface(screen.get_size())
    question_area.fill((0,0,0))

    with open('questions.json') as f:
        questions = json.load(f)
        q = questions[number]  # 0 For getting first question answer set
        question_text = q["question"]
        answer_text = q["answer"]
        fake_one = q["fake1"]
        fake_two = q["fake2"]
        fake_three = q["fake3"]
    f.close()

    """ This is used to position the questions """
    position = {"A": ["A: ", (30, 60)], "B": ["B: ", (30, 120)], "C": ["C: ", (300, 60)], "D": ["D: ", (300, 120)]}

    def position_text(letter, render_text):
        text = font.render(position[letter][0]+render_text, 1, WHITE)
        textpos = text.get_rect()
        textpos.topleft = (position[letter][1])
        screen.blit(text, textpos)

    def position_question():
        text = font.render(question_text, 1, WHITE)
        textpos = text.get_rect()
        textpos.centerx = screen.get_rect().centerx
        textpos.centery = 30
        screen.blit(text, textpos)

    font = pygame.font.Font(None, 20)
    #Questions

    position_question()
    letters = ["A", "B", "C", "D"]
    random.shuffle(letters)
    numbers = [1, 2, 3, 4]
    get_letter = dict(zip(numbers, letters))

    position_text(get_letter[1], answer_text)

    position_text(get_letter[2], fake_one)

    position_text(get_letter[3], fake_two)

    position_text(get_letter[4], fake_three)



### WORKING HERE ON MAKING THE QUESTIONS RANDOMISE.




# Call this function so the Py game library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.RESIZABLE)

# Set the title of the window
pygame.display.set_caption('Prototype')

# List to hold all the sprites

all_sprite_list = pygame.sprite.Group()

wall_list = pygame.sprite.Group()

end_zone_list = pygame.sprite.Group()

def make_walls(list):

    for i in range(len(list)):
        wall = Wall(*list[i])
        wall_list.add(wall)
        all_sprite_list.add(wall)

walls_to_make = [(10, 300, 700, 10, WHITE),
                 (150, 450, 10, 340, WHITE),
                 (300, 450, 10, 340, WHITE),
                 (450, 450, 10, 340, WHITE),
                 (600, 450, 10, 340, WHITE),
                 ]

four_sides = [(0, 200, 10, 600, BLUE),
              (10, 200, 790, 10, BLUE),
              (0, 790, 800, 10, BLUE),
              (790, 200, 10, 600, BLUE)
              ]

make_walls(walls_to_make)
make_walls(four_sides)


EndZone_to_make = [(70, 720), (220, 720), (370, 720)]
for i in range(len(EndZone_to_make)):
    end_zone = EndZone(*EndZone_to_make[i])
    wall_list.add(end_zone)
    all_sprite_list.add(end_zone)

# Create the player paddle object
player = Player(250, 50)
player.walls = wall_list
all_sprite_list.add(player)


clock = pygame.time.Clock()

done = False

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

    all_sprite_list.update()

    screen.fill(BLACK)

    question(2)

    all_sprite_list.draw(screen)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
