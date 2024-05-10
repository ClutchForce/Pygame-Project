import pygame
import levelMap as lm
# import bossfightMain form the Joel folder
import button
import shop

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

#YOOFSUFS MENU CODE

#game variables
pauseGame = False
currentState = "main"

#define fonts
font = pygame.font.SysFont("arialblack", 40)

#define colours
txtCLR = (255, 255, 255)


#load button images
resumeIMG = pygame.image.load('Yoosuf/button_resume.png').convert_alpha()
optionsIMG = pygame.image.load("Yoosuf/button_options.png").convert_alpha()
quitIMG = pygame.image.load("Yoosuf/button_quit.png").convert_alpha()
audioIMG = pygame.image.load('Yoosuf/button_audio.png').convert_alpha()
keysIMG = pygame.image.load('Yoosuf/button_keys.png').convert_alpha()
backIMG = pygame.image.load('Yoosuf/button_back.png').convert_alpha()
shopIMG = pygame.image.load('Yoosuf/store_icon.png').convert_alpha()

#create button instances
resumeBTN = button.Button(304, 125, resumeIMG, 1)
optionsBTN = button.Button(297, 250, optionsIMG, 1)
quitBTN = button.Button(336, 375, quitIMG, 1)
audioBTN = button.Button(225, 200, audioIMG, 1)
keysBTN = button.Button(246, 325, keysIMG, 1)
backBTN = button.Button(332, 450, backIMG, 1)
shopBTN = button.Button(200, 200, shopIMG, 0.5)

def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def menu():
    #game loop
    running = True
    while running:
        screen.fill((52, 78, 91))

        #checks if game is paused
        if pauseGame == True:
            #check menu state
            if currentState == "main":
            #draw pause screen buttons
                if resumeBTN.draw(screen):
                    pauseGame = False
                if optionsBTN.draw(screen):
                    currentState = "options"
                if quitBTN.draw(screen):
                    running = False
            #check if the options menu is open
            if currentState == "options":
            #draw the different options buttons
                if audioBTN.draw(screen):
                    currentState = "main"
                if keysBTN.draw(screen):
                    print("Change Key Bindings")
                if backBTN.draw(screen):
                    currentState = "main"
                if shopBTN.draw(screen):
                    print("Shop")
        else:
            draw_text("Press ESC to pause", font, txtCLR, 160, 250)

        #event handler
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        pygame.display.update()



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
                pauseGame = True
                menu()
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
