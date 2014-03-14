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

#class for functions related to the spritesheet
class SpriteSheet():
    #points to sprite sheet image
    sprite_sheet=None

    def __init__(self, file_name):
        #file name is passed as a parameter
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def getImage( self, x, y, width, height):
        #x and y is image start coordinate, width and length defines size of the sprite
        image = pygame.Surface([width, length]).convert()

        image.blit(self.sprite_sheet,(0,0),(x,y,width, length))

        image.set_colorkey(constants.BLACK)

        return image

# This class represents the bar at the bottom that the player controls
class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player controls. """

    # Set speed vector
    change_x = 0
    change_y = 0

    #list to hold images for moving left/right
    walking_frames_l = []
    walking_frames_r =[]
    walking_frames_u = []
    walking_frames_d=[]
    #direction sprites facing
    direction = "R"

    # Constructor function
    def __init__(self, start_y, start_x):
        # Call the parent's constructor
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = SpriteSheet("sprite_sheet")

        #load sprites to right list
        image= sprite_sheet.getImage(35,0,28,30)
        self.walking_frames_r.append(image)
        image= sprite_sheet.getImage(35,30,25,40)
        self.walking_frames_r.append(image)
        image= sprite_sheet.getImage(35,60,28,30)
        self.walking_frames_r.append(image)

        #load sprites to left list

        image= sprite_sheet.getImage(88,1,25,30)
        self.walking_frames_l.append(image)
        image= sprite_sheet.getImage(88,30,25,30)
        self.walking_frames_l.append(image)
        image= sprite_sheet.getImage(88,60,25,30)
        self.walking_frames_l.append(image)

        #load sprites to up list
        image= sprite_sheet.getImage(56,2,30,30)
        self.walking_frames_u.append(image)
        image= sprite_sheet.getImage(56,30,28,30)
        self.walking_frames_u.append(image)
        image= sprite_sheet.getImage(56,60,28,30)
        self.walking_frames_u.append(image)

        #load sprites to down list
        image= sprite_sheet.getImage(0,0,28,30)
        self.walking_frames_d.append(image)
        image= sprite_sheet.getImage(0,35,28,30)
        self.walking_frames_d.append(image)
        image= sprite_sheet.getImage(0,65,28,30)
        self.walking_frames_d.append(image)

        #default image
        self.image=self.walking_frames_r[0]
               
        self.reset_position_y = start_y
        self.reset_position_x = start_x

        # Set height, width
        #self.image = pygame.Surface([15, 15])
        #self.image.fill(RED)
        
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

    def go_left(self):
        self.change_x=-6
        self.direction = "L"
        
    def go_right(self):
        self.change_x=6
        self.direction = "R"
        
    def go_up(self):
        self.change_y =6
        self.direction="U"

    def go_down(self):
        self.change_y=-6
        self.direction="D"  

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

    def __init__(self, x, y, letter, question):
        pygame.sprite.Sprite.__init__(self)
        """ Constructor for the Endzone """
        self.letter = letter
        # Call the parent's constructor
        if self.letter == "a":
            self.image = pygame.image.load("a.jpg").convert()
        elif self.letter == "b":
            self.image = pygame.image.load("b.jpg").convert()
        elif self.letter == "c":
            self.image = pygame.image.load("c.jpg").convert()
        elif self.letter == "d":
            self.image = pygame.image.load("d.jpg").convert()

        # Make a green box

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.type = question
    def draw(self, screen):
        screen.blit(self.image, self.rect)

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
        return self.answer_letter

    def make_fake(self, number):
        letter = self.letters.pop(random.randint(0, len(self.letters)-1))
        self.position_text(letter, self.list_fake_questions[number])

    def get_question_number(self):
        return self.number



class Map():
    wall_list = None
    def __init__(self, walls, endzones, question):
        self.wall_list = pygame.sprite.Group()
        self.walls_to_make = walls[:] # Split the walls up
        self.endzones = endzones[:]   # Split the endzones up
        self.question = question      # Question Number

        four_sides = [(0, 150, 10, 600, BLUE),
                      (10, 150, 580, 10, BLUE),    #The standard walls
                      (0, 590, 600, 10, BLUE),
                      (590, 150, 10, 600, BLUE)
                      ]
        for item in four_sides:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])   # Make standard walls
            self.wall_list.add(wall)

        for item in self.walls_to_make:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])   # Make specific walls
            self.wall_list.add(wall)

        self.letters = ["a", "b", "c", "d"]

        self.answer_letter = questions[self.question].get_answer()  # Get the questions

        self.letters.pop(self.letters.index(self.answer_letter))  # remove the answer question from list of letters

        random.shuffle(self.letters)  # shuffle the remaining

        self.fake1 = self.letters.pop()
        self.fake2 = self.letters.pop()  # Get fakes
        self.fake3 = self.letters.pop()

        self.possible_endzones = self.endzones  # Endzones for this map
        random.shuffle(self.possible_endzones)  # shuffle them
        one = self.possible_endzones.pop()
        two = self.possible_endzones.pop()
        three = self.possible_endzones.pop()
        four = self.possible_endzones.pop()
        EndZone_to_make = [(one[0], one[1], self.fake1, self.question), (two[0], two[1], self.fake2, self.question), (three[0], three[1], self.fake3, self.question)]

        answer_zone = EndZone(four[0], four[1], self.answer_letter, self.question)
        end_zone_answer.add(answer_zone) # here it's adding them all to it. Not one at a time.

        for i in range(len(EndZone_to_make)):
            end_zone = EndZone(*EndZone_to_make[i])
            self.wall_list.add(end_zone)
        # currently made all the maps into one. Now add a question variable.
        # Then create the loop to make the endzone
        # Make sure they are displaying
#Map1
map1_walls = [(10, 250, 450, 10, WHITE),
              (150, 350, 10, 175, WHITE),
              (300, 350, 10, 175, WHITE),
              (450, 350, 10, 175, WHITE),
              (600, 350, 10, 175, WHITE),
              ]

map1_endzones = [(70, 250), (220, 250), (370, 250), (520, 250)]

#Map2
map2_walls = [(10, 250, 450, 10, WHITE)]

map2_endzones = [(70, 450), (220, 450), (370, 450), (520, 450)]
#Map3
map3_walls = [(150, 350, 10, 175, WHITE),
              (300, 350, 10, 175, WHITE),
              (450, 350, 10, 175, WHITE),
              (600, 350, 10, 175, WHITE),
              ]

map3_endzones = [(70, 550), (220, 550), (370, 550), (520, 550)]

# Call this function so the Py game library can initialize itself

# List to hold all the sprites

all_sprite_list = pygame.sprite.Group()

player_list = pygame.sprite.Group()

end_zone_list = pygame.sprite.Group()

end_zone_answer = pygame.sprite.Group()
current_end_zone_answer = pygame.sprite.Group()

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

question = Question(4)
questions.append(question)

current_question_no = 0


rooms = []
rooms.append(Map(map1_walls, map1_endzones, 0))
rooms.append(Map(map2_walls, map2_endzones, 1))
rooms.append(Map(map3_walls, map3_endzones, 2))

rooms.append(Map(map1_walls, map1_endzones, 3))

current_room_no = 0
current_room = rooms[current_room_no]

#set current endzone to answer


# Create the player paddle object
player = Player(200, 70)
player.walls = current_room.wall_list

for i in end_zone_answer:
    if i.type == current_question_no:
        current_end_zone_answer.add(i)

player.end_zone_answer = current_end_zone_answer
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
                player.go_left()
            elif event.key == pygame.K_RIGHT:
                player.changespeed(speed, 0)
                player.go_right()
            elif event.key == pygame.K_UP:
                player.changespeed(0, -speed)
                player.go_up()
            elif event.key == pygame.K_DOWN:
                player.changespeed(0, speed)
                player.go_down()
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

    rooms[current_room_no].wall_list.update()
    

    for i in end_zone_answer:
        if i.type == current_question_no:
            i.draw(screen)
            current_end_zone_answer.empty()
            current_end_zone_answer.add(i)
            player.end_zone_answer = current_end_zone_answer

    player.walls = rooms[current_room_no].wall_list

    pygame.display.flip()

    pygame.display.update()

    clock.tick(60)

pygame.quit()
