import pygame
from pygame import mixer
from bossFighter import Fighter

mixer.init()
pygame.init()

#creating the game window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #creates the game window
pygame.display.set_caption("Boss Fight") #sets the title of the game window

#set the framerate
clock = pygame.time.Clock()
FPS = 60

#define colourss
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)


#define game variables
intro_counter = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0] #score[0] = player score, score[1] = enemy score
round_over = False
ROUND_OVER_COOLDOWN = 2000
ALT_COOLDOWN = 10

PLAYER_WINS = False
BOSS_WINS = False

#degfine fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72,56]
WARRIOT_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112,107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load sounds
pygame.mixer.music.load("Joel/Assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("Joel/Assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("Joel/Assets/audio/magic.wav")
magic_fx.set_volume(0.75)


#load images

#background
bg_image = pygame.image.load("Joel\Assets\Images\Background\Background.jpg").convert_alpha()

#load sprite sheets
warrior_sheet = pygame.image.load("Joel\Assets\Images\warrior\Sprites\warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("Joel\Assets\Images\wizard\Sprites\wizard.png").convert_alpha()

#load victory images
victory_image = pygame.image.load("Joel\Assets\Images\icons\Victory.png").convert_alpha()


#defining number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]


#difine font
count_font = pygame.font.Font("Joel/Assets/fonts/turok.ttf", 120)
score_font = pygame.font.Font("Joel/Assets/fonts/turok.ttf", 30)
score_font_highlight = pygame.font.Font("Joel/Assets/fonts/turok.ttf", 34)

#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for draw the backgroundqswsww
def draw_bg():
    scaled_bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)) #scales the background image to the size of the game window
    screen.blit(scaled_bg_image, (0, 0))   #draws the background image at the top left corner of the screen

#drawing the health bars
def draw_health_bars(health_og,health, x, y):
    pygame.draw.rect(screen, WHITE, (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, BLACK, (x, y, 400, 30))
    ratio = health / health_og

    if ratio > 0.75:
        health_color = GREEN
    elif ratio > 0.50:
        health_color = YELLOW
    elif ratio > 0.25:
        health_color = ORANGE
    else:
        health_color = RED

    pygame.draw.rect(screen, health_color, (x, y, 400*ratio, 30))

def draw_alt_cooldown_bar(x, y, cooldown, cooldown_og):
    pygame.draw.rect(screen, WHITE, (x-2, y-2, 404, 34))
    pygame.draw.rect(screen, BLACK, (x, y, 400, 30))
    c = cooldown_og - cooldown
    ratio = c / cooldown_og
    filled_width = int (ratio*400)
    pygame.draw.rect(screen, BLUE, (x, y,filled_width, 30))

#creating two instances of the Fighters
figter_1 = Fighter(1,200, 310, False, WARRIOT_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx,"Joel\Assets\Images\icons\Victory.png",ALT_COOLDOWN)
figter_2 = Fighter(2, 1700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx,"Joel\Assets\Images\icons\Victory.png",0)

#game loop
running = True

while running:

    clock.tick(FPS)

    #draw the background
    draw_bg()   

    #draw the health bars
    draw_health_bars(100,figter_1.health, 20, 20)
    draw_health_bars(100,figter_2.health, SCREEN_WIDTH - 420, 20)
    draw_text("Player: "+str(score[0]), score_font, WHITE, 440, 20)
    draw_text(str(score[1])+" :Boss", score_font, WHITE, SCREEN_WIDTH - 520, 20)
    draw_alt_cooldown_bar(20, 70, figter_1.alt_cooldown, ALT_COOLDOWN)

    #update the intro counter
    if intro_counter <=0:
         #move the fighters
        figter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, figter_2,round_over)
        figter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, figter_1,round_over)
    else:
        #display the intro counter
        draw_text(str(intro_counter), count_font, RED, SCREEN_WIDTH/2 , SCREEN_HEIGHT/3 ) 
        #update counter
        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_counter -= 1
            last_count_update = pygame.time.get_ticks()
            

   

    #update the fighters
    figter_1.update()
    figter_2.update()

    #draw the fighters
    figter_1.draw(screen)
    figter_2.draw(screen)


    if round_over == False:
        if figter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_timer = pygame.time.get_ticks()
        elif figter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_timer = pygame.time.get_ticks()
    else:
        #display victory image
        if pygame.time.get_ticks() - round_over_timer >= ROUND_OVER_COOLDOWN:
            round_over = False
            intro_counter = 3
            figter_1 = Fighter(1,200, 310, False, WARRIOT_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx,"Joel\Assets\Images\icons\Victory.png",ALT_COOLDOWN)
            figter_2 = Fighter(2, 1700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx,"Joel\Assets\Images\icons\Victory.png",0)

    ########################################################
    ########################################################
    ########################################################
    ####### have to finish after everything is done ########
    ########################################################
    ########################################################
    ########################################################

    if score[0] == 2 and score[1] <=1 or score[1] == 2 and score[0] <=1:
        round_over = True
        if score[0] > score[1]:
            PLAYER_WINS = True
        else:
            BOSS_WINS = True

    if PLAYER_WINS == True:
        # cover the screen with a black rectangle
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        # display the victory image
        screen.blit(victory_image, (SCREEN_WIDTH/2 - victory_image.get_width()/2, SCREEN_HEIGHT/2 - victory_image.get_height()/2))
    if BOSS_WINS == True:
        # cover the screen with a black rectangle
        pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        # display the defeat image
        # screen.blit(defeat_image, (SCREEN_WIDTH/2 - defeat_image.get_width()/2, SCREEN_HEIGHT/2 - defeat_image.get_height()/2))
        # display the defeat text
        draw_text("You have been defeated", score_font, WHITE, SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/2 - 100)



    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    #update the display
    pygame.display.update()


#exit the game
pygame.quit()