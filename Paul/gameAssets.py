import pygame
from pytmx.util_pygame import load_pygame as lp
import os

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
                #print('hit top')
                self.direction.y = 0
            else:
                self.direction.y = -1
        elif keys[pygame.K_s]:
            if(self.rect.bottom > self.surfRect.bottom):
                self.direction.y = 0
            elif('bottom' in getHits):
                #print('hit bot')
                self.direction.y = 0
            else:
                self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            if(self.rect.right > self.surfRect.right):
                self.direction.x = 0
            elif('right' in getHits):
                #print('hit right')
                self.direction.x = 0
            else:
                self.direction.x = 1
        elif keys[pygame.K_a]:
            if(self.rect.left < self.surfRect.left):
                self.direction.x = 0
            elif('left' in getHits):
                #print('hit left')
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

    def getRect(self):
        return self.rect

class CameraGroup(pygame.sprite.Group):
    def __init__(self,borders, mapIMG, dataTMX,screen):
        super().__init__()
        self.displaySurface = screen
        #print(self.displaySurface.get_size())

        #Camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = self.displaySurface.get_size()[0]/2
        self.half_h = self.displaySurface.get_size()[1]/2

        #Camera box setup
        self.camera_borders = {'left': borders[0], 'right': borders[1],'top': borders[2],'bottom': borders[3]}
        left = self.camera_borders['left']
        top = self.camera_borders['top']
        width = self.displaySurface.get_size()[0]  - (self.camera_borders['left'] + self.camera_borders['right'])
        height = self.displaySurface.get_size()[1]  - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(left,top,width,height)

        #TMX setup
        self.dataTMX = dataTMX
        #sets the map width and height of dataTMX in pixels
        map_width = dataTMX.width * dataTMX.tilewidth
        map_height = dataTMX.height * dataTMX.tileheight
        

        #Map Image setup
        self.ground_surf = pygame.image.load(mapIMG).convert_alpha()
        self.ground_rect = self.ground_surf.get_rect(topleft = ((self.displaySurface.get_width()-map_width)/2,self.displaySurface.get_height()-map_height))

        

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

        #this keeps the camera from going out of bounds 
        # TODO find a way to accomodat this for map 3 and 4
        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']
    
    def custom_draw(self,player): 
        #,key_dict,enemy_dict
        #vector to hold the map offset
        self.ground_offset = self.ground_rect.topleft - self.offset
        #print(ground_offset)

        getHits = ['null']

        #setup a sprite group, Not needed for game to work, used for testing and visualizing the tile map
        # sprite_group = pygame.sprite.Group()

        #cycles through boundary layer
        #TODO this is very inefficent as it cycles through every tile in the map, need to find a way to only cycle through the tiles that are in the camera view or close to the player
        for layer in self.dataTMX.visible_layers:
            if layer.name in ('Bounds'):
                yp = 0
                for x in layer.data:
                    xp = 0
                    for y in x:
                        #create a rect object for the current tile
                        xpos = xp*16+self.ground_offset[0]
                        ypos = yp*16+self.ground_offset[1]
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
        self.displaySurface.blit( self.ground_surf,  self.ground_offset)

        #draws the camera rect on the screen
        pygame.draw.rect(self.displaySurface,'yellow',self.camera_rect,5)
        
        #Not needed for game to work, used for testing and visualizing the tile map
        # sprite_group.draw(screen) 

        #draws the player on the screen
        player.update(getHits)
        pygame.draw.rect(self.displaySurface,'yellow',self.camera_rect,5)

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
            #print(tileAdj[2])
        if tileAdj[3] != 0:
            hits.append( 'bottom')
        return hits
    def getOffset(self):
        return self.ground_offset

class Grunt1():
    def __init__(self):
        pass

class Grunt2():
    def __init__(self):
        pass

class Grunt3():
    def __init__(self):
        pass

class Grunt4():
    def __init__(self):
        pass

class Troll():
    def __init__(self):
        pass

class Boss():
    def __init__(self):
        pass

class MerchentShop():
    def __init__(self):
        pass

class WorldBuildingAssets():
    def __init__(self):
        pass

