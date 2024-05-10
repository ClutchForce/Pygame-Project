import pygame
import button
import shop

pygame.init()

#create game window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

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
        pauseGame = True
    if event.type == pygame.QUIT:
      running = False

  pygame.display.update()

pygame.quit()