import pygame
from pygame import mixer
from bossFighter import Fighter

mixer.init()
pygame.init()

class levelBoss():
    def __init__(self, screen):
        #creating the game window
        self.SCREEN_WIDTH = 1920
        self.SCREEN_HEIGHT = 1000

        self.screen = screen #creates the game window

        #set the framerate
        self.clock = pygame.time.Clock()
        self.FPS = 60

        #define colourss
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.ORANGE = (255, 165, 0)


        #define game variables
        self.intro_counter = 3
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0] #score[0] = player score, score[1] = enemy score
        self.round_over = False
        self.ROUND_OVER_COOLDOWN = 2000
        self.ALT_COOLDOWN = 10

        self.PLAYER_WINS = False
        self.BOSS_WINS = False

        #degfine fighter variables
        self.WARRIOR_SIZE = 162
        self.WARRIOR_SCALE = 4
        self.WARRIOR_OFFSET = [72,56]
        self.WARRIOT_DATA = [self.WARRIOR_SIZE, self.WARRIOR_SCALE, self.WARRIOR_OFFSET]
        self.WIZARD_SIZE = 250
        self.WIZARD_SCALE = 3
        self.WIZARD_OFFSET = [112,107]
        self.WIZARD_DATA = [self.WIZARD_SIZE, self.WIZARD_SCALE, self.WIZARD_OFFSET]

        #load sounds
        pygame.mixer.music.load("Joel/Assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        self.sword_fx = pygame.mixer.Sound("Joel/Assets/audio/sword.wav")
        self.sword_fx.set_volume(0.5)
        self.magic_fx = pygame.mixer.Sound("Joel/Assets/audio/magic.wav")
        self.magic_fx.set_volume(0.75)


        #load images

        #background
        self.bg_image = pygame.image.load("Joel\Assets\Images\Background\Background.jpg").convert_alpha()

        #load sprite sheets
        self.warrior_sheet = pygame.image.load("Joel\Assets\Images\warrior\Sprites\warrior.png").convert_alpha()
        self.wizard_sheet = pygame.image.load("Joel\Assets\Images\wizard\Sprites\wizard.png").convert_alpha()

        #load victory images
        self.victory_image = pygame.image.load("Joel\Assets\Images\icons\Victory.png").convert_alpha()


        #defining number of steps in each animation
        self.WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
        self.WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]


        #difine font
        self.count_font = pygame.font.Font("Joel/Assets/fonts/turok.ttf", 120)
        self.score_font = pygame.font.Font("Joel/Assets/fonts/turok.ttf", 30)
        self.score_font_highlight = pygame.font.Font("Joel/Assets/fonts/turok.ttf", 34)

#function for drawing text
def draw_text(self,text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    self.screen.blit(img, (x, y))

#function for draw the backgroundqswsww
def draw_bg(self):
    scaled_bg_image = pygame.transform.scale(self.bg_image, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)) #scales the background image to the size of the game window
    self.screen.blit(scaled_bg_image, (0, 0))   #draws the background image at the top left corner of the screen

#drawing the health bars
def draw_health_bars(self,health_og,health, x, y):
    pygame.draw.rect(self.screen, self.WHITE, (x-2, y-2, 404, 34))
    pygame.draw.rect(self.screen, self.BLACK, (x, y, 400, 30))
    ratio = health / health_og

    if ratio > 0.75:
        health_color = self.GREEN
    elif ratio > 0.50:
        health_color = self.YELLOW
    elif ratio > 0.25:
        health_color = self.ORANGE
    else:
        health_color = self.RED

    pygame.draw.rect(self.screen, health_color, (x, y, 400*ratio, 30))

def draw_alt_cooldown_bar(self,x, y, cooldown, cooldown_og):
    pygame.draw.rect(self.screen, self.WHITE, (x-2, y-2, 404, 34))
    pygame.draw.rect(self.screen, self.BLACK, (x, y, 400, 30))
    c = cooldown_og - cooldown
    ratio = c / cooldown_og
    filled_width = int (ratio*400)
    pygame.draw.rect(self.screen, self.BLUE, (x, y,filled_width, 30))

