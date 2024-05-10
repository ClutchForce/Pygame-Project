import pygame

class Shop():
# Initialize pygame
    pygame.init()

# Set the dimensions of the screen
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Store")
    storeBackground = (255, 255, 255)


    #Define each item in the store, with attributes name price and type
    def __init__(self):
        self.storeItems =  [{"name": "Iron Sword", "price": 100, "type": "earth weapon"},
                            {"name": "Water Gun", "price": 100, "type": "water weapon"},
                            {"name": "Tornado Attack", "price": 150, "type": "air weapon"},
                            {"name": "Fireball", "price": 150, "type": "fire weapon"}, 
                            {"name": "Shield", "price": 100, "type": "armor"},
                            {"name": "Super Shield", "price": 200, "type": "super armor"},
                            {"name": "Health potion", "price": 50, "type": "health"},]
        
        
        self.storeInventory = [] #This is the store's inventory
        self.playerInventory = []#This is the player's inventory
        self.playerCoins = 300 #This is the base gold of the player
        self.playerHealth = 100 #This is the base health of the player
        self.playerAttack = 10 #This is the base attack of the player

        
    #This function allows the player to buy an item from the store, subtracting from their gold and adding to their inventory
    def buyItem(self, item):
        if self.playerCoins >= item["price"]:
            self.playerCoins -= item["price"]
            self.playerInventory.append(item)
            self.storeInventory.remove(item)
        else:
            print("You don't have enough gold!") 

    #This function allows the user to update their stats based on the item they bought
    def update(self, item):
        if item["type"] == "earth weapon" "water weapon":
                self.playerAttack += 10
        elif item["type"] == "fire weapon" "air weapon":
                self.playerAttack += 15
        elif item["type"] == "armor":
                self.playerHealth += 20
        elif item["type"] == "super armor":
                self.playerHealth += 50
        elif item["type"] == "health":
                self.playerHealth += 10

    def draw(self, screen):
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont("arial", 30)
        text = font.render("Welcome to the store! Press 1-7 to buy an item, or press escape to exit.", 1, (0, 0, 0))
        screen.blit(text, (10, 10))
        text = font.render("You have " + str(self.playerCoins) + " gold.", 1, (0, 0, 0))
        screen.blit(text, (10, 50))
        text = font.render("You have " + str(self.playerHealth) + " health.", 1, (0, 0, 0))
        screen.blit(text, (10, 90))
        text = font.render("You have " + str(self.playerAttack) + " attack.", 1, (0, 0, 0))
        screen.blit(text, (10, 130))
        text = font.render("Press 1 to buy an Iron Sword for 100 gold.", 1, (0, 0, 0))
        screen.blit(text, (10, 170))
        text = font.render("Press 2 to buy a Water Gun for 100 gold.", 1, (0, 0, 0))
        screen.blit(text, (10, 210))
        text = font.render("Press 3 to buy a Tornado Attack for 150 gold.", 1, (0, 0, 0))
        screen.blit(text, (10, 250))
        text = font.render("Press 4 to buy a Fireball for 150 gold.", 1, (0, 0, 0))
        screen.blit(text, (10, 290))
        text = font.render("Press 5 to buy a Shield for 100 gold.", 1, (0, 0, 0))
        screen.blit(text, (10, 330))
        text = font.render("Press 6 to buy a Super Shield for 200 gold.", 1, (0, 0, 0))
        screen.blit(text, (10, 370))
        text = font.render("Press 7 to buy a Health potion for 50 gold.", 1, (0, 0, 0))
        screen.blit(text, (10, 410))
        pygame.display.update()

         
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1:
                            self.buyItem(self.storeItems[0])
                            self.update(self.storeItems[0])
                        if event.key == pygame.K_2:
                            self.buyItem(self.storeItems[1])
                            self.update(self.storeItems[1])
                        if event.key == pygame.K_3:
                            self.buyItem(self.storeItems[2])
                            self.update(self.storeItems[2])
                        if event.key == pygame.K_4:
                            self.buyItem(self.storeItems[3])
                            self.update(self.storeItems[3])
                        if event.key == pygame.K_5:
                            self.buyItem(self.storeItems[4])
                            self.update(self.storeItems[4])
                        if event.key == pygame.K_6:
                            self.buyItem(self.storeItems[5])
                            self.update(self.storeItems[5])
                        if event.key == pygame.K_7:
                            self.buyItem(self.storeItems[6])
                            self.update(self.storeItems[6])
                        if event.key == pygame.K_ESCAPE:
                            running = False
            self.draw(self.screen)
            pygame.display.update() 

runGame = Shop()
runGame.run()


 # Quit pygame
pygame.quit()




