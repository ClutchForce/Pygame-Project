import pygame
from pytmx.util_pygame import load_pygame as lp
import gameAssets as ga
import fights as f
import os
from pygame import mixer
from bossFighter import Fighter

#user must interact with the tutorial enemy and battle it , once its health is 0 the user
#must pick up the key and go to the door to complete the level
#interact is set to ('e') 
class levelTutorial():
    def __init__(self, screen):
        #screen init
        self.screen = screen
        self.WIDTH = screen.get_width()
        self.HEIGHT = screen.get_height()
        self.close = False

        #player dict
        self.player_dict = {
            "Hpots": 5,
            "Heavy Attack": True,
            "Shield": True,
            "coins": 100
            }

        #player sprite init
        self.BOX_WIDTH = 50
        self.BOX_HEIGHT = 50
        self.BOX_SPEED = 5 #[0,0] #x,y
        self.HAS_KEY = False

        self.box = pygame.Rect(175, 275, self.BOX_WIDTH, self.BOX_HEIGHT)

        #key sprite init
        self.KEY_WIDTH = 20
        self.KEY_HEIGHT = 20
        self.key = pygame.Rect(self.WIDTH/2 - self.KEY_WIDTH/2, self.HEIGHT/2 - self.KEY_HEIGHT/2, self.KEY_WIDTH, self.KEY_HEIGHT)
        self.KEY_HIDE = True

        #tutorial sprite init
        self.BOT_WIDTH = 50
        self.BOT_HEIGHT = 50
        self.bot = pygame.Rect(self.WIDTH/2 - self.BOT_WIDTH/2, self.HEIGHT/2 - self.BOT_HEIGHT/2, self.BOT_WIDTH, self.BOT_HEIGHT)
        self.BOT_HIDE = False

        #next level sprite init
        self.END_WIDTH = 20
        self.END_HEIGHT = 200
        self.end = pygame.Rect(self.WIDTH-self.END_WIDTH,self.HEIGHT-self.END_HEIGHT,self.END_WIDTH,self.END_HEIGHT)

    
    def gameLoop(self):

        pygame.display.set_caption("Tutorial")
        running = True
        while running:
            #1 Check for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.close = True
                        running = False
            
            #1 Get the keys that are currently pressed
            keys = pygame.key.get_pressed()
            
            #XBOX < XBOT + BOT_WIDTH AND YBOX < YBOT + BOT_HEIGHT AND XBOT < XBOX + BOX_WIDTH AND YBOT < YBOX + BOX_HEIGHT

            #bot rigid body hit collision 
            collision_tolarance = 10
            self.BOX_SPEED = 5
            if(not self.BOT_HIDE):
                if self.box.colliderect(self.bot):
                    if abs(self.bot.top - self.box.bottom) < collision_tolarance and keys[pygame.K_s]:
                        self.BOX_SPEED = 0
                    if abs(self.bot.bottom - self.box.top) < collision_tolarance and keys[pygame.K_w]:
                        self.BOX_SPEED = 0
                    if abs(self.bot.right - self.box.left) < collision_tolarance and keys[pygame.K_a]:
                        self.BOX_SPEED = 0
                    if abs(self.bot.left - self.box.right) < collision_tolarance and keys[pygame.K_d]:
                        self.BOX_SPEED = 0

            #2 Move the box based on the keys that are pressed within the bounds of the screen
            if keys[pygame.K_w] and self.box.top > 0:
                self.box.move_ip(0, -self.BOX_SPEED)
            if keys[pygame.K_s] and self.box.bottom < self.HEIGHT:
                self.box.move_ip(0, self.BOX_SPEED)
            if keys[pygame.K_a] and self.box.left > 0:
                self.box.move_ip(-self.BOX_SPEED, 0)
            if keys[pygame.K_d] and self.box.right < self.WIDTH:
                self.box.move_ip(self.BOX_SPEED, 0)


            #2 interact
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.box, self.bot) and not self.BOT_HIDE:
                print("interact")
                fight = f.TBFight(self.screen, "lvlT", self.player_dict)
                fight.battle()
                self.BOT_HIDE = True
                self.KEY_HIDE = False
            
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.box, self.key) and not self.KEY_HIDE:
                print("key collect")
                self.HAS_KEY = True
                self.KEY_HIDE = True
            
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.box, self.end) and self.HAS_KEY:
                print("next level")
                running = False
            
            self.render()
    
    def render(self): 
        #TODO add background 
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 0), self.box)
        pygame.draw.rect(self.screen, (255, 255, 255), self.end)

        if(not self.KEY_HIDE):
            pygame.draw.rect(self.screen, (255, 100, 100), self.key)
        if(not self.BOT_HIDE):
            pygame.draw.rect(self.screen, (255, 0, 0), self.bot)
        pygame.display.flip()
    
    def finish(self):
        return (self.player_dict)

