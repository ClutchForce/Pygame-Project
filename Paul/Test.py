import pygame
from pytmx.util_pygame import load_pygame as lp
import os

#Tile class not needed for game to work, used for testing and visualizing the tile map
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

#Player class 
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,surf,group):
        super().__init__(group)
        #defines player image
        # playerPic = os.path.join(os.path.dirname(__file__), 'player.png')
        # self.image = pygame.image.load(playerPic).convert_alpha()
        # self.rect = self.image.get_rect(center = pos)
        #defines player as a rect
        self.rect = pygame.Rect((pos),(32,32))
        self.direction = pygame.math.Vector2()
        self.speed = 5    
        self.surface = surf 

        #rect object of the surface
        self.surfRect = self.surface.get_rect()

    #controls the player movement and collisions
    def input(self, getHits):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            if(self.rect.top < self.surfRect.top):
                self.direction.y = 0
            elif('top' in getHits):
                print('hit top')
                self.direction.y = 0
            else:
                self.direction.y = -1
        elif keys[pygame.K_s]:
            if(self.rect.bottom > self.surfRect.bottom):
                self.direction.y = 0
            elif('bottom' in getHits):
                print('hit bot')
                self.direction.y = 0
            else:
                self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            if(self.rect.right > self.surfRect.right):
                self.direction.x = 0
            elif('right' in getHits):
                print('hit right')
                self.direction.x = 0
            else:
                self.direction.x = 1
        elif keys[pygame.K_a]:
            if(self.rect.left < self.surfRect.left):
                self.direction.x = 0
            elif('left' in getHits):
                print('hit left')
                self.direction.x = 0
            else:
                self.direction.x = -1
        else:
            self.direction.x = 0

    #Render the player
    def update(self,getHits):
        self.input(getHits)
        self.rect.center += self.direction * self.speed
        pygame.draw.rect(self.surface,'red',self.rect,5)

    




class CameraGroup(pygame.sprite.Group):
    def __init__(self,borders):
        super().__init__()
        self.displaySurface = pygame.display.get_surface()

        #Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.displaySurface.get_size()[0]//2
        self.half_h = self.displaySurface.get_size()[1]//2

        #Camera box setup
        self.camera_borders = {'left': borders[0], 'right': borders[1],'top': borders[2],'bottom': borders[3]}
        left = self.camera_borders['left']
        top = self.camera_borders['top']
        width = self.displaySurface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        height = self.displaySurface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(left,top,width,height)

        #Map Image setup
        mapIMG = os.path.join(os.path.dirname(__file__), '../Maps/Map002.png')
        self.ground_surf = pygame.image.load(mapIMG).convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = ((1920-1680)/2,-776))

    #this set the camera offest to the center of the target(Player)
    def center_target_camera(self,target):
        self.offset.x = target.rect.centerx - self.half_w 
        self.offset.y = target.rect.centery - self.half_h
    
    #this controlls how close the player must be to the border b4 it starts moving away
    def box_target_camera(self,target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top  < self.camera_rect.top:
            self.camera_rect.top = target.rect.top 
        if target.rect.bottom  > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom 

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']
    
    def custom_draw(self,player,x_offset,dataTMX):
        #vector to hold the map offset
        ground_offset = self.ground_rect.topleft - self.offset

        getHits = ['null']

        #setup a sprite group, Not needed for game to work, used for testing and visualizing the tile map
        # sprite_group = pygame.sprite.Group()

        #cycles through boundary layer
        #TODO this is very inefficent as it cycles through every tile in the map, need to find a way to only cycle through the tiles that are in the camera view or close to the player
        for layer in dataTMX.visible_layers:
            if layer.name in ('Bounds'):
                yp = 0
                for x in layer.data:
                    xp = 0
                    for y in x:
                        #create a rect object for the current tile
                        xpos = xp*16+ground_offset[0]
                        ypos = yp*16+ground_offset[1]
                        tileRect = pygame.Rect(xpos,ypos,16,16)
                        #create a rect object for the player's center pixel
                        centerPlayer = pygame.Rect(player.rect.centerx,player.rect.centery,1,1)

                        #checks if the player is at the edge of the tile and creates a list of the adjacent tiles ID's
                        if y == 0 and tileRect.colliderect(centerPlayer):
                            adjTop = 0
                            adjBottom = 0
                            adjLeft = 0
                            adjRight = 0  
                            try:
                                adjTop = layer.data[yp-1][xp]
                            except IndexError:
                                pass
                            try:
                                adjBottom = layer.data[yp+1][xp]
                            except IndexError:
                                pass
                            try:
                                adjLeft = layer.data[yp][xp-1]
                            except IndexError:
                                pass
                            try:
                                adjRight = layer.data[yp][xp+1]
                            except IndexError:
                                pass
                            #list of the adjacent tiles ID's
                            tileAdj = [adjLeft,adjRight,adjTop,adjBottom]
                            
                            #list of the borders hit
                            getHits = self.checkHit(centerPlayer,tileRect,tileAdj)

                        xp+=1
                    yp+=1

                #Not needed for game to work, used for testing and visualizing the tile map
                # for x,y,surf in layer.tiles():
                #     Tile((x*16+ground_offset[0],y*16+ground_offset[1]),surf,sprite_group)

        #draws the map image on the screen
        self.displaySurface.blit( self.ground_surf,  ground_offset)

        #draws the camera rect on the screen
        # pygame.draw.rect(self.displaySurface,'yellow',self.camera_rect,5)
        
        #Not needed for game to work, used for testing and visualizing the tile map
        # sprite_group.draw(screen) 

        #draws the player on the screen
        player.update(getHits)

		#camera box movment and centering
        self.center_target_camera(player)
        self.box_target_camera(player)

    #checks if a collision border is hit and returns a list of the borders hit
    def checkHit(self,target,tile,tileAdj):
        hits = []
        #checks to see if the player is at a border with a non 0 ID tile if so appends direction to hits list
        if tileAdj[0] != 0:
            hits.append('left')
        if tileAdj[1] != 0:
            hits.append( 'right')
        if tileAdj[2] != 0:
            hits.append( 'top')
        if tileAdj[3] != 0:
            hits.append( 'bottom')
        return hits

pygame.init()

# Set the screen dimensions
screen_width = 1920
screen_height = 1000

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

#Access the tile map
#lol thx gpt, no idea what this does lmao
filename = os.path.join(os.path.dirname(__file__), 'WaterMap2.tmx')
dataTMX = lp(filename)

#sets the map width and hight of dataTMX in pixels
map_width = dataTMX.width * dataTMX.tilewidth
map_height = dataTMX.height * dataTMX.tileheight

#sets the x offset of the map in order for it to be centered
x_offset = (screen_width - map_width) / 2

# camera set up
cam_borders = [0,0,776,0] #left,right,top,bottom
camera_group = CameraGroup(cam_borders)

#Player set up and spawn pos
pos = (1920/2-150,1000-64)
player = Player(pos,screen,camera_group)

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
        


    # Fill the screen with black
    screen.fill((0, 0, 0))
    
    #render function
    camera_group.custom_draw(player,x_offset,dataTMX)
    
    # Update the screen
    pygame.display.flip()

# Quit Pygame
pygame.quit()
