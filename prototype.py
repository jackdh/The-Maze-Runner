bif = "bg1.jpg"
mif = "dot.png"

import pygame, sys
from pygame.locals import *

#Globals
BLACK    = (   0,   0,   0) 
WHITE    = ( 255, 255, 255) 
BLUE     = (   0,   0, 255)

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600


class Player(




pygame.init()
screen=pygame.display.set_mode((640,587),0,32)

background = pygame.image.load(bif).convert()   #Convert it so pygame can use them
mouse_c = pygame.image.load(mif).convert_alpha()
x,y=0,0
movex, movey=0,0
while True:
    for event in pygame.event.get():#Go through every event in 
        if event.type ==  QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background, (0,0))  #Blit means COPY 
    x,y = pygame.mouse.get_pos()
    
    x -= mouse_c.get_width()/2
    y -= mouse_c.get_height()/2
            
    
    screen.blit(mouse_c,(x,y))
    pygame.display.update()

