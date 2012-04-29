import pygame
import math
import random
from unit import *

class Tile:
    top_img = pygame.transform.flip(pygame.image.load("img/top.png"), False, True)
    sqS = ()
    def __init__(self,cx,cy,cz):
        self.selected = False
        self.x = cx
        self.y = cy
        self.z = cz
        self.unit = (Unit("ninja") if random.randint(0,20)<4 else None)
    def drawTile(self, surface, mx, rx=None, ry=None, rz=None):
        if Tile.sqS == ():
            raise Exception("You must define sqS in Tile before using any Tiles")
        rx = self.x if rx==None else rx
        ry = self.y if ry==None else ry
        rz = self.z if rz==None else rz
        
        sqW = Tile.sqS[0]
        sqH = Tile.sqS[1]
        sqD = Tile.sqS[2]
        
        # vvv COLORS!!! vvv
        step = 255/max(20,20)   # size of board
        base  = (rx*step/2,ry*step/4,50)
        top = (rx*step,50,ry*step)
        #base = (128,64,0)
        #top  = (0,128,0)
        
        size = (sqW,rz*sqD+sqH)
        surf = pygame.Surface(size)
        surf.fill((255,0,255))
        surf.set_colorkey((255,0,255))  # magenta is see-through
        
        pygame.draw.polygon(surf, base, [(0,sqH/2),(sqW/2,0),(sqW,sqH/2),(sqW,sqD*rz+sqH/2),(0,sqD*rz+sqH/2)])
        surf.blit(Tile.top_img, (0,sqD*rz+1))
        if self.selected:
            pygame.draw.polygon(surf, top,  [(0,sqD*rz+sqH/2),(sqW/2,sqD*rz),(sqW,sqD*rz+sqH/2),(sqW/2,sqD*rz+sqH)])
        surfloc = ((mx-1)*sqW/2-((rx-ry)*sqW)/2, ((rx+ry-2)*sqH)/2)
        surface.blit(surf, surfloc)
        if self.unit != None:
            self.unit.display(surface,(int(surfloc[0]+(size[0]-25)/2),int(surfloc[1]+size[1]-12)))
        
class Board:
    def __init__(self,chunk_size,square_size,screen_size):
        self.assertType(chunk_size,  tuple, 3, name="chunk_size")
        self.assertType(square_size, tuple, 3, name="square_size")
        self.assertType(screen_size, tuple, 2, name="screen_size")
        self.sqS = square_size
        self.chunk = chunk_size
        self.ssize = screen_size
        Tile.sqS = self.sqS
        self.board_size = ((self.chunk[0]+self.chunk[1])*self.sqS[0]/2,\
                           (self.chunk[0]+self.chunk[1])*self.sqS[1]/2,\
                           (self.chunk[2]*self.sqS[2]))
        self.board_data = [[Tile(x+1,y+1,min(self.chunk[2],math.floor(((y+1)**2+(x+1)**2)**.5)))\
                                for y in xrange(self.chunk[1])]\
                                    for x in xrange(self.chunk[0])]
        self.board_image = pygame.Surface((self.board_size[0], self.board_size[1]+self.board_size[2]))
        self.dx = 0
        self.dy = 0
        self.buildDisplay()

    # set the display position based on player coordinates. accepts fractional values
    # for one coordinate (never both), for a frame in a transition
    def setDisplayPosition(self,cx,cy):
        if cx==math.floor(cx) and cy==math.floor(cy):   # you are ON a square
            zOffset = self.board_data[int(cx)][int(cy)].z
        else:                                           # you are between squares
            fx = cx-math.floor(cx)
            fy = cy-math.floor(cy)
            if fx and fy:
                raise TypeError("You may only move the display in one cardinal direction at a time.")
            zOffset = self.board_data[int(math.floor(cx))][int(math.floor(cy))].z*(1-max(fx,fy))    # linearly average of the two
            zOffset+= self.board_data[ int(math.ceil(cx))][ int(math.ceil(cy))].z*(  max(fx,fy))
        
        self.dx = (cx-cy)*self.sqS[0]/2+(self.ssize[0]-self.board_size[0])/2
        self.dy = (cx+cy)*self.sqS[1]/2+zOffset*self.sqS[2]+(self.ssize[1]/2-(self.board_size[1]+self.board_size[2]))+18
    
    def selectSquare(self, cx, cy):
        cx = int(cx)
        cy = int(cy)
        self.board_data[int(cx)][int(cy)].selected ^= True
        self.buildDisplay()
    
    def buildDisplay(self):
        self.board_image.fill((0,0,0))
        for x in range(self.chunk[0]-1,-1,-1):
            for y in range(self.chunk[1]-1,-1,-1):
                self.board_data[x][y].drawTile(self.board_image, self.chunk[0])
        self.board_image = pygame.transform.flip(self.board_image, False, True)
        
    def printToScreen(self,screen):
        screen.blit(self.board_image,(self.dx,self.dy))
        
    def assertType(self, checkitem, checkType, size=-1, **args):
        name = ""
        if "name" in args:
            name = " for "+args["name"]
        if not (isinstance(checkitem,checkType) and (size==-1 or len(checkitem)==size)):
            size = str(size)
            if isinstance(checkitem,checkType):
                raise TypeError("You must pass a tuple of size "+size+name+" (passed tuple of size "+str(len(checkitem))+")")
            raise TypeError("You must pass a tuple"+("" if size=="-1" else " of size "+size)+name+" (passed "+str(type(checkitem))+")")
