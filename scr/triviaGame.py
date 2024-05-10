import pygame
from pygame.locals import *

class trivGame():
    def __init__(self,screen):
        #screen init
        self.screen = screen
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        gameBackground = pygame.image.load("trivia-bg.png")
        pygame.display.set_caption("Quiz")
        firstBackground = pygame.image.load("AIR.png")

        # Define some colors
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GRAY = (128, 128, 128)

        # Set up the font for displaying text
        font = pygame.font.SysFont('Times New Roman', 48)
        font2 = pygame.font.SysFont('Times New Roman', 30)

        # Define the questions and answers
        questions = ["What is the capital of France?",             "What is the largest planet in our solar system?",             "What is the tallest mountain in the world?",             "What is the name of the world's largest ocean?",]

        answers = [["Paris", "London", "Berlin", "Madrid"],
                ["Jupiter", "Saturn", "Neptune", "Mars"],
                ["Mount Everest", "K2", "Makalu", "Cho Oyu"],
                ["Pacific", "Atlantic", "Indian", "Arctic"]]
        
        # Calculate the position of the answer options
        answer_width = screen_width // 2 - 50
        answer_height = (screen_height // 2 - 100) // 2 - 50
        answer_positions = [
            (450,760), # Paris
            (450, 860), # London
            (1200,760), # Berlin
            (1200,860), # Madrid
        ]

        # Calculate the maximum width of all answer options
        max_answer_width = max([font.size(answer)[0] for answer_list in answers for answer in answer_list])

        # Calculate the starting position for the answer options
        start_x = screen_width // 2 - max_answer_width // 2

    def intro(self):
        # Introduction sequence
        intro_text = font.render("You must prove that you are wise in order to continue!", True, BLACK)
        continue_text = font.render("Press Enter to continue", True, BLACK)
        intro_text_rect = intro_text.get_rect(center=(screen_width/2, screen_height/3))
        continue_text_rect = continue_text.get_rect(center=(screen_width/2, screen_height/2))

        screen.blit(firstBackground, (0,0))
        screen.blit(intro_text, intro_text_rect)
        screen.blit(continue_text, continue_text_rect)
        pygame.display.update()

    def gameLoop(self):
        # Start the game loop
        question_index = 0
        tries_remaining = 3
        tries_text = font2.render(f"Tries: {tries_remaining}", True, WHITE)
        tries_rect = tries_text.get_rect(topright=(screen_width-10, 10))
        screen.blit(tries_text, tries_rect)
        while question_index < len(questions):
            # Set up the current question
            current_question = questions[question_index]
            current_answers = answers[question_index]
            title_text = font.render("Trivia Game", True, WHITE)
            title_text_rect = title_text.get_rect(center=(660,690))    

            # Draw the question and answers on the screen
            screen.blit(gameBackground, (0,0))
            question_text = font.render(current_question, True, BLACK)
            question_text_rect = question_text.get_rect(center=(950,400))
            screen.blit(question_text, question_text_rect)
            screen.blit(title_text,title_text_rect)

            # Draw the answer options with borders around them
            max_answer_width = max([font.size(answer)[0] for answer in current_answers])
            answer_rects = []
            for i, answer in enumerate(current_answers):
                answer_surface = font.render(answer, True, BLACK)
                answer_width, answer_height = font.size(answer)
                answer_x = answer_positions[i][0]
                answer_y = answer_positions[i][1]
                answer_rect = answer_surface.get_rect(center=(answer_x + (answer_width // 2), answer_y + (answer_height // 2)))
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
                tries_remaining -= 1

                if tries_remaining == 0:
                # Show the "You Failed" message
                    failed_text = font.render("You Failed!", True, BLACK)
                    screen.blit(firstBackground, (0,0))
                    screen.blit(failed_text, (800, 450))
                    pygame.display.update()
                    pygame.time.delay(1000)
                    pygame.quit()
                    sys.exit()
                # Show the correct answer
                correct_text = font2.render(f"Wrong, Try Again - Tries: {tries_remaining}", True, BLACK)
                correct_text_rect = correct_text.get_rect(center=(950,470))
                screen.blit(correct_text, correct_text_rect)
                tries_text = font.render(f"Tries: {tries_remaining}", True, WHITE)
                tries_rect = tries_text.get_rect(topright=(screen_width-10, 10))
                screen.blit(tries_text, tries_rect)
                pygame.display.update()
                pygame.time.delay(1000)
                question_index = 0

        # End the game
        end_text = font.render("Congratulations, you are wise!", True, BLACK)
        screen.blit(firstBackground, (0,0))
        screen.blit(end_text, (650, 450))
        pygame.display.update()
        pygame.time.delay(3000)
        pygame.quit()