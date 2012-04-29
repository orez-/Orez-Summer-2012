import pygame
import random
import math
import tile

# Initialize the game engine
pygame.init()

# Define the colors we will use in RGB format
black = (  0,  0,  0)
white = (255,255,255)
blue =  (  0,  0,255)
green = (  0,128,  0)
red =   (255,  0,  0)
brown = (128, 64,  0)

pi=3.141592653

# Set the height and width of the screen
size=(400,500)
screen=pygame.display.set_mode(size)

cx = 0
cy = 0
dx = 0
dy = 0
pygame.display.set_caption("Orez Tactics")

#Loop until the user clicks the close button.
done=False
clock = pygame.time.Clock()

sqH = 20
sqW = sqH*2
sqD = 10

xChunk = 10
yChunk = 10
zChunk = 10

boW = (xChunk+yChunk)*sqW/2
boH = (xChunk+yChunk)*sqH/2
boD = sqD*zChunk

def setPos():
    global dx, dy
    dx = (cx-cy)*sqW/2+(size[0]-boW)/2
    dy = (cx+cy)*sqH/2+board[cx][cy]*sqD+(size[1]/2-(boH+boD))+18

def drawTile(surface, rx, ry, rz, mx, texture=green):
    step = 255/max(xChunk,yChunk)
    base  = (rx*step/2,ry*step/4,50)
    top = (rx*step,50,ry*step)
    #base = brown
    #top  = green
    
    surf = pygame.Surface((sqW,rz*sqD+sqH))
    surf.fill((255,0,255))
    surf.set_colorkey((255,0,255))  # magenta is see-through
    
    pygame.draw.polygon(surf, base, [(0,sqH/2),(sqW/2,0),(sqW,sqH/2),(sqW,sqD*rz+sqH/2),(0,sqD*rz+sqH/2)])
    pygame.draw.polygon(surf, top,  [(0,sqD*rz+sqH/2),(sqW/2,sqD*rz),(sqW,sqD*rz+sqH/2),(sqW/2,sqD*rz+sqH)])
    surface.blit(surf, ((mx-1)*sqW/2-((rx-ry)*sqW)/2, ((rx+ry-2)*sqH)/2))

screen.fill(black)
moveableBoard = pygame.Surface((boW,boH+boD))
#moveableBoard.fill(white)
board = [[min(zChunk,math.floor(((y+1)**2+(x+1)**2)**.5)) for y in xrange(yChunk)] for x in xrange(xChunk)]
#board = [[min(zChunk,x+y+1) for y in xrange(yChunk)] for x in xrange(xChunk)]
#board = [[0 for y in xrange(yChunk)] for x in xrange(xChunk)]

for x in range(xChunk-1,-1,-1):
    for y in range(yChunk-1,-1,-1):
        drawTile(moveableBoard, x+1,y+1,board[x][y], xChunk)
moveableBoard = pygame.transform.flip(moveableBoard, False, True)
setPos()

while done==False:
    # This limits the while loop to a max of 60 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(60)
    
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            #print event.key
            if event.key == pygame.K_w:
                cy = min(yChunk-1,cy+1)
                setPos()
            elif event.key == pygame.K_a:
                cx = min(xChunk-1,cx+1)
                setPos()
            elif event.key == pygame.K_s:
                cy = max(0,cy-1)
                setPos()
            elif event.key == pygame.K_d:
                cx = max(0,cx-1)
                setPos()
    
    screen.fill(black)
    screen.blit(moveableBoard,(dx,dy))
    pygame.draw.circle(screen,white,(size[0]/2,size[1]/2),10)
    pygame.display.flip()

# Be IDLE friendly
pygame.quit ()
