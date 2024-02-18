# random is used to place the enemies randomly
import random
# math is used to maintain the score
import math
#pygame is used to import all the pygame libraries
import pygame 
#mixer is used to import music and sound into the game 
from pygame import mixer

import emoji

# colors
BLACK = (20, 20, 20)
WHITE = (240, 240, 240)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Initialize Pygame
pygame.init()
pygame.font.init()

# create the screen
screen = pygame.display.set_mode((800,650))

def menu():

    size = (800, 650)
    screen = pygame.display.set_mode(size)

    menu_options = ["Start Game - Tank Turfs", "Mini Game - Quiz", "Instructions", "Quit     "]
    menu_functions = [main_game, minigame_monumentquiz, instructions, quit]

    menu_item_height = 50

    menu_y = 80

    menu_rects = []
    
    # creating rect for menu options
    for i in range(0,3):
        rect = pygame.Rect(0, 0, size[0] // 2, menu_item_height)
        rect.center = (205, menu_y + (i * (menu_item_height+5)))
        menu_rects.append(rect)

    for i in range(4,0,-4):
        rect = pygame.Rect(0, 0, size[0] // 2, menu_item_height)
        rect.center = (205, menu_y + ((i+4) * (menu_item_height+11)))
        menu_rects.append(rect)

    # makes the hover animation smoother
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        menu_bg = pygame.image.load('bg-gradient.jpeg')
        menu_bg = pygame.transform.scale(menu_bg, (800, 800))
        screen.blit(menu_bg, [0, -65])
        
        menu_bg = pygame.image.load('menu_bg.jpg')
        menu_bg = pygame.transform.scale(menu_bg, (980, 550))
        screen.blit(menu_bg, [-60, 50])

        # draw menu items
        for i, rect in enumerate(menu_rects):

            # initialise font for option_text
            option_text = pygame.font.Font(None, 45)
            option_text = option_text.render(menu_options[i], True, WHITE)
            option_rect = option_text.get_rect(center=menu_rects[i].center)
            if rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(option_text, option_rect)
                if pygame.mouse.get_pressed()[0]:
                    # call the function associated with correspnding option
                    menu_functions[i]()
            else:
                # Make the menu option transparent by modifying the BLACK color's alpha value
                pygame.draw.rect(screen, WHITE, rect, 0, border_radius=menu_item_height//2)
            BLACK = (0, 0, 0, 128)
            pygame.font.init()
            text = pygame.font.Font(None, 45)
            text = text.render(menu_options[i], True, BLACK)   # True is Boolean value for anti-aliasing function
            text_rect = text.get_rect(center = rect.center)    # get_rect returns the rectangle
            screen.blit(text, text_rect)

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def quit():
    pygame.quit()

def instructions():

    #the blitting order is important
    menu_bg = pygame.image.load('menu_bg.jpg')
    menu_bg = pygame.transform.scale(menu_bg, (800, 650))
    screen.blit(menu_bg, [0, 0])

    display_left_button = pygame.image.load('left_button.jpg')
    display_left_button = pygame.transform.scale(display_left_button, (220, 110))
    screen.blit(display_left_button, (180, 200))

    display_right_button = pygame.image.load('right_button.jpg')
    display_right_button = pygame.transform.scale(display_right_button, (220, 110))
    screen.blit(display_right_button, (420, 200))

    display_space_button = pygame.image.load('space_button.jpg')
    display_space_button = pygame.transform.scale(display_space_button, (600, 80))
    screen.blit(display_space_button, (110, 350))

    instructions_text = pygame.font.Font('freesansbold.ttf', 40)
    instructions_text = instructions_text.render('Instructions', True, WHITE)
    screen.blit(instructions_text, (290, 50))

    instructions_text2 = pygame.font.Font('freesansbold.ttf', 30)
    instructions_text2 = instructions_text2.render('(Esc to go back)', True, WHITE)
    screen.blit(instructions_text2, (300, 110))
    
    displaying = True
    while displaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                displaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()
        pygame.display.update()

def main_game():
    #PLAYER
    #The values present below determine the position of the tank
    playerImg = pygame.image.load('001-tank.png')

    # intialising initial x and y cordinates of the tank
    playerX = 370
    playerY = 480

    # shifting tank sideways
    playerX_change = 0

    #ENEMY
    #Creating number of enemies for which we use list and the append function,
    # 8 enemies will be made
    enemyImg = []
    enemyX = []
    enemyY = []
    enemyX_change = []
    enemyY_change = []
    num_of_enemies = 8
    for i in range(num_of_enemies):
        enemyImg.append(pygame.image.load('002-shooting.png'))
        enemyX.append(random.randint(0,735))
        enemyY.append(random.randint(50,150))
        # Speed of enemy
        enemyX_change.append(4)
        # Changes the enemy position in y axis
        enemyY_change.append(50)

    #Canon Ball = cb
    #ready = cb not visible to the player
    #fire = cb is moving

    cbImg = pygame.image.load('001-shooting-ball.png')
    cbX = 0
    cbY = 480
    cbX_change = 0
    cbY_change = 10
    cb_state = "ready"


    #SCORE
    # Score to be printed on the screen by using freesansbold style and the size is 32
    score_value = 0
    font = pygame.font.Font('freesansbold.ttf', 34)

    # the position of the score board
    textX = 10
    textY = 10

    def show_score(x,y):
        #rendering the text of the score on the screen
        score = font.render("SCORE :"+ str(score_value), True, (0,255,0))
        screen.blit(score, (x, y))

    def game_over():
        screen.fill(WHITE)

        game_over_text = pygame.font.Font('freesansbold.ttf', 40)
        game_over_text = game_over_text.render("Game Over", True, RED)
        screen.blit(game_over_text, (300, 240))

        game_over_text = pygame.font.Font('freesansbold.ttf', 30)
        game_over_text = game_over_text.render("Press ENTER to play quiz", True, RED)
        screen.blit(game_over_text, (235, 290))

        game_over_text = pygame.font.Font('freesansbold.ttf', 20)
        game_over_text = game_over_text.render("OR Press Esc to go to menu", True, BLACK)
        screen.blit(game_over_text, (285, 380))

        displaying = True
        while displaying:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    displaying = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                        maingame_monumentquiz()
                    elif event.key == pygame.K_ESCAPE:
                        menu()

            pygame.display.flip()
        pygame.quit()
        

    def player(x , y):
        # used to display the tank's image
        screen.blit(playerImg, (x, y))

    def enemy(x , y, i):
        #used to display the multiple enemy images
        screen.blit(enemyImg[i], (x, y))

    #variable made global to be accessed in the definition
    def fire_cb(x , y):
        global cb_state
        cb_state = "fire"
        screen.blit(cbImg, (x+16, y+10))

    def isCollision(enemyX, enemyY, cbX, cbY) :
        #distance = diatance between two coordinates
        distance = math.sqrt((math.pow(enemyX-cbX,2)) + (math.pow(enemyY-cbY,2)))
        if distance < 27 : 
            return True
        else :
            return False
    # Game Loop
    running = True
    while running:
        #RGB - red , green , blue
        screen.fill((0,0,0))

        clock = pygame.time.Clock()

        #Background Image
        screen.blit(background,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # if keystroke is pressed check whether it goes to the right or left side
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -4
                elif event.key == pygame.K_RIGHT:
                    playerX_change = 4
                elif event.key == pygame.K_SPACE:
                    if cb_state == "ready":
                        cb_state = "fire"

                        #Since the cannon ball sound is only played for a while we use Sound function and not Music
                        cb_Sound = mixer.Sound('laser.wav')
                        cb_Sound.play()

                        #helps to get the current coordinate of the tank
                        cbX = playerX
                        fire_cb(cbX, cbY)

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or  event.key == pygame.K_RIGHT:
                    playerX_change = 0
        
        # Boundary of tank so it doesn't go beyond the screen
        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736
        # Movement of the enemy
        #in order for the program understand which enemy are we talking about
        for i in range (num_of_enemies):
            #Even if one of the enemies cross 440 pixels then Game over
            if enemyY[i] > 440:
                for j in range (num_of_enemies):
                  enemyY[j] = 2000
                game_over()

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <=0:
                enemyX_change[i] = 3
                enemyY[i] += enemyY_change[i]

            elif enemyX[i] >= 736:
                enemyX_change[i] = -3
                enemyY[i] += enemyY_change[i]

            # Collision check
            # To calculate the number of collisions
            # also to know which enemy coordinate are we talking about
            collision = isCollision(enemyX[i] , enemyY[i], cbX, cbY)

            if collision :
                #Since the explosion sound is only played for a while we use Sound function and not Music
                explosion_Sound = mixer.Sound('explosion.wav')
                explosion_Sound.play()
                cbY = 480
                cb_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 735)
                enemyY[i] = random.randint(50, 150)
            # to know which enemy coordinate is wanted to be drawn on the screen
            enemy(enemyX[i], enemyY[i], i)
        #Bullet Movement 
        if cbY <= 0 :
            cbY = 480
            cb_state = "ready"
        if  cb_state == "fire":
            fire_cb(cbX, cbY)
            cbY -= cbY_change

        player(playerX, playerY)
        show_score(textX, textY)

        pygame.display.update()
        clock.tick(100)
    pygame.quit()

def correct_answer():

    screen = pygame.display.set_mode((800, 650))

    green = pygame.transform.scale(pygame.image.load("green-bg.jpg"), (800, 650))
    
    correct_text = pygame.font.Font('freesansbold.ttf', 25)
    correct_text = correct_text.render('You guessed it RIGHT !', True, (255, 255, 255))

    font = pygame.font.Font('freesansbold.ttf', 30)
    text_surface = font.render('Press [Enter] to resume tank turfs', True, WHITE)

    goto_menu_text = pygame.font.Font('freesansbold.ttf', 10)
    goto_menu_text = goto_menu_text.render('(Esc - MENU)', True, WHITE)


    displaying = True
    while displaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                displaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    main_game()
                elif event.key == pygame.K_ESCAPE:
                    menu()
        screen.blit(green, [0, 0])
        screen.blit(correct_text, (250, 15))
        screen.blit(text_surface, (160, 305))
        screen.blit(goto_menu_text, (390, 620))
        emoji.happy()

        pygame.display.update()
    pygame.quit()

def minigame_correct_answer():

    screen = pygame.display.set_mode((800, 650))

    green = pygame.transform.scale(pygame.image.load("green-bg.jpg"), (800, 650))

    correct_text = pygame.font.Font('freesansbold.ttf', 25)
    correct_text = correct_text.render('You guessed it RIGHT !', True, (255, 255, 255))

    font = pygame.font.Font('freesansbold.ttf', 30)
    text_surface = font.render('Press [Enter] for new question', True, WHITE)

    goto_menu_text = pygame.font.Font('freesansbold.ttf', 10)
    goto_menu_text = goto_menu_text.render('(Esc - MENU)', True, WHITE)

    displaying = True
    while displaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                displaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    minigame_monumentquiz()
                elif event.key == pygame.K_ESCAPE:
                    menu()

        screen.blit(green, [0, 0])
        screen.blit(correct_text, (250, 15))
        screen.blit(text_surface, (180, 305))
        screen.blit(goto_menu_text, (390, 620))
        emoji.happy()
        pygame.display.update()
    pygame.quit()

def incorrect_answer():

    screen = pygame.display.set_mode((800, 650))
    red = pygame.transform.scale(pygame.image.load("red-bg.jpg"), (800, 650))

    incorrect_text = pygame.font.Font('freesansbold.ttf', 25)
    incorrect_text = incorrect_text.render('You guessed it WRONG !', True, (255, 255, 255))

    font = pygame.font.Font('freesansbold.ttf', 30)
    text_surface = font.render('Press [Enter] to make another guess', True, WHITE)

    goto_menu_text = pygame.font.Font('freesansbold.ttf', 10)
    goto_menu_text = goto_menu_text.render('(Esc - MENU)', True, WHITE)


    displaying = True
    while displaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                displaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    maingame_monumentquiz()
                elif event.key == pygame.K_ESCAPE:
                    menu()

        screen.blit(red, [0, 0])
        screen.blit(incorrect_text, (250, 15))
        screen.blit(text_surface, (155, 305))
        screen.blit(goto_menu_text, (390, 620))
        emoji.sad()
        pygame.display.update()
    pygame.quit()

def minigame_incorrect_answer():

    screen = pygame.display.set_mode((800, 650))

    red = pygame.transform.scale(pygame.image.load("red-bg.jpg"), (800, 650))

    incorrect_text = pygame.font.Font('freesansbold.ttf', 25)
    incorrect_text = incorrect_text.render('You guessed it WRONG !', True, (255, 255, 255))

    font = pygame.font.Font('freesansbold.ttf', 30)
    text_surface = font.render('Press [Enter] to make another guess', True, WHITE)

    goto_menu_text = pygame.font.Font('freesansbold.ttf', 10)
    goto_menu_text = goto_menu_text.render('(Esc - MENU)', True, WHITE)


    displaying = True
    while displaying:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                displaying = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    minigame_monumentquiz()
                elif event.key == pygame.K_ESCAPE:
                    menu()
        screen.blit(red, [0, 0])
        screen.blit(incorrect_text, (250, 15))
        screen.blit(text_surface, (155, 305))
        screen.blit(goto_menu_text, (390, 620))
        emoji.sad()
        pygame.display.update()
    pygame.quit()

def maingame_monumentquiz():

    quiz_bg = pygame.transform.scale(pygame.image.load("quiz-background.jpg"), (800, 650))
    screen.blit(quiz_bg, [0, 0])

    questions = ["SELECT monument situated Agra, India?",
                 "SELECT monument situated in New York City, USA?",
                 "SELECT monument situated in Paris, France?",
                 "SELECT monument situated in Rio de Janeiro, Brazil?",
                 "SELECT monument situated in Beijing, China?",
                 "SELECT monument situated in Rome, Italy?",
                 "SELECT monument situated in London, UK?",
                 "SELECT monument situated in Washington D.C., USA?",
                 "SELECT monument situated in Moscow, Russia?",
                 "SELECT monument situated in Tokyo, Japan?"]

    # list of answers
    answers = [["The Great Wall of China", "The Colosseum", "The Taj Mahal", "The Pyramids of Giza"],
            ["The Eiffel Tower", "The Statue of Liberty", "The Leaning Tower of Pisa", "The Sydney Opera House"],
            ["The Golden Gate Bridge", "The Tower of London", "The Louvre Museum", "The Eiffel Tower"],
            ["The Christ the Redeemer statue", "The Great Sphinx of Giza", "The Acropolis of Athens", "The Parthenon"],
            ["The Temple of Confucius", "The Great Mosque of Xi'an", "The Temple of Heaven", "The Forbidden City"],
            ["The Pantheon", "The Colosseum", "The Leaning Tower of Pisa", "The Trevi Fountain"],
            ["The Westminster Abbey", "London Bridge",  "The Big Ben", "The Buckingham Palace"],
            ["The Lincoln Memorial", "The Washington Monument", "The White House", "The Empire State Building"],
            ["The St. Basil's Cathedral", "The Peter and Paul Fortress", "The Red Square", "The Bolshoi Theatre"],
            ["The Meiji Shrine", "The Tokyo Tower", "The Sensoji Temple", "The Imperial Palace"]]

    correct_answers = [2, 1, 3, 0, 3, 0, 1, 2, 0, 1]
    
    # list of images
    images = [pygame.transform.scale(pygame.image.load("taj-mahal.jpg"), (400, 280)),
          pygame.transform.scale(pygame.image.load("statue-of-liberty.jpg"), (400, 280)),
          pygame.transform.scale(pygame.image.load("eiffel-tower.jpg"), (400, 280)),
          pygame.transform.scale(pygame.image.load("christ-the-redeemer.jpg"), (400, 280)),
          pygame.transform.scale(pygame.image.load("forbidden-city.jpg"), (400, 280)),
          pygame.transform.scale(pygame.image.load("pantheon.jpg"), (400, 280)),
          pygame.transform.scale(pygame.image.load("london-bridge.jpg"), (400, 280)),
          pygame.transform.scale(pygame.image.load("white-house.jpg"), (400, 280)),
          pygame.transform.scale(pygame.image.load("st-basil-cathedral.jpg"), (400, 250)),
          pygame.transform.scale(pygame.image.load("tokyo-tower.jpg"), (400, 280))]
    
    random_question = random.randrange(0, 10)
    image = images[random_question]
    answer_options = answers[random_question]
    correct_answer_index = correct_answers[random_question]

    # shuffle the answer options and correct answers lists in the same way
    shuffled_indices = random.sample(range(len(answer_options)), len(answer_options))
    answer_options = [answer_options[i] for i in shuffled_indices]
    correct_answer_index = shuffled_indices.index(correct_answer_index)

    font = pygame.font.Font(None, 36)
    question_text = font.render(questions[random_question], True, WHITE)

    font = pygame.font.Font(None, 45)
    A = font.render("A", True, WHITE)
    B = font.render("B", True, WHITE)
    C = font.render("C", True, WHITE)
    D = font.render("D", True, WHITE)

    screen.blit(A, [170, 410])
    screen.blit(B, [170, 470])
    screen.blit(C, [170, 530])
    screen.blit(D, [170, 590])

    # dimensions for option box
    box_width = 400
    box_height = 50
    answer_boxes = []
    answer_colors = [WHITE] * len(answer_options)

    for i in range(len(answer_options)):
        # add boxes one below another
        box = pygame.Rect(200, 400 + i * (box_height + 10), box_width, box_height)
        answer_boxes.append(box)
    # answer boxes
    for i in range(len(answer_options)):
        pygame.draw.rect(screen, answer_colors[i], answer_boxes[i])
        text = pygame.font.Font(None, 36)
        text = text.render(answer_options[i], True, BLACK)
        screen.blit(text, [answer_boxes[i].x + 10, answer_boxes[i].y + 12])

    # question text
    screen.blit(question_text, [50, 20])
    # monument image
    screen.blit(image, [200, 85])

    # waiting for user to answer
    answered = False
    while not answered:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                answered = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # answer valid or invalid?
                (x, y) = event.pos
                for i in range(len(answer_options)):
                    if answer_boxes[i].collidepoint(x, y):
                        if correct_answer_index == i:
                            correct_answer()
                        else:
                            incorrect_answer()

        pygame.display.flip()
    pygame.quit()

def minigame_monumentquiz():

    screen = pygame.display.set_mode((800,650))

    questions = ["SELECT monument situated Agra, India?",
                 "SELECT monument situated in New York City, USA?",
                 "SELECT monument situated in Paris, France?",
                 "SELECT monument situated in Rio de Janeiro, Brazil?",
                 "SELECT monument situated in Beijing, China?",
                 "SELECT monument situated in Rome, Italy?",
                 "SELECT monument situated in London, UK?",
                 "SELECT monument situated in Washington D.C., USA?",
                 "SELECT monument situated in Moscow, Russia?",
                 "SELECT monument situated in Tokyo, Japan?"]
    # list of answers
    answers = [["The Great Wall of China", "The Colosseum", "The Taj Mahal", "The Pyramids of Giza"],
               ["The Eiffel Tower", "The Statue of Liberty", "The Leaning Tower of Pisa", "The Sydney Opera House"],
               ["The Golden Gate Bridge", "The Tower of London", "The Louvre Museum", "The Eiffel Tower"],
               ["The Christ the Redeemer statue", "The Great Sphinx of Giza", "The Acropolis of Athens", "The Parthenon"],
               ["The Temple of Confucius", "The Great Mosque of Xi'an", "The Temple of Heaven", "The Forbidden City"],
               ["The Pantheon", "The Colosseum", "The Leaning Tower of Pisa", "The Trevi Fountain"],
               ["The Westminster Abbey", "London Bridge",  "The Big Ben", "The Buckingham Palace"],
               ["The Lincoln Memorial", "The Washington Monument", "The White House", "The Empire State Building"],
               ["The St. Basil's Cathedral", "The Peter and Paul Fortress", "The Red Square", "The Bolshoi Theatre"],
               ["The Meiji Shrine", "The Tokyo Tower", "The Sensoji Temple", "The Imperial Palace"]]

    correct_answer_list = [2, 1, 3, 0, 3, 0, 1, 2, 0, 1]

    # list of images
    images = [pygame.transform.scale(pygame.image.load("taj-mahal.jpg"), (400, 280)),
              pygame.transform.scale(pygame.image.load("statue-of-liberty.jpg"), (400, 280)),
              pygame.transform.scale(pygame.image.load("eiffel-tower.jpg"), (400, 280)),
              pygame.transform.scale(pygame.image.load("christ-the-redeemer.jpg"), (400, 280)),
              pygame.transform.scale(pygame.image.load("forbidden-city.jpg"), (400, 280)),
              pygame.transform.scale(pygame.image.load("pantheon.jpg"), (400, 280)),
              pygame.transform.scale(pygame.image.load("london-bridge.jpg"), (400, 280)),
              pygame.transform.scale(pygame.image.load("white-house.jpg"), (400, 280)),
              pygame.transform.scale(pygame.image.load("st-basil-cathedral.jpg"), (400, 250)),
              pygame.transform.scale(pygame.image.load("tokyo-tower.jpg"), (400, 280))]


    box_width = 400
    box_height = 50
    answer_boxes = []
    answer_color = WHITE

    quiz_bg = pygame.transform.scale(pygame.image.load("quiz-background.jpg"), (800, 650))
    screen.blit(quiz_bg, [0, 0])

    for j in range(4):
        # add boxes one below another
        box = pygame.Rect(200, 400 + j * (box_height + 10), box_width, box_height)
        answer_boxes.append(box)

    points = 0

    for k in range (10):

        # background image
        quiz_bg = pygame.transform.scale(pygame.image.load("quiz-background.jpg"), (800, 650))
        screen.blit(quiz_bg, [0, 0])

        # monument image
        screen.blit(images[k], [200, 85])

        # question text
        question_text = pygame.font.Font(None, 36)
        question_text = question_text.render(questions[k], True, WHITE)
        screen.blit(question_text, [50, 20])

        # answer boxes
        answer_options = answers[k]
        correct_answer = correct_answer_list[k]

        font = pygame.font.Font(None, 45)
        A = font.render("A", True, WHITE)
        B = font.render("B", True, WHITE)
        C = font.render("C", True, WHITE)
        D = font.render("D", True, WHITE)
        screen.blit(A, [170, 410])
        screen.blit(B, [170, 470])
        screen.blit(C, [170, 530])
        screen.blit(D, [170, 590])

        for j in range (4):
            pygame.draw.rect(screen, answer_color, answer_boxes[j])
            text = pygame.font.Font(None, 36)
            text = text.render(answer_options[j], True, BLACK)
            screen.blit(text, [answer_boxes[j].x + 10, answer_boxes[j].y + 12])

        # waiting for user to answer
        answered = False
        while not answered:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    answered = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # answer valid or invalid?
                    (x, y) = event.pos
                    for i in range(4):
                        if answer_boxes[i].collidepoint(x, y):
                            if correct_answer == i:
                                points += 1
                            answered = True
            pygame.display.flip()

    pts = str(points)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running = False

            quiz_answer_bg = pygame.transform.scale(pygame.image.load("quiz-answer-bg.jpg"), (800, 650))
            screen.blit(quiz_answer_bg, [0, 0])
            
            other_text = pygame.font.Font(None, 36)
            other_text = other_text.render('You have guessed        out of 10 monuments correctly!' , True, WHITE)
            screen.blit(other_text, [97, 300])

            points_text = pygame.font.Font(None, 36)
            points_text = points_text.render(pts, True, WHITE)
            screen.blit(points_text, [322, 300])

            goto_menu_text = pygame.font.Font('freesansbold.ttf', 20)
            goto_menu_text = goto_menu_text.render('(Esc - MENU)', True, WHITE)
            screen.blit(goto_menu_text, (355, 360))

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu()

        pygame.display.flip()
    pygame.quit()

background = pygame.image.load('background.png')

#This music will be played continously in the background
mixer.music.load('background.wav')
# To play music in a loop
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Tank Turfs")
display_icon = pygame.image.load('003-tank-1.png')
pygame.display.set_icon(display_icon)

name = pygame.font.Font('freesansbold.ttf', 40)
name = name.render('Tank Turfs', True, (100, 255, 100))
screen.blit(name, (205, 600))

running = True

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
    menu()

    pygame.flip.display()

pygame.quit()