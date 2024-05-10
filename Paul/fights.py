import pygame
import random
import os

class TBFight():
    def __init__(self,screen,map,player_dict):
        self.player_dict = player_dict

        #screen init
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        # Set up the game variables
        self.player_health = 100
        self.opponent_health = 100
        self.player_turn = True

        # Set up the buttons
        self.button_width = 400
        self.button_height = 200
        self.button_padding = 80

        self.attack1_button = pygame.Rect(
            self.button_padding/2,
            self.HEIGHT - self.button_height - self.button_padding/2,
            self.button_width,
            self.button_height,
        )
        self.attack2_button = pygame.Rect(
            self.attack1_button.right + self.button_padding,
            self.HEIGHT - self.button_height - self.button_padding/2,
            self.button_width,
            self.button_height,
        )
        self.block_button = pygame.Rect(
            self.attack2_button.right + self.button_padding,
            self.HEIGHT - self.button_height - self.button_padding/2,
            self.button_width,
            self.button_height,
        )
        self.heal_button = pygame.Rect(
            self.block_button.right + self.button_padding,
            self.HEIGHT - self.button_height - self.button_padding/2,
            self.button_width,
            self.button_height,
        )

        # Set up the fonts
        self.font = pygame.font.SysFont(None, 40)

        if map == "lvl1":
            self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '../BattleTypes/WATER.png'))
        elif map == "lvl2":
            self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '../BattleTypes/EARTH.png'))
        else:
            self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), '../BattleTypes/FIRE.png'))



    def battle(self):
        # Set up the clock
        clock = pygame.time.Clock()
        
        # Set up the game loop
        game_running = True
        while game_running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle button clicks
                    if self.player_turn:
                        if self.attack1_button.collidepoint(event.pos):
                            damage = random.randint(10, 20)
                            self.opponent_health -= damage
                            self.player_turn = False
                        elif self.attack2_button.collidepoint(event.pos) and self.player_dict["Heavy Attack"]:
                            damage = random.randint(15, 30)
                            self.opponent_health -= damage
                            self.player_turn = False
                        #TODO add functionality to block button
                        elif self.block_button.collidepoint(event.pos) and self.player_dict["Shield"]:
                            self.player_turn = False
                        elif self.heal_button.collidepoint(event.pos) and self.player_dict["Hpots"]>0:
                            self.player_health += random.randint(10, 20)
                            self.player_turn = False
                            self.player_dict["Hpots"] -= 1

                    else:
                        # Opponent's turn
                        damage = random.randint(5, 15)
                        self.player_health -= damage
                        self.player_turn = True
            
            # Check for a winner
            if self.player_health <= 0:
                winner_text = self.font.render("Opponent wins!", True, (255, 0, 0))
                self.screen.blit(winner_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2))
                pygame.display.update()
                pygame.time.wait(3000)
                game_running = False
            elif self.opponent_health <= 0:
                winner_text = self.font.render("Player wins!", True, (0, 255, 0))
                self.screen.blit(winner_text, (self.WIDTH // 2 - 100, self.HEIGHT // 2))
                pygame.display.update()
                pygame.time.wait(3000)
                game_running = False


            # Draw the background
            self.render() 
    def getDict(self):
        return self.player_dict
    
    def render(self): 
        # Set up the colors
        black = (0, 0, 0)
        white = (255, 255, 255)
        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0,0,255)
        yellow = (255, 255, 0)


        # Load the images
        # player_image = pygame.image.load("pika.png")
        # opponent_image = pygame.image.load("char.png")
        attack1_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'image.png'))
        attack2_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'image (1).png'))
        block_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'image (2).png'))
        heal_image = pygame.image.load(os.path.join(os.path.dirname(__file__), 'image (3).png'))

        

        #fill background
        #TODO Add background image dependent on location
        self.screen.blit(self.image, (0,0))

        #show player & bot
        # self.screen.blit(player_image, (game_display.get_width() // 4, game_display.get_height() // 2))
        # self.screen.blit(opponent_image, (game_display.get_width() * 3 // 4, game_display.get_height() // 2))
        pygame.draw.rect(self.screen,yellow, pygame.Rect(200,200,400,400))
        pygame.draw.rect(self.screen,red, pygame.Rect(self.WIDTH-600,200,400,400))

        # Draw the buttons
        pygame.draw.rect(self.screen, blue, self.attack1_button)
        self.screen.blit(attack1_image, (self.attack1_button.x, self.attack1_button.y))
        pygame.draw.rect(self.screen, red, self.attack2_button)
        self.screen.blit(attack2_image, (self.attack2_button.x,self.attack2_button.y))
        pygame.draw.rect(self.screen, green, self.block_button)
        self.screen.blit(block_image, (self.block_button.x, self.block_button.y))
        pygame.draw.rect(self.screen, yellow, self.heal_button)
        self.screen.blit(heal_image, (self.heal_button.x, self.heal_button.y))

        # Draw the health bars
        player_health_bar_width = self.player_health * 2
        pygame.draw.rect(
            self.screen, green, (50, 50, player_health_bar_width, 25)
        )
        opponent_health_bar_width = self.opponent_health * 2
        pygame.draw.rect(
            self.screen,
            green,
            (self.WIDTH - opponent_health_bar_width - 50, 50, opponent_health_bar_width, 25),
        )

        # Draw the turn indicator
        if self.player_turn:
            turn_text = self.font.render("Player's turn", True, black)
        else:
            turn_text = self.font.render("Opponent's turn", True, black)
        self.screen.blit(turn_text, (self.WIDTH // 2 - 75, 20))

        pygame.display.flip()


class FinalBossFight ():
    def __init__(self):
        pass


class TriviaFight():
    def __init__(self):
        pass

    