import pygame
import time
import random

global sections

def isSectionClear(xstart, ypos, offset):
    global sections
    rightGround = None
    for ground in sections:
      if ground.getY(xstart + offset):
        rightGround = ground
        break
    if rightGround:
      # we found boundry
      return rightGround.ypos >= ypos
    return True

class DrawObject(object):
    def draw(self, gameDisplay):
        if self.xpos + self.width > 0 and self.xpos < 800:
            pygame.draw.rect(gameDisplay, self.color, [self.xpos,self.ypos,self.width,self.height])

class Bullet(DrawObject):
    yVelocity = 50
    def __init__(self, character):
        self.xpos = character.xpos
        self.ypos = character.ypos
        self.color = (255,255,0) # yellow
        self.width = 10
        self.height = 4

    def drawPosition(self, gameDisplay):
        for cnt in range(-25,25,5):
           if not isSectionClear(self.xpos, self.ypos+self.height, cnt):
               return True
        if self.xpos <= 810:
            self.draw(gameDisplay)
            self.xpos += 50
            return False
        else:
            # remove the bullet
            return True

class MainCharacter(DrawObject):
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.width = 20
        self.height = 30
        self.color = (0,0,0) # black
        self.xChange = 0
        self.yChange = 0
        self.velocity = 0

    def updateEvents(self, groundLimit):
        self.velocity += 2
        self.ypos += self.velocity
        if self.ypos >= groundLimit-30:
            self.ypos = groundLimit-30
            self.velocity = 0

        mypos = self.getXPosition()
        if self.xChange > 0:
            mypos += self.width/2
        if isSectionClear(mypos, mainChar.ypos + self.height, self.xChange):
            self.xpos += self.xChange
            if self.xpos <= 0:
                self.xpos = 0

    def getXPosition(self):
        return self.xpos + self.width/2

class LandScape(DrawObject):

    def __init__(self, color, ypos, width, previous=None):
        self.offset = 0
        if previous:
            self.offset = previous.xpos + previous.width
        self.xpos = self.offset
        self.ypos = ypos
        self.color = color
        self.width = width
        self.height = 800 - ypos

    def update(self, xpos):
       self.xpos = xpos + self.offset

    def getY(self, pos):
        #pos = character.getXPosition()
        if self.xpos <= pos and self.xpos + self.width >= pos:
            return self.ypos
        else:
            return None
        

sections = []
pygame.init()
screenWidth = screenHeight = 800
gameDisplay = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Personal Project")

blue = (0,0,255)
sky = (72,209,204)
white = (255,255,255)
black = (0,0,0)
brightGreen = (0,255,0)
grass = (0,100,0)
yellow = (255,255,0)
firebrick = (174,34,34)

gameExit = False
mainChar = MainCharacter(200,0)

groundx = 0
# color, xstart, ystart, width, height

# here we build the landscape!!
numSections = 400
myground = 500
lastsec = LandScape(grass,myground,30)
for cnt in range(numSections):
    sections.append(lastsec)
    myground = random.randint(myground - 20, myground + 20)
    lastsec = LandScape(grass,myground,30,lastsec)

bullets = []

vel = 0

clock = pygame.time.Clock()
groundLimit = 500

while not gameExit:
    for event in pygame.event.get():
        
        print event
        
        if event.type == pygame.QUIT:
            gameExit = True
        
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mainChar.xChange = -10
                elif event.key == pygame.K_RIGHT:
                    mainChar.xChange = 10
                elif event.key == pygame.K_UP:
                    mainChar.yChange = 0
                elif event.key == pygame.K_DOWN:
                    mainChar.yChange = 10
                elif event.key == pygame.K_SPACE:
                    bullets.append(Bullet(mainChar))

        if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    mainChar.xChange = 0
                elif event.key == pygame.K_RIGHT:
                    mainChar.xChange = 0
                elif event.key == pygame.K_UP:
                    mainChar.yChange = 0 
                elif event.key == pygame.K_DOWN:
                    mainChar.yChange = 0
                elif event.key == pygame.K_SPACE:
                    None        

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP and \
        mainChar.ypos >= groundLimit - 31:
            mainChar.velocity = -18
            
    gameDisplay.fill(sky)
    for ground in sections:
      lim = ground.getY(mainChar.getXPosition())
      if lim:
        groundLimit = lim
    for ground in sections:
      ground.update(groundx)
      ground.draw(gameDisplay)    
    
    mainChar.updateEvents(groundLimit)

    mainChar.draw(gameDisplay)
    # print "Main Char is", str(mainChar.xpos), "and GroundX is", str(groundx)
    
    if mainChar.xpos >= 350:
        groundx -= 10
        mainChar.xpos -= 10
    if mainChar.xpos <= 35:
        groundx += 10
        if groundx >= 0:
            groundx = 0
        mainChar.xpos += 10

    bullet_remove = None
    for mybullet in bullets:
        remove = mybullet.drawPosition(gameDisplay)
        if remove:
            bullets.remove(mybullet)
    pygame.display.update()

    clock.tick(15)

pygame.quit()
quit()