class levelOne():
    def __init__(self, screen):
        #screen set up
        self.screen = screen
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        self.close = False

        #Access the tile map
        #lol thx gpt, no idea what this does lmao
        filename = os.path.join(os.path.dirname(__file__), '../Maps/WaterMap2.tmx')
        self.dataTMX = lp(filename)
        map_width = self.dataTMX.width * self.dataTMX.tilewidth
        map_height = self.dataTMX.height * self.dataTMX.tileheight

        #sets the x offset of the map in order for it to be centered
        self.x_offset = (screen_width - map_width) / 2

        mapIMG = os.path.join(os.path.dirname(__file__), '../Maps/Map002.png')
        
        # camera set up
        cam_borders = [0,0,776,0] #left,right,top,bottom
        self.camera_group = ga.CameraGroup(cam_borders,mapIMG,self.dataTMX,self.screen)

        #Player set up and spawn pos
        pos = (1920/2-150,1000-80)
        self.player = ga.Player(pos,screen,self.camera_group)

        #player dict
        self.player_dict = {
            "Hpots": 5,
            "Heavy Attack": True,
            "Shield": True,
            "coins": 100
            }

        #player sprite init
        self.HAS_KEY = False

        #key sprite init
        self.KEY_WIDTH = 32
        self.KEY_HEIGHT = 32
        self.key = pygame.Rect(1136, 0, self.KEY_WIDTH, self.KEY_HEIGHT)
        self.KEY_HIDE = True

        #lvl1 enemy init
        self.BOT_WIDTH = 32
        self.BOT_HEIGHT = 32
        self.bot = pygame.Rect(1136, 0, self.BOT_WIDTH, self.BOT_HEIGHT)
        self.BOT_HIDE = False

        #TROLL enemy init
        self.TROLL_WIDTH = 48
        self.TROLL_HEIGHT = 48
        self.troll = pygame.Rect(504, 0, self.TROLL_WIDTH, self.TROLL_HEIGHT)
        self.TROLL_HIDE = False

        #end sprite init
        self.end_WIDTH = 48
        self.end_HEIGHT = 32
        self.end = pygame.Rect(800, 0, self.KEY_WIDTH, self.KEY_HEIGHT)

        self.offsets = (0,0)

    def gameLoop(self):
        # Set the window title
        pygame.display.set_caption("Map 1 Screen")

        # Create a clock
        clock = pygame.time.Clock()

        # Define a flag to control the main loop
        running = True
        # Main game loop
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user clicks the close button, exit the main loop
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                    elif event.key == pygame.K_p:
                        self.close = True
                        running = False

            #1 Get the keys that are currently pressed
            keys = pygame.key.get_pressed()

            #bot rigid body hit collision 
            #TODO add collision for all sides
            # collision_tolarance = 10
            # if(not self.BOT_HIDE):
            #     if self.bot.colliderect(self.player.getRect()):
            #         if abs(self.bot.top - self.player.getRect().bottom) < collision_tolarance and keys[pygame.K_s]:
            #             self.player.update(["bottom"])
            #             print("bot")
            #         if abs(self.bot.bottom - self.player.getRect().top) < collision_tolarance and keys[pygame.K_w]:
            #             self.player.update(["top"])
            #             print("top")
            #         if abs(self.bot.right - self.player.getRect().left) < collision_tolarance and keys[pygame.K_a]:
            #             self.player.update(["left"])
            #             print("left")
            #         if abs(self.bot.left - self.player.getRect().right) < collision_tolarance and keys[pygame.K_d]:
            #             self.player.update(["right"])
            #             print("right")

            #2 interact
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.player.getRect(), self.bot) and not self.BOT_HIDE:
                print("interact")
                fight = f.TBFight(self.screen,"lvl1",self.player_dict)
                fight.battle()
                self.player_dict = fight.getDict()
                self.BOT_HIDE = True
                self.KEY_HIDE = False

            if keys[pygame.K_e] and pygame.Rect.colliderect(self.player.getRect(), self.troll) and not self.TROLL_HIDE:
                print("interact w troll")
                trivia = 1 #TODO add class
                #trivia.call method
                #self.player_dict = fight.getDict()
                self.TROLL_HIDE = True
            
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.player.getRect(), self.key) and not self.KEY_HIDE:
                print("key collect")
                self.HAS_KEY = True
                self.KEY_HIDE = True
            
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.player.getRect(), self.end) and self.HAS_KEY:
                print("next level")
                running = False

            self.render()
           


    #render function
    def render(self):
        self.screen.fill((0, 0, 0))
        #render function
        self.camera_group.custom_draw(self.player)
        self.offsets = self.camera_group.getOffset()
        #print(self.offsets)

        if(not self.KEY_HIDE):
            self.key.y = self.offsets[1]+480
            pygame.draw.rect(self.screen, (255, 100, 100), self.key)
        if(not self.BOT_HIDE):
            self.bot.y = self.offsets[1]+480
            pygame.draw.rect(self.screen, (255, 255, 0), self.bot) 
        if(not self.TROLL_HIDE):
            self.troll.y = self.offsets[1]+800
            pygame.draw.rect(self.screen, (0, 255, 0), self.troll) 

        self.end.y = self.offsets[1]+304
        #pygame.draw.rect(self.screen, (0, 0, 0), self.end)       
        pygame.display.flip()

