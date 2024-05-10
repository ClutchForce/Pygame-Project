import pygame

# initialize pygame
pygame.init()

# set up the display window
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Box Collision Game')

# load background image
background_image = pygame.image.load('tile.png')
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# set up colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# set up fonts
font = pygame.font.SysFont('Arial', 30)

# set up box properties
BOX_WIDTH = 50
BOX_HEIGHT = 50
box1_x = WINDOW_WIDTH - BOX_WIDTH  - 700
box1_y = 700
box2_x = WINDOW_WIDTH - BOX_WIDTH -50
box2_y = 50

# set up box movement
box1_move_speed = 3
box1_move_up = False
box1_move_down = False
box1_move_left = False
box1_move_right = False

# set up game loop
game_running = True
while game_running:

    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                box1_move_up = True
            elif event.key == pygame.K_s:
                box1_move_down = True
            elif event.key == pygame.K_a:
                box1_move_left = True
            elif event.key == pygame.K_d:
                box1_move_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                box1_move_up = False
            elif event.key == pygame.K_s:
                box1_move_down = False
            elif event.key == pygame.K_a:
                box1_move_left = False
            elif event.key == pygame.K_d:
                box1_move_right = False

    # move box1
    if box1_move_up:
        box1_y -= box1_move_speed
    elif box1_move_down:
        box1_y += box1_move_speed
    if box1_move_left:
        box1_x -= box1_move_speed
    elif box1_move_right:
        box1_x += box1_move_speed

    # check for collision
    box1_rect = pygame.Rect(box1_x, box1_y, BOX_WIDTH, BOX_HEIGHT)
    box2_rect = pygame.Rect(box2_x, box2_y, BOX_WIDTH, BOX_HEIGHT)
    if box1_rect.colliderect(box2_rect):
        # show collision message
        message_surface = font.render('Hello', True, RED)
        message_rect = message_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        display_surface.fill(WHITE)
        display_surface.blit(message_surface, message_rect)
        pygame.display.update()
        pygame.time.wait(2000)  # wait for 2 seconds
        # reset box positions
        box1_x = WINDOW_WIDTH // 2 - BOX_WIDTH // 2 
        box1_y = WINDOW_HEIGHT // 2 - BOX_HEIGHT // 2
        box2_x = WINDOW_WIDTH - BOX_WIDTH -50
        box2_y = 50
    
    # draw background image
    display_surface.blit(background_image, (0, 0))

    # draw boxes
    pygame.draw.rect(display_surface, BLUE, (box1_x, box1_y, BOX_WIDTH, BOX_HEIGHT))
    pygame.draw.rect(display_surface, RED, (box2_x, box2_y, BOX_WIDTH, BOX_HEIGHT))
    pygame.display.update()

# quit pygame
pygame.quit()