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

class platform(entity):
    height = None
    width = None
    image = None

#Jump Function
#def jump():
    
    
#move items
def move(a):
    a.x += a.xSpeed
    
#Update items drawn on screen
def update():
    screen.fill((0,0,0))
    pygame.draw.rect(screen, (150, 150, 150), platform.rectangle)
    #pygame.draw.rect(screen, (255, 255, 255), mainChar.rectangle)
    #pygame.draw.rect(screen, (150, 150, 150), enemy.rectangle)
    screen.blit(floor.image,(floor.x,floor.y))
    #screen.blit(platform.image,(platform.x,platform.y))
    screen.blit(enemy.image,(enemy.x,enemy.y))
    screen.blit(mainChar.image,(mainChar.x,mainChar.y))
    pygame.display.flip()
    clock.tick(55)

#create rectangle for bounds check
def getBounds(rect):
    left = rect.x
    top = rect.y
    right = rect.image.get_width() 
    bottom = rect.image.get_height()
    rect.rectangle = (left,top,right,bottom)

#check for collision (rect one collides with rect2)
def collisionCheck(rect1, rect2):
    #collision on bottom of rect1
    if (rect1.y + rect1.height >= rect2.y) and (rect1.x + rect1.width > rect2.x) and (rect1.x < rect2.x + rect2.width):
        rect1.y = (rect2.y - rect1.height) + 1
        rect1.status = "run"
        rect1.collide = True
        rect1.collideSide = "bottom"
        rect1.itemHit = rect2.name
        
    #collision on right of rect1
    if (rect1.x + rect1.width > rect2.x - 2) and (rect1.x + rect1.width < rect2.x + 2) and (rect1.y + rect1.height >= rect2.y):
        rect1.collide = True
        rect1.collideSide = "right"
        rect1.status = "run"

    #collision on left of rect1
    if rect1.x < (rect2.x + rect2.width + 2) and rect1.x > (rect2.x + rect2.width - 2) and rect1.y + rect1.height >= rect2.y:
        rect1.collide = True
        rect1.collideSide = "left"
        rect1.status = "run"

    #if rect1.collideSide == "right" and rect1.y < platform.y:
        #rect1.status = "run"
        #rect1.y = (rect2.y - rect1.height) + 1
        
    
pygame.init()

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
mainChar.collide = False
mainChar.name = "main"

#Floor
floor = person()
floor.image = pygame.image.load("floor.jpg").convert()
floor.x = 0
floor.y = height - 3
floor.height = floor.image.get_height()
floor.width = floor.image.get_width()
floor.name = "floor"

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

#Platform
platform = platform()
platform.image = pygame.image.load("platform.jpg").convert()
platform.x = 850
platform.y = 480
platform.height = platform.image.get_height()
platform.width = platform.image.get_width()
platform.rectangle = (0,0,0,0)
getBounds(platform)
pygame.draw.rect(screen, (150, 150, 150), platform.rectangle)
platform.name = "platform"



#Sword Image
swordImages = ['sword1.png','sword2.png','sword3.png']

#Running and jumping
fall = None
jump = 0
direction = "right"

#First Draw 
screen.blit(mainChar.image,(mainChar.x,mainChar.y))
mainChar.image.set_colorkey((255,255,255))
screen.blit(floor.image,(floor.x,floor.y))

#Main Game Loop
while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        #Events for pushing key down
        if event.type == KEYDOWN:
            if pygame.key.get_pressed()[K_RIGHT]:
                mainChar.status = "run"
                mainChar.image = pygame.image.load("right.png").convert()
                mainChar.image.set_colorkey((255,255,255))
                mainChar.direction = "right"
                mainChar.xSpeed = 3
                if mainChar.collide == False:
                    mainChar.status = "fall"
                
            if pygame.key.get_pressed()[K_LEFT]:
                mainChar.status = "run"
                mainChar.image = pygame.image.load("left.png").convert()
                mainChar.image.set_colorkey((255,255,255))
                mainChar.direction = "left"
                mainChar.xSpeed = -3
                if mainChar.collide == False:
                    mainChar.status = "fall"
                
            if pygame.key.get_pressed()[K_UP] and mainChar.status != "jump" and mainChar.status != "fall":
                mainChar.status = "jump"

        #Event for key releases
        if event.type == KEYUP and mainChar.status != "jump" and mainChar.collide == True:
            mainChar.status = "stopped"

    #If not jumping or collided always fall (Gravity)
    if mainChar.collide == False and mainChar.status != "jump":
        mainChar.status = "fall"
        
    #Stopped status
    if mainChar.status == "stopped":
        mainChar.xSpeed = 0
        mainChar.yspeed = 0
        move(mainChar)
        
    #Running while key is held down
    if mainChar.status == "run":
        move(mainChar)

    #Jump
    if mainChar.status == "jump" and mainChar.direction == "right":
        jump += 1
        mainChar.y -= 8
        mainChar.x += 2
        if mainChar.y > height:
            mainChar.y = height
        if mainChar.y < 0:
            mainChar.y = mainChar.image.get_height()
        if mainChar.x < 0:
            mainChar.x = 0
        if mainChar.x > width - 75:
            mainChar.x = width - 75

        if jump == 20:
            mainChar.status = "fall"
            
    if mainChar.status == "jump" and mainChar.direction == "left":
        mainChar.y -= 8
        mainChar.x -= 2
        jump += 1
        if mainChar.y > height:
            mainChar.y = height
        if mainChar.y < 0:
            mainChar.y = mainChar.image.get_height()
        if mainChar.x < 0:
            mainChar.x = 0
        if mainChar.x > width - 75:
            mainChar.x = width - 75

        if jump == 20:
            mainChar.status = "fall"
            

    if mainChar.status == "fall":
        if mainChar.direction == "right":
            jump = 0
            mainChar.y +=20
            mainChar.x += 3
        if mainChar.direction == "left":
            jump = 0
            mainChar.y +=20
            mainChar.x -=3

    #if mainChar.status != "jump" and mainChar.collide == False:
        #mainChar.status = "fall"

    #Collision Actions
    #if mainChar.collide == True and mainChar.itemHit == "floor":
        #mainChar.y = floor.y - mainChar.y
        #mainChar.status = "run"
    #Check collision
    collisionCheck(mainChar,floor)
    collisionCheck(mainChar,enemy)
    collisionCheck(mainChar,platform)

    getBounds(mainChar)
    getBounds(floor)
    getBounds(enemy)
    getBounds(platform)

    #Update Images On Screen
    update()
        
    


    
    