def gameLoop(self):
    #creating two instances of the Fighters
    figter_1 = Fighter(1,200, 310, False, self.WARRIOT_DATA, self.warrior_sheet, self.WARRIOR_ANIMATION_STEPS, self.sword_fx,"Joel\Assets\Images\icons\Victory.png",self.ALT_COOLDOWN)
    figter_2 = Fighter(2, 1700, 310, True, self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS, self.magic_fx,"Joel\Assets\Images\icons\Victory.png",0)

    #game loop
    running = True

    while running:

        self.clock.tick(self.FPS)

        #draw the background
        draw_bg()   

        #draw the health bars
        draw_health_bars(100,figter_1.health, 20, 20)
        draw_health_bars(100,figter_2.health, self.SCREEN_WIDTH - 420, 20)
        draw_text("Player: "+str(self.score[0]), self.score_font, self.WHITE, 440, 20)
        draw_text(str(self.score[1])+" :Boss", self.score_font, self.WHITE, self.SCREEN_WIDTH - 520, 20)
        draw_alt_cooldown_bar(20, 70, figter_1.alt_cooldown, self.ALT_COOLDOWN)

        #update the intro counter
        if intro_counter <=0:
            #move the fighters
            figter_1.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, figter_2,round_over)
            figter_2.move(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.screen, figter_1,round_over)
        else:
            #display the intro counter
            draw_text(str(intro_counter), self.count_font, self.RED, self.SCREEN_WIDTH/2 , self.SCREEN_HEIGHT/3 ) 
            #update counter
            if pygame.time.get_ticks() - last_count_update >= 1000:
                intro_counter -= 1
                last_count_update = pygame.time.get_ticks()
                

    

        #update the fighters
        figter_1.update()
        figter_2.update()

        #draw the fighters
        figter_1.draw(self.screen)
        figter_2.draw(self.screen)


        if round_over == False:
            if figter_1.alive == False:
                self.score[1] += 1
                round_over = True
                round_over_timer = pygame.time.get_ticks()
            elif figter_2.alive == False:
                self.score[0] += 1
                round_over = True
                round_over_timer = pygame.time.get_ticks()
        else:
            #display victory image
            if pygame.time.get_ticks() - round_over_timer >= self.ROUND_OVER_COOLDOWN:
                round_over = False
                intro_counter = 3
                figter_1 = Fighter(1,200, 310, False, self.WARRIOT_DATA, self.warrior_sheet, self.WARRIOR_ANIMATION_STEPS, self.sword_fx,"Joel\Assets\Images\icons\Victory.png",self.ALT_COOLDOWN)
                figter_2 = Fighter(2, 1700, 310, True, self.WIZARD_DATA, self.wizard_sheet, self.WIZARD_ANIMATION_STEPS, self.magic_fx,"Joel\Assets\Images\icons\Victory.png",0)

        ########################################################
        ########################################################
        ########################################################
        ####### have to finish after everything is done ########
        ########################################################
        ########################################################
        ########################################################

        if self.score[0] == 2 and self.score[1] <=1 or self.score[1] == 2 and self.score[0] <=1:
            round_over = True
            if self.score[0] > self.score[1]:
                PLAYER_WINS = True
            else:
                BOSS_WINS = True

        if PLAYER_WINS == True:
            # cover the screen with a black rectangle
            pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            # display the victory image
            self.screen.blit(self.victory_image, (self.SCREEN_WIDTH/2 - self.victory_image.get_width()/2, self.SCREEN_HEIGHT/2 - self.victory_image.get_height()/2))
        if BOSS_WINS == True:
            # cover the screen with a black rectangle
            pygame.draw.rect(self.screen, self.BLACK, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            # display the defeat image
            # screen.blit(defeat_image, (SCREEN_WIDTH/2 - defeat_image.get_width()/2, SCREEN_HEIGHT/2 - defeat_image.get_height()/2))
            # display the defeat text
            draw_text("You have been defeated", self.score_font, self.WHITE, self.SCREEN_WIDTH/2 - 200, self.SCREEN_HEIGHT/2 - 100)



        #event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        #update the display
        pygame.display.update()


#exit the game
pygame.quit()