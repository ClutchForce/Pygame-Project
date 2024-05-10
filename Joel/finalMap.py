import pygame
from pytmx.util_pygame import load_pygame as lp
import gameAssets as ga
import fights as f

class levelTutorial():

    def __init__(self, screen):
        #screen init
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()

        #player sprite init
        self.BOX_WIDTH = 50
        self.BOX_HEIGHT = 50
        self.BOX_SPEED = 5
        self.box = pygame.Rect(175, 275, self.BOX_WIDTH, self.BOX_HEIGHT)

        #tutorial sprite init
        self.BOT_WIDTH = 50
        self.BOT_HEIGHT = 50
        self.bot = pygame.Rect(self.WIDTH/2 - self.BOT_WIDTH/2, self.HEIGHT/2 - self.BOT_HEIGHT/2, self.BOT_WIDTH, self.BOT_HEIGHT)


        pass
    
    def gameLoop(self):
        pygame.display.set_caption("Tutorial")
        running = True
        while running:
            #1 Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
            
            #1 Get the keys that are currently pressed
            keys = pygame.key.get_pressed()
            #2 Move the box based on the keys that are pressed
            if keys[pygame.K_w] and self.box.top > 0:
                self.box.move_ip(0, -self.BOX_SPEED)
            if keys[pygame.K_s] and self.box.bottom < self.HEIGHT:
                self.box.move_ip(0, self.BOX_SPEED)
            if keys[pygame.K_a] and self.box.left > 0:
                self.box.move_ip(-self.BOX_SPEED, 0)
            if keys[pygame.K_d] and self.box.right < self.WIDTH:
                self.box.move_ip(self.BOX_SPEED, 0)
            #2 interact
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.box, self.bot):
                print("interact")
                fight = f.TBFight(self.screen)
                fight.battle()

            
            self.render()
    
    def render(self):   
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 0), self.box)
        pygame.draw.rect(self.screen, (255, 0, 0), self.bot)
        pygame.display.flip()







class levelOne():
    def __init__(self):
        pass

class levelTwo():
    def __init__(self):
        pass

class levelThree():
    def __init__(self):
        pass

class levelFour():
    def __init__(self):
        pass

class levelBoss():
    def __init__(self):
        pass

class levelShop():
    def __init__(self):
        pass

