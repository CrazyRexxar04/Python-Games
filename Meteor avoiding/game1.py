#----------------------------------------------------------------------------------------------------------------------------------------------------# importing

import pygame
import time
import random

pygame.init() #initiate pygame

#----------------------------------------------------------------------------------------------------------------------------------------------------#  variable setting

display_width = 800 #display parameters
display_height = 600 

black = (0,0,0) #basic colours
white = (255, 255, 255)
red = (255, 0, 0)
blue = (50, 0, 255)
green =(0, 255, 0)

gameDisplay = pygame.display.set_mode((display_width,display_height)) #setup the screen and clock
pygame.display.set_caption('Walkthrough')
clock = pygame.time.Clock()

car_width = 40
car_height = 70

meteor_width = 80
meteor_height = 80

carImg = pygame.image.load('space_ship.png') #calls the image
carImg = pygame.transform.scale(carImg, (car_width, car_height))

meteorImg = pygame.image.load('meteor.png')
meteorImg = pygame.transform.scale(meteorImg, (meteor_width, meteor_height))

backgroundImg = pygame.image.load('space-background.jpg')
backgroundImg = pygame.transform.scale(backgroundImg, (display_width, display_height))

#----------------------------------------------------------------------------------------------------------------------------------------------------# game function setting

def car(x,y): #blit the image at x,y parameters
    gameDisplay.blit(carImg, (x,y))

def crash(): #crash function - restart method
    message_display('You Crashed')

def text_objects(text, font):
    textSurface = font.render(text, True, red) #defines the text colour and font
    return textSurface, textSurface.get_rect()

def message_display(text):
    text_type = pygame.font.Font('freesansbold.ttf', 115)# Text setting
    TextSurf, TextRect = text_objects(text, text_type)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop()

def things(thingx, thingy):
    gameDisplay.blit(meteorImg, (thingx, thingy))

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Points: ' + str(count), True, green)
    gameDisplay.blit(text, (0,0))

def bonus(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render('Bonus: ' + str(count), True, blue)
    gameDisplay.blit(text, (600,0))
    

#----------------------------------------------------------------------------------------------------------------------------------------------------#  main game function

def game_loop():

    x = (display_width * 0.45) #starting point for the image
    y = (display_height * 0.8)

    x_change = 0 # sets the change to 0 at the start

    thing_startx = random.randrange(0, display_width) # defines the position of thing
    thing_starty = -600
    thing_speed = 3

    dodged = 0
    bonusNum = 1

    gameExit = False #have not crashed

    while not gameExit:

        for event in pygame.event.get(): #checks to see if the user exits
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN: # key down loop
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP: #key up loop
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change # changes the x possition based on the x_change loop before

        gameDisplay.blit(backgroundImg, (0,0))# draws the background

        things(thing_startx, thing_starty) #draws and adds speed to the meteor
        thing_starty += thing_speed
        
        car(x,y)

        things_dodged(dodged)

        bonus(bonusNum)


        if x > display_width - car_width or x < 0: # handels crashing into the wall
            crash()

        if thing_starty > display_height: # meteor collision and restart
            thing_starty = 0 - meteor_height
            thing_startx = random.randrange(0, display_width)
            dodged += 1
            if thing_speed > 7:
                dodged += 4
                bonusNum = 5
                thing_speed += 0.5
            elif thing_speed > 10:
                dodged += 9
                thing_speed += 0.2
                bonusNum = 10
            else:
                thing_speed += 1
                bonusNum = 1

        

        if y < thing_starty+meteor_height: # collision logic loop
            #print('y crossover') - re-comment to check collison

            if x > thing_startx and x < thing_startx + meteor_width or x + car_width > thing_startx and x + car_width < thing_startx + meteor_width:
                #print('x crossover') - re-comment to check collison
                crash()

        pygame.display.update() #updates and clocks the framerate
        clock.tick(60)

#----------------------------------------------------------------------------------------------------------------------------------------------------# after game loop

game_loop()

pygame.quit() #correctly quits pygame at the end
quit()
