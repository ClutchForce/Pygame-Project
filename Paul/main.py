import pygame
import levelMap as lm
# import bossfightMain form the Joel folder

import sys
sys.path.insert(1,"Joel")

# from Joel import bossfightMain as bossfightMain

#1 Initialize pygame
pygame.init()

#1p Set the dimensions of the screen
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000

TUTORIAL_LVL = True
LVL_1 = False
LVL_2 = False
LVL_3 = False
LVL_4 = False
BOSS_LVL = False

# #1 Set the color of the border
BORDER_COLOR = (255, 255, 255)

#1 Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")


def render(screen):
    screen.fill((0, 0, 0))
    pygame.display.update()

key = pygame.key.get_pressed()

#1 Run the game loop
running = True
while running:
    #1 Check for events
    for event in pygame.event.get() :

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
             print("Key pressed")
             if event.key == pygame.K_p:
                print("Paused")
                TUTORIAL_LVL = False
                LVL_1 = False
                LVL_2 = False
                LVL_3 = False
                LVL_4 = False
                BOSS_LVL = False
                running = False
        #TODO implement pause menu

    if(TUTORIAL_LVL):
        tutorial = lm.levelTutorial(screen)
        if(tutorial.close):
            running = False
        tutorial.gameLoop()
        TUTORIAL_LVL = False
        LVL_1 = True
        
    if(LVL_1):
        lvl1 = lm.levelOne(screen)
        lvl1.gameLoop()
        LVL_1 = False
        if(lvl1.close):
            running = False
        LVL_2 = True
    if(LVL_2):
        lvl2 = lm.levelTwo(screen)
        lvl2.gameLoop()
        LVL_2 = False
        if(lvl2.close):
            running = False

    ### map 3 and 4 are unable to be used beacuse they are too tall 
    # #TODO find a way to get the camera box to accomodate this 
    #     
    # if(LVL_3):
    #     lvl3 = lm.levelThree(screen)
    #     lvl3.gameLoop()
    #     LVL_3 = False
    #     if(lvl3.close):
    #         running = False
    #     LVL_4 = True
    # if(LVL_4):
    #     lvl4 = lm.levelFour(screen)
    #     lvl4.gameLoop()
    #     LVL_4 = False
    #     BOSS_LVL = True


    ###TODO implement Joels level 
    # if(BOSS_LVL):
    #     lvlBoss = bossfightMain()
    #     lvlBoss.gameLoop()
    #     BOSS_LVL = False

    running = False

    # #3 Draw the screen
    # render(screen)

#1 Quit pygame
pygame.quit()
