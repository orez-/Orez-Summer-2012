import pygame
import random
import math
from tile import *

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
colors = {"black":(  0,  0,  0),\
          "white":(255,255,255),\
          "blue": (  0,  0,255),\
          "green":(  0,128,  0),\
          "red":  (255,  0,  0),\
          "brown":(128, 64,  0)}

pi=3.141592653

# Set the height and width of the screen
size=(1000,500)
screen=pygame.display.set_mode(size)

cx = 0  # player loc
cy = 0
dx = 0  # display loc
dy = 0
pygame.display.set_caption("Orez Tactics")

#Loop until the user clicks the close button.
done=False
clock = pygame.time.Clock()

board = Board((20,20,30), (40,20,10), size)
screen.fill(colors["black"])
board.setDisplayPosition(cx,cy)

moving = 0  # direction of movement (0 is stationary, 1-4 are directions)
step = .125 # be careful with this number and floating point rounding....

while not done:
    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            #print event.key
            if not moving:
                if event.key == pygame.K_w:
                    if cy != board.chunk[1]-1:
                        moving = 1
                        board.setDisplayPosition(cx,cy)
                elif event.key == pygame.K_a:
                    if cx != board.chunk[0]-1:
                        moving = 2
                        board.setDisplayPosition(cx,cy)
                elif event.key == pygame.K_s:
                    if cy != 0:
                        moving = 3
                        board.setDisplayPosition(cx,cy)
                elif event.key == pygame.K_d:
                    if cx != 0:
                        moving = 4
                        board.setDisplayPosition(cx,cy)
                elif event.key == pygame.K_SPACE:
                    board.selectSquare(cx,cy)
    
    if moving:
        if moving==1:
            cy += step
        if moving==2:
            cx += step
        if moving==3:
            cy -= step
        if moving==4:
            cx -= step
        board.setDisplayPosition(cx,cy)
        if cx==math.floor(cx) and cy==math.floor(cy):
            moving = 0
    
    screen.fill(colors["black"])
    board.printToScreen(screen)
    pygame.draw.polygon(screen,(255,255,255),[(int((size[0]/2)-20), int((size[1]/2)+5)),\
                                              (int(size[0]/2),      int((size[1]/2)-5)),\
                                              (int((size[0]/2)+20), int((size[1]/2)+5)),\
                                              (int(size[0]/2),      int((size[1]/2)+15))], 3)
    pygame.display.flip()

# Be IDLE friendly
pygame.quit ()
