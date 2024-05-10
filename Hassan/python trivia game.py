import pygame
from pygame.locals import *

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Initialize Pygame
pygame.init()

# Set up the Pygame window
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
gameBackground = pygame.image.load("background-trivia.png")
pygame.display.set_caption("Quiz")

# Set up the font for displaying text
font = pygame.font.SysFont(None, 48)

# Define the questions and answers
questions = ["What is the capital of France?",             "What is the largest planet in our solar system?",             "What is the tallest mountain in the world?",             "What is the name of the world's largest ocean?",]

answers = [["Paris", "London", "Berlin", "Madrid"],
           ["Jupiter", "Saturn", "Neptune", "Mars"],
           ["Mount Everest", "K2", "Makalu", "Cho Oyu"],
           ["Pacific", "Atlantic", "Indian", "Arctic"],]

# Calculate the position of the answer options
answer_width = screen_width // 2 - 50
answer_height = (screen_height // 2 - 100) // 2 - 50
answer_positions = [
    (50, screen_height // 2),
    (screen_width // 2 + 50, screen_height // 2),
    (50, screen_height // 2 + answer_height + 100),
    (screen_width // 2 + 50, screen_height // 2 + answer_height + 100),
]

# Calculate the maximum width of all answer options
max_answer_width = max([font.size(answer)[0] for answer_list in answers for answer in answer_list])

# Calculate the starting position for the answer options
start_x = screen_width // 2 - max_answer_width // 2

# Introduction sequence
intro_text = font.render("You must prove that you are wise in order to continue!", True, WHITE)
continue_text = font.render("Press Enter to continue", True, WHITE)
intro_text_rect = intro_text.get_rect(center=(screen_width/2, screen_height/3))
continue_text_rect = continue_text.get_rect(center=(screen_width/2, screen_height/2))

screen.blit(gameBackground, (0,0))
screen.blit(intro_text, intro_text_rect)
screen.blit(continue_text, continue_text_rect)
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                break
    else:
        continue
    break

# Start the game loop
question_index = 0
while question_index < len(questions):
    # Set up the current question
    current_question = questions[question_index]
    current_answers = answers[question_index]

    # Draw the question and answers on the screen
    screen.blit(gameBackground, (0,0))
    question_text = font.render(current_question, True, WHITE)
    question_text_rect = question_text.get_rect(center=(screen_width/2, screen_height/4))
    screen.blit(question_text, question_text_rect)

    # Draw the answer options with borders around them
    max_answer_width = max([font.size(answer)[0] for answer in current_answers])
    answer_rects = []
    for i, answer in enumerate(current_answers):
        answer_surface = font.render(answer, True, WHITE)
        answer_width, answer_height = font.size(answer)
        answer_x = answer_positions[i][0]
        answer_y = answer_positions[i][1]
        answer_rect = answer_surface.get_rect(center=(answer_x + (answer_width // 2), answer_y + (answer_height // 2)))
        # pygame.draw.rect(screen, GRAY, answer_rect, 2)
        screen.blit(answer_surface, answer_rect)
        answer_rects.append(answer_rect)

    # Update the display
    pygame.display.update()

    # Wait for the user to select an answer
    user_answer = None
    while user_answer is None:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                # Check which answer was clicked
                for i, answer_rect in enumerate(answer_rects):
                    if answer_rect.collidepoint(pygame.mouse.get_pos()):
                        user_answer = current_answers[i]

    # Check if the user's answer is correct
    if user_answer is not None and user_answer == current_answers[0]:
        question_index += 1
    else:
        # Show the correct answer
        correct_text = font.render(f"Wrong, Try Again", True, WHITE)
        correct_text_rect = correct_text.get_rect(center=(screen_width/2, (3*screen_height)//4))
        screen.blit(correct_text, correct_text_rect)
        pygame.display.update()
        pygame.time.delay(2000)
        question_index = 0

# End the game
end_text = font.render("Congratulations! You are wise.", True, WHITE)
screen.fill(BLACK)
screen.blit(end_text, (50, 50))
pygame.display.update()
pygame.time.delay(2000)
pygame.quit()
