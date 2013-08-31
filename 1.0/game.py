import pygame
import sys
import os
from pygame.locals import *
from sys import exit

class entity:
    visible = False
    name = None
    x = None
    y = None
    point1 = []
    point2 = []
    point3 = []
    point4 = []
    xSpeed = None
    ySpeed = None
    rectangle = None

class person(entity):
    image = None
    status = None
    direction = None
    collide = None
    collideSide = None
    height = None
    width = None
    itemHit = None
    pickupBut = False
    holdingBox = False
    currentHold = False

class platform(entity):
    height = None
    width = None
    image = None

class box(entity):
    image = None
    height = None
    width = None
    pickedUp = False
    xSpeed = 0
    ySpeed = 0
    name = None
    collide = None
    status = None
    direction = None

#jump Function
#def jump(a):

def boxCollide(a, speed):
    if a.collide == True:
        a.xSpeed = speed
    if a.collide == False:
        a.xSpeed = 0

def pickupBox(char, box):
    box.y = char.y - box.height - 15
    box.x = ((char.width - box.width)/2) + char.x
    mainChar.holdingBox = True

def throwBox(box,direction):
    if direction == "right":
        box.direction = "right"
        box.xSpeed = 7
        box.ySpeed = 6
    if direction == "left":
        box.direction = "left"
        box.xSpeed = -7
        box.ySpeed = 6

def setCollideFalse(a):
    a.collide = False
    
#move items
def move(a):
    a.x = a.xSpeed + a.x
    if a.xSpeed > 0:
        a.x += 3
    elif a.xSpeed < 0:
        a.x -= 3
    a.y = a.y + a.ySpeed
    
#Update items drawn on screen
def update():
    screen.fill((0,0,0))
    screen.blit(box.image, (box.x,box.y))
    pygame.draw.rect(screen, (150, 150, 150), platform.rectangle)
    screen.blit(floor.image,(floor.x,floor.y))
    screen.blit(platform.image,(platform.x,platform.y))
    screen.blit(enemy.image,(enemy.x,enemy.y))
    screen.blit(mainChar.image,(mainChar.x,mainChar.y))
    pygame.display.flip()
    clock.tick(65)

#create rectangle for bounds check
def getBounds(rect):
    left = rect.x
    top = rect.y
    right = rect.image.get_width() 
    bottom = rect.image.get_height()
    
    rect.point1 = []
    rect.point2 = []
    rect.point3 = []
    rect.point4 = []
    
    rect.rectangle = (left,top,right,bottom)
    rect.point1.append(rect.x)
    rect.point1.append(rect.y)
    rect.point2.append(rect.x + right)
    rect.point2.append(rect.y)
    rect.point3.append(rect.x + right)
    rect.point3.append(rect.y + bottom)
    rect.point4.append(rect.x)
    rect.point4.append(rect.y + bottom)

#check for collision (rect one collides with rect2)
def collisionCheck(rect1, rect2):
    getBounds(rect1)
    getBounds(rect2)

    #Bottom of 1 hits top of 2
    if rect1.point4[1] >= rect2.point1[1] and rect1.point3[0] > rect2.point1[0] and rect1.point4[0] < rect2.point2[0]:
        rect1.y = rect2.y - rect1.height - jumpSpeed
        rect1.collide = True
        
    #Handler for box collisions(box physics)
    if rect1.name == "box":
        #If not colliding with anything stay still
        if rect1.collide == False:
            rect1.status = "fall"

        #rect 1 hits top of something
        if rect1.point3[0] >= rect2.point1[0] and rect1.point1[0] < rect2.point2[0] and rect1.point3[1] >= rect2.point1[1]:
            rect1.collision = "true"
            rect1.status = "stopped"
            rect1.y = rect2.y - rect1.height

        #If rect2 contacts left side of rect1
        if rect2.point3[1] >= (rect1.point1[1] + 5) and (rect2.point3[0] + 5) >= rect1.point1[0] and rect2.point3[0] <= (rect1.point1[0] + 5):
            rect1.collide = True
            print "***************************************************"
            if rect2.pickupBut == False and rect1.collide == True:
                box.direction = "right"
                boxCollide(rect1, 1)
            if rect2.pickupBut == True:
                pickupBox(rect2, rect1)

        #If rect2 touches right side of rect1
        #if  (rect1.point1[1] + 5) <= rect2.point4[1] and (rect2.point1[0] - 5) <= rect1.point2[0] and rect2.point4[0] >= (rect1.point2[0] - 5):
            #rect1.collide = True
            #if rect2.pickupBut == False:
                #box.direction = "left"
                #boxCollide(rect1, -1)
            #if rect2.pickupBut == True:
                #pickupBox(rect2, rect1)
                
        #if rect2.holdingBox == True and rect2.pickupBut == False:
            #rect1.status == "throw"
   
pygame.init()

#lists for moving and non moving
moving = []
nonMoving = []

#clock to limit FPS
clock = pygame.time.Clock()

#Set Screen Data
height = 700
width = 1200

#Start Screen
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Game")

#Create Main Char
mainChar = person()
mainChar.visible = True
mainChar.image = pygame.image.load("right.png").convert()
mainChar.rectangle = (0,0,0,0)
mainChar.x = 10
mainChar.y = (height - mainChar.image.get_height())
mainChar.xSpeed = 0
mainChar.ySpeed = 0
mainChar.status = "stopped"
mainChar.direction = "right"
mainChar.height = mainChar.image.get_height()
mainChar.width = mainChar.image.get_width()
mainChar.name = "mainChar"
moving.append(mainChar.name)

#Floor
floor = person()
floor.image = pygame.image.load("floor.jpg").convert()
floor.x = 0
floor.y = height - 3
floor.height = floor.image.get_height()
floor.width = floor.image.get_width()
floor.name = "floor"
nonMoving.append(floor.name)

#Enemy
enemy = person()
enemyImages = ['e0.jpg','e1.jpg','e2.jpg','e3.jpg','e4.jpg','e5.jpg','e6.jpg','e7.jpg','e7.jpg','e8.jpg','e9.jpg']
enemy.image = pygame.image.load("e0.jpg").convert()
enemy.x = ((width - (enemy.image.get_width())) - 600)
enemy.image.set_colorkey((255,255,255))
enemy.y =height - (enemy.image.get_height())
enemy.width = enemy.image.get_width()
enemy.height = enemy.image.get_height()
enemy.rectangle = (0,0,0,0)
enemy.name = "enemy"
moving.append(enemy.name)

#Platform
platform = platform()
platform.image = pygame.image.load("platform.jpg").convert()
platform.height = platform.image.get_height()
platform.width = platform.image.get_width()
platform.x = 850
platform.y = 580
platform.rectangle = (0,0,0,0)
getBounds(platform)
pygame.draw.rect(screen, (150, 150, 150), platform.rectangle)
platform.name = "platform"
nonMoving.append(platform.name)

#box
box = box()
box.image = pygame.image.load("box.jpg").convert()
box.width = box.image.get_width()
box.height = box.image.get_height()
box.x = 400
box.y = 50
box.xSpeed = 0
box.ySpeed = 0
box.pickedUp = False
box.name = "box"
moving.append(box.name)

#Sword Image
swordImages = ['sword1.png','sword2.png','sword3.png']

#Running and jumping
jump = 0
jumpSpeed = 5
direction = "right"

#First Draw 
screen.blit(mainChar.image,(mainChar.x,mainChar.y))
mainChar.image.set_colorkey((255,255,255))
screen.blit(floor.image,(floor.x,floor.y))
screen.blit(box.image, (box.x,box.y))

#Main Game Loop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        #Events for pushing keys down
        if event.type == KEYDOWN:
            if pygame.key.get_pressed()[K_RIGHT]:
                mainChar.status = "run"
                mainChar.image = pygame.image.load("right.png").convert()
                mainChar.image.set_colorkey((255,255,255))
                mainChar.direction = "right"
                #box.direction = "right"
    
            if pygame.key.get_pressed()[K_LEFT]:
                mainChar.status = "run"
                mainChar.image = pygame.image.load("left.png").convert()
                mainChar.image.set_colorkey((255,255,255))
                mainChar.direction = "left"
                #box.direction = "left"
                
            if pygame.key.get_pressed()[K_UP] and mainChar.collide == True:
                mainChar.status = "jump"

            if pygame.key.get_pressed()[K_SPACE]:
                mainChar.pickupBut = True
            if pygame.key.get_mods() &KMOD_ALT:
                mainChar.pickupBut = False

        #Event for key releases
        if event.type == KEYUP and mainChar.collide == True:
            mainChar.status = "stopped"
            
    #Always apply downward force until opposite reaction is created
    if mainChar.collide == False and mainChar.status != "jump":
        mainChar.status = "fall"

    #If box not touching anything fall
    #if box.collide == False:
        #box.status = "fall"
    

    #Running
    if mainChar.status == "run":
        if mainChar.direction == "right":
            mainChar.xSpeed = 1
            mainChar.ySpeed = 0
        if mainChar.direction == "left":
            mainChar.xSpeed = -1
            mainChar.ySpeed = 0

    #Jump
    if mainChar.status == "jump":
        if jump <= 35 and mainChar.direction == "right":
            mainChar.xSpeed = 1
            mainChar.ySpeed = -6
            jump += 1
        elif jump <= 35 and mainChar.direction == "left":
            mainChar.xSpeed = -1
            mainChar.ySpeed = -6
            jump += 1
        if jump == 35:
            mainChar.status = "fall"
            jump = 0

    #if box.status == "throw":
        #if jump <= 35 and boxr.direction == "right":
            #box.xSpeed = 1
            #box.ySpeed = -6
            #jump += 1
        #elif jump <= 35 and box.direction == "left":
            #box.xSpeed = -1
            #box.ySpeed = -6
            #jump += 1
        #if jump == 15:
            #box.status = "fall"
            #jump = 0
            
    #Falling state, always on unless object.collide = true
    if mainChar.status == "fall":
        if mainChar.direction == "right":
            mainChar.xSpeed = 1
            mainChar.ySpeed = jumpSpeed
        if mainChar.direction == "left":
            mainChar.xSpeed = -1
            mainChar.ySpeed = jumpSpeed

    if box.status == "fall":
        if box.direction == "right":
            box.xSpeed = 1
            box.ySpeed = 4
        if box.direction == "left":
            box.xSpeed = -1
            box.ySpeed = 4
        else:
            box.ySpeed = 4
            box.xSpeed = 0
            
     
    #Stopped status
    if mainChar.status == "stopped":
        mainChar.xSpeed = 0
        mainChar.yspeed = 0

    if box.status == "stopped":
        box.xSpeed = 0
        box.yspeed = 0

    #set collide to false in order to clear variable
    setCollideFalse(mainChar)
    if box.collide == None:
        setCollideFalse(box)

    #if main char is higher than platform check for collision
    if (mainChar.y + mainChar.height) <= platform.y + 5:
        collisionCheck(mainChar,platform)

    if mainChar.y <= box.y + box.height + 5:
        collisionCheck(mainChar,box)

    #Other collision checks
    collisionCheck(mainChar,floor)
    collisionCheck(mainChar,enemy)
    collisionCheck(box,floor)
    #collisionCheck(mainChar,box)

    #If main char is holding box place it above his head and stay with him
    #if mainChar.holdingBox == True:
        #box.y = mainChar.y - box.height - 20
        #box.xSpeed = mainChar.xSpeed
        #mainChar.currentHold = True
        
    if mainChar.pickupBut == False and mainChar.holdingBox == True:
        mainChar.holdongBox = False
        if mainChar.direction == "right":
            throwBox(box,"right")
        if mainChar.direction == "left":
            throwBox(box,"left")
    
    print box.status, box.collide, box.y
    #move images
    move(mainChar)
    move(box)

    #refresh screen
    update()



    
        
    


    
    