class levelTwo():
    def __init__(self, screen):
        #screen set up
        self.screen = screen
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.close = False

        #Access the tile map
        #lol thx gpt, no idea what this does lmao
        filename = os.path.join(os.path.dirname(__file__), '../Maps/earthlevel.tmx')
        self.dataTMX = lp(filename)
        map_width = self.dataTMX.width * self.dataTMX.tilewidth
        map_height = self.dataTMX.height * self.dataTMX.tileheight

        #sets the x offset of the map in order for it to be centered
        self.x_offset = (self.screen_width - map_width) / 2

        mapIMG = os.path.join(os.path.dirname(__file__), '../Maps/Map007.png')
        
        # camera set up
        cam_borders = [0,0,920,0] #left,right,top,bottom
        self.camera_group = ga.CameraGroup(cam_borders,mapIMG,self.dataTMX,self.screen)

        #Player set up and spawn pos
        #TODO: player spawn pos
        pos = (960+348,1000-80)
        self.player = ga.Player(pos,screen,self.camera_group)

        #player dict
        self.player_dict = {
            "Hpots": 5,
            "Heavy Attack": True,
            "Shield": True,
            "coins": 100
            }

        #player sprite init
        self.HAS_KEY = False

        #key sprite init
        self.KEY_WIDTH = 32
        self.KEY_HEIGHT = 32
        self.key = pygame.Rect(1072, 0, self.KEY_WIDTH, self.KEY_HEIGHT)
        self.KEY_HIDE = True

        #lvl2 enemy init
        self.BOT_WIDTH = 32
        self.BOT_HEIGHT = 32
        self.bot = pygame.Rect(1072, 0, self.BOT_WIDTH, self.BOT_HEIGHT)
        self.BOT_HIDE = False

        #end sprite init
        self.end_WIDTH = 48
        self.end_HEIGHT = 48
        self.end = pygame.Rect(1440, 0, self.end_WIDTH, self.end_HEIGHT)

        self.offsets = (0,0)


    def gameLoop(self):
        # Set the window title
        pygame.display.set_caption("Map 2 Screen")

        # Create a clock
        clock = pygame.time.Clock()

        # Define a flag to control the main loop
        running = True
        # Main game loop
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user clicks the close button, exit the main loop
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                    elif event.key == pygame.K_p:
                        self.close = True
                        running = False

            #1 Get the keys that are currently pressed
            keys = pygame.key.get_pressed()

            #TODO add 1 enemy
            #TODO add 1 key
            #TODO add 1 door  
            #2 interact
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.player.getRect(), self.bot) and not self.BOT_HIDE:
                print("interact")
                fight = f.TBFight(self.screen,"lvl2",self.player_dict)
                fight.battle()
                self.player_dict = fight.getDict()
                self.BOT_HIDE = True
                self.KEY_HIDE = False
            
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.player.getRect(), self.key) and not self.KEY_HIDE:
                print("key collect")
                self.HAS_KEY = True
                self.KEY_HIDE = True
            
            if keys[pygame.K_e] and pygame.Rect.colliderect(self.player.getRect(), self.end) and self.HAS_KEY:
                print("next level")
                running = False

            self.render()    

            self.render()

    #render function
    def render(self):
        self.screen.fill((0, 0, 0))
        #render function
        self.camera_group.custom_draw(self.player)
        self.offsets = self.camera_group.getOffset()

        if(not self.KEY_HIDE):
            self.key.y = self.offsets[1]+800
            pygame.draw.rect(self.screen, (255, 100, 100), self.key)
        if(not self.BOT_HIDE):
            self.bot.y = self.offsets[1]+800
            pygame.draw.rect(self.screen, (255, 255, 0), self.bot) 

        self.end.y = self.offsets[1]+384
        #pygame.draw.rect(self.screen, (255, 255, 0), self.end) 

        pygame.display.flip()

class levelThree():
    def __init__(self, screen):
        #screen set up
        self.screen = screen
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        self.close = False

        #Access the tile map
        #lol thx gpt, no idea what this does lmao
        filename = os.path.join(os.path.dirname(__file__), '../Maps/lavaMap.tmx')
        self.dataTMX = lp(filename)
        map_width = self.dataTMX.width * self.dataTMX.tilewidth
        map_height = self.dataTMX.height * self.dataTMX.tileheight

        #sets the x offset of the map in order for it to be centered
        self.x_offset = (screen_width - map_width) / 2

        mapIMG = os.path.join(os.path.dirname(__file__), '../Maps/Map006.png')
        
        # camera set up
        #TODO: fix camera borders
        cam_borders = [600,600,960,0] #left,right,top,bottom
        self.camera_group = ga.CameraGroup(cam_borders,mapIMG,self.dataTMX,self.screen)

        #Player set up and spawn pos
        pos = (1920/2,1000-80)
        self.player = ga.Player(pos,screen,self.camera_group)

    def gameLoop(self):
        # Set the window title
        pygame.display.set_caption("Map 3 Screen")

        # Create a clock
        clock = pygame.time.Clock()

        # Define a flag to control the main loop
        running = True
        # Main game loop
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user clicks the close button, exit the main loop
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                    elif event.key == pygame.K_p:
                        self.close = True
                        running = False

            self.render()

    #render function
    def render(self):
        self.screen.fill((0, 0, 0))
        #render function
        self.camera_group.custom_draw(self.player)
        pygame.display.flip()

class levelFour():
    def __init__(self, screen):
        #screen set up
        self.screen = screen
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        #Access the tile map
        #lol thx gpt, no idea what this does lmao
        filename = os.path.join(os.path.dirname(__file__), '../Maps/FinalMap.tmx')
        self.dataTMX = lp(filename)
        map_width = self.dataTMX.width * self.dataTMX.tilewidth
        map_height = self.dataTMX.height * self.dataTMX.tileheight

        #sets the x offset of the map in order for it to be centered
        self.x_offset = (screen_width - map_width) /2

        mapIMG = os.path.join(os.path.dirname(__file__), '../Maps/Map008.png')
        
        # camera set up
        #TODO: fix camera borders
        cam_borders = [0,0,960,0] #left,right,top,bottom
        self.camera_group = ga.CameraGroup(cam_borders,mapIMG,self.dataTMX,self.screen)

        #Player set up and spawn pos
        pos = (960-28,1000-168)
        self.player = ga.Player(pos,screen,self.camera_group)

    def gameLoop(self):
        # Set the window title
        pygame.display.set_caption("Map 3 Screen")

        # Create a clock
        clock = pygame.time.Clock()

        # Define a flag to control the main loop
        running = True
        # Main game loop
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user clicks the close button, exit the main loop
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
                    elif event.key == pygame.K_p:
                        self.close = True
                        running = False

            self.render()

    #render function
    def render(self):
        self.screen.fill((0, 0, 0))
        #render function
        self.camera_group.custom_draw(self.player)
        pygame.display.flip()

class levelBoss():
    def __init__(self,screen):
        self.screen = screen
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
    def gameLoop(self):
        pass
    def render(self):
        pass

class levelShop():
    def __init__(self, screen):
        #screen set up
        self.screen = screen
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        #Access the tile map
        #lol thx gpt, no idea what this does lmao
        filename = os.path.join(os.path.dirname(__file__), '../Maps/shop.tmx')
        self.dataTMX = lp(filename)
        map_width = self.dataTMX.width * self.dataTMX.tilewidth
        map_height = self.dataTMX.height * self.dataTMX.tileheight

        #sets the x offset of the map in order for it to be centered
        self.x_offset = (screen_width - map_width) / 2

        mapIMG = os.path.join(os.path.dirname(__file__), '../Maps/Map003.png')
        
        # camera set up
        #TODO: fix camera borders
        cam_borders = [0,0,abs(map_height-1000),0] #left,right,top,bottom
        self.camera_group = ga.CameraGroup(cam_borders,mapIMG,self.dataTMX,self.screen)

        #Player set up and spawn pos
        #TODO: player spawn pos
        pos = (1920/2,1000)
        self.player = ga.Player(pos,screen,self.camera_group)

    def gameLoop(self):
        # Set the window title
        pygame.display.set_caption("Map 3 Screen")

        # Create a clock
        clock = pygame.time.Clock()

        # Define a flag to control the main loop
        running = True
        # Main game loop
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If the user clicks the close button, exit the main loop
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False

            self.render()

    #render function
    def render(self):
        self.screen.fill((0, 0, 0))
        #render function
        self.camera_group.custom_draw(self.player)
        pygame.display.flip()

