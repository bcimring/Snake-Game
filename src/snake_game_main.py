#########################################
# Name: Barry Cimring                   #
# Date: April 1, 2018                   #
# Description: snake.py                 #
#########################################

import pygame
pygame.init()

from random import randint
from time import perf_counter

height = 900
width = 1200

game_window = pygame.display.set_mode((width,height))

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
sandBeige = (249, 229, 148)
yellow = (255,255,0)
orange = (255,200,0)
grey = (100,100,100)
darkGrey = (50,50,50)

#-----------Text Fonts-------------------------------------------------------------------------#
gameOverFont = pygame.font.SysFont("Arial Black",170)
countFont = pygame.font.SysFont("Arial Black",60)   
gameFont= pygame.font.SysFont("Impact", 100)
ruleFont = pygame.font.SysFont("Arial Black", 35)

#-----------Text for ingame--------------------------------------------------------------------#
title = "Snake"
play = "Play"
introMessage = "Welcome to SNAKE"
ruleMessage = "Rules:"
rule1_text = "1. Use the arrow keys to move"
rule2_text = "2. Eat          to grow, if you eat 2 in 3 seconds, 4 seconds of"
rule2_cont = "extra time is rewarded"
rule3_text = "3. You are allergic to "
rule4_text = "4. Stay within the game borders"
rule5_text = "5.           are deadly predators!"

play_again = "Play Again"
play_stop = "Quit"
#------------Images----------------------------------------------------------------------------#
background = pygame.image.load("graphics/sand.jpg")
background = background.convert_alpha()
background = pygame.transform.scale(background,(1200,1100))

mouse = pygame.image.load("graphics/apple.png")
mouse = mouse.convert_alpha()
big_mouse = pygame.transform.scale(mouse,(100,100))
mouse = pygame.transform.scale(mouse,(40,40))

egg = pygame.image.load("graphics/rotten_apple.png")
egg = egg.convert_alpha()
big_rotten_egg = pygame.transform.scale(egg,(110,110))
egg = pygame.transform.scale(egg,(40,40))

hawk = pygame.image.load("graphics/hawk.png")
hawk = hawk.convert_alpha()
big_hawk = pygame.transform.scale(hawk,(100,80))
hawk = pygame.transform.scale(hawk,(40,40))
   
body = pygame.image.load("graphics/snakebody.png")
body = body.convert_alpha()
body = pygame.transform.scale(body,(40,40))

greenbody = pygame.image.load("graphics/snakebody_flashgreen.png")
greenbody = greenbody.convert_alpha()
greenbody = pygame.transform.scale(greenbody,(40,40))

redbody = pygame.image.load("graphics/snakebody_flashred.png")
redbody = redbody.convert_alpha()
redbody = pygame.transform.scale(redbody,(40,40))

tail = pygame.image.load("graphics/snaketail.png")
tail = tail.convert_alpha()
tail = pygame.transform.scale(tail,(40,40))

#-----------Sound------------------------------------------------------------------------------#
pygame.mixer.pre_init()
pygame.mixer.init()
pygame.mixer.music.load('audio/Mariachi.mp3')

#-----------Functions-------------------------------------------------------------------------#
#######################################
#    Function for intro screen        #
#######################################
def intro_screen():
    game_window.blit(background,(0,0))                      # draw background
    pygame.draw.rect(game_window,grey,(50,700,1100,150),5)  # draw button for play
    
    button = gameFont.render(play,1,black)                  # render play now
    intro = gameFont.render(introMessage,1,black)           # render rules and intro
    rules = gameFont.render(ruleMessage,1,black)            #
    rule_1 = ruleFont.render(rule1_text,1,black)            #
    rule_2 = ruleFont.render(rule2_text,1,black)            #
    rule_2_cont = ruleFont.render(rule2_cont,1,black)       #
    rule_3 = ruleFont.render(rule3_text,1,black)            #
    rule_4 = ruleFont.render(rule4_text,1,black)            #
    rule_5 = ruleFont.render(rule5_text,1,black)            #

    game_window.blit(intro,(200,50))                        # blit rules and text 
    game_window.blit(rules,(40,150))                        # and images of ingame items
    game_window.blit(rule_1,(40,270))                       #
    game_window.blit(rule_2,(40,340))                       #
    game_window.blit(big_mouse,(155,305))                   #
    game_window.blit(rule_2_cont,(85,395))                  #
    game_window.blit(rule_3,(40,450))                       #
    game_window.blit(big_rotten_egg,(450,435))              #
    game_window.blit(rule_4,(40,540))                       #
    game_window.blit(button,(500,710))                      # 
    game_window.blit(rule_5,(40,630))                       #
    game_window.blit(big_hawk,(90,600))                     #
    
    pygame.display.update()                                 # display on screen

#######################################
#   Function for difficulty screen    #
#######################################
def difficulty_screen():
    game_window.blit(background,(0,0))                      # draw background
    pygame.draw.rect(game_window,green,(50,50,1100,195))    # draw easy medium and hard rectangles
    pygame.draw.rect(game_window,yellow,(50,250,1100,195))  #
    pygame.draw.rect(game_window,orange,(50,450,1100,195))  #
    pygame.draw.rect(game_window,red,(50,650,1100,195))     #
    E = "Easy"                                              # text variables for buttons
    M = "Medium"                                            #
    H = "Hard"                                              #
    I = "Impossible"                                        #
    emh_font = pygame.font.SysFont("Times New Roman",190,True) # bolded font for buttons
    easy = emh_font.render(E,1,black)                       # renders text
    medium = emh_font.render(M,1,black)                     #
    hard = emh_font.render(H,1,black)                       #
    impossible = emh_font.render(I,1,black)                 #
    game_window.blit(easy,(375,30))                         # blit button text
    game_window.blit(medium,(230,250))                      #
    game_window.blit(hard,(355,450))                        #
    game_window.blit(impossible,(150,630))                  #
    
    pygame.display.update()                                 # display on screen

#######################################
#     Redrawing the whole board       #
#######################################
def redrawGameBoard(flashcolour = 0,snakeAttack = False):
    game_window.blit(background,(0,0))                                          # draw background
    pygame.draw.rect(game_window,sandBeige,(30,120,1140,750))                   # draw snake region
    for i in range((width-180)//30):                                            # for loops to draw
        pygame.draw.line(game_window,grey,(30,(i*30)+120),(1170,(i*30)+120),2)  # grid for snake
    for i in range(width//30):                                                  #
        pygame.draw.line(game_window,grey,(i*30,120),(i*30,870),2)              #

    game_window.blit(mouse,(mouse_x-5,mouse_y-5))                               # draws mouse
    for i in range(len(egg_x)):                                                 # for loop to draw
        game_window.blit(egg,(egg_x[i]-5,egg_y[i]-5))                           # rotten eggs
        
    #if snakeAttack == False:                                                   # if snake not being eaten
    if len(body_x) > 0:                                                         # if the snake's eaten a mouse already
        if flashcolour == 0:                                                    # if not flashing
            game_window.blit(tail,(body_x[-1]-5,body_y[-1]-5))                  # draw snake tail black
        if flashcolour == 'green':                                              # if flashing green
            game_window.blit(greenbody,(body_x[-1]-5,body_y[-1]-5))             # draw snake tail green
        if flashcolour == 'red':                                                # if flashing red
            game_window.blit(redbody,(body_x[-1]-5,body_y[-1]-5))               # draw snake tail red
                
    for i in range(len(body_x)-1):                                              # for loop to draw snake's body
        if flashcolour == 0:                                                    # same if statements above with snake tail
            game_window.blit(body,(body_x[i]-5,body_y[i]-5))                    #
        if flashcolour == 'green':                                              #
            game_window.blit(greenbody,(body_x[i]-5,body_y[i]-5))               #
        if flashcolour == 'red':                                                #
            game_window.blit(redbody,(body_x[i]-5,body_y[i]-5))                 #
            
    if snakeAttack == False:                                                    # if snake's not being eaten
        game_window.blit(head,(head_x-5,head_y-5))                              # draw snake head

    for i in range(len(hawk_x)):                                                # for loop to draw
        game_window.blit(hawk,(hawk_x[i]-5,hawk_y[i]-5))                        # hawk predators
    
    scoreCount = str(snakeLength)                                               # variables for snakelength, time
    timer = str(time)[:5]+" s"                                                  #
    score = gameFont.render(scoreCount,1,black)                                 # renders score and clock
    clock = gameFont.render(timer,1,black)                                      #
    header = gameFont.render(title,1,black)                                     #
    game_window.blit(score,(1100,0))                                            # blits score, clock, and large mouse
    game_window.blit(clock,(50,0))                                              #
    game_window.blit(header,(475,0))                                            #
    game_window.blit(big_mouse,(1000,0))                                        #
        
    pygame.display.update()                                                     # updates screen

#######################################
#       Intro Countdown               #
#######################################
def gameFieldIntro():
    three = "3"                                                                 # text variables for countdown
    two = "2"                                                                   #
    one = "1"                                                                   #
                                                                                #
    countDownFont = pygame.font.SysFont("Arial Black",150)                      # font for countdown
                                                                                #
    timer = countDownFont.render(three,1,black)                                 # renders text, displays count of three on screen
    game_window.blit(timer,(550,410))                                           #
    pygame.display.update()                                                     #
    pygame.time.delay(1000)                                                     # delay 1 second
                                                                                #
    redrawGameBoard()                                                           # redraws board, renders text, displays count of two on screen
    timer = countDownFont.render(two,1,black)                                   #
    game_window.blit(timer,(550,410))                                           #
    pygame.display.update()                                                     #
    pygame.time.delay(1000)                                                     # delays 1 second
                                                                                #
    redrawGameBoard()                                                           # redraws board
    timer = countDownFont.render(one,1,black)                                   # renders text, displays count of one on screen
    game_window.blit(timer,(550,410))                                           # 
    pygame.display.update()                                                     #
    pygame.time.delay(1000)                                                     # delays 1 second
    redrawGameBoard()                                                           # redraws board
    
#######################################
#       Snake flashing green          #
#######################################
def flashGreen(body_x,body_y,snakeLength,compensateTime):
    if len(body_x) >0:                          # if snake has already eaten a mouse
        body_x.append(body_x[-1]-speed_x*2)     # add body segment behind the snake the opposite way it is moving
        body_y.append(body_y[-1]-speed_y*2)     #
    else:                                       # if it has no length
        body_x.append(mouse_x-speed_x*2)        # add body segment behind the head of the snake
        body_y.append(mouse_y-speed_y*2)        #
        
    snakeLength += 1                            # add one to snakelength
    for i in range(2):                          # flash twice
        redrawGameBoard('green')                # draw snake green
        pygame.time.delay(200)                  # delay 0.2 secs
        redrawGameBoard()                       # draw snake black
        pygame.time.delay(200)                  # delay 0.2 secs
        
    compensateTime += 0.8                       # add 0.8 secs to compensate the delay
    return body_x,body_y,snakeLength,compensateTime

#######################################
#       Snake flashing red            #
#######################################
def flashRed(body_x,body_y,snakeLength,compensateTime):
    snakeLength -= 1                            # subtract 1 from snakelength
    body_x.pop()                                # remove last item from body list
    body_y.pop()                                #
    
    for i in range(2):                          # flash twice
        redrawGameBoard('red')                  # draw snake red
        pygame.time.delay(200)                  # delay 0.2 secs
        redrawGameBoard()                       # draw snake black
        pygame.time.delay(200)                  # delay 0.2 secs
        
    compensateTime += 0.8                       # add 0.8 secs to compensate the delay
    return body_x,body_y,snakeLength,compensateTime

#######################################
#     Function for checking keys      #
#######################################
def keyPressed(speed_x,speed_y,head):
    keys = pygame.key.get_pressed()                      # create T/F for all keys
    if keys[pygame.K_UP]:                                # if up is pressed
        if speed_y == 0 :                                # and snake is not moving in Y direction
            speed_y = -15                                # make snake move up
            if speed_x > 0:                              # if snake moxing to the right
                head = pygame.transform.rotate(head,90)  # rotate  head counterclockwise
            else:                                        # snake moving to the left
                head = pygame.transform.rotate(head,-90) # rotate head clockwise
            speed_x = 0                                  # snake stops moving in X direction

    if keys[pygame.K_DOWN]:                              # if down pressed
        if speed_y == 0 :                                # same as above, just change rotational direction and Y direction
            speed_y = 15                                 #
            if speed_x > 0:                              #
                head = pygame.transform.rotate(head,-90) #
            else:                                        #
                head = pygame.transform.rotate(head,90)  #
            speed_x = 0                                  #

    if keys[pygame.K_RIGHT]:                             # if right is pressed
        if speed_x == 0 :                                # if snake not moving in x direction
            speed_x = 15                                 # make snake move right
            if speed_y > 0:                              # if snake moves down
                head = pygame.transform.rotate(head,90)  # rotate counterclockwise
            else:                                        # if snake moves up
                head = pygame.transform.rotate(head,-90) # rotate counterclockwise
            speed_y = 0                                  # snake stops moving in Y direction
        
    if keys[pygame.K_LEFT]:                              # if left pressed
        if speed_x == 0 :                                # same as above, just change rotational direction and X direction
            speed_x = -15                                # 
            if speed_y > 0:                              #
                head = pygame.transform.rotate(head,-90) #
            else:                                        #
                head = pygame.transform.rotate(head,90)  #
            speed_y = 0                                  #

    return speed_x,speed_y,head
    
#######################################
#    Function for spawning a apple    #
#######################################
def spawnMouse():
    mouse_x = randint(2,(1110//30))*30  # spawn mouse at random location on the gridlines
    mouse_y = randint(5,(810//30))*30   # 
    return mouse_x,mouse_y

#######################################
#    Function for eating an apple     #
#######################################
def mouseEat(head_y,head_x,mouse_y,mouse_x,body_x,body_y,snakeLength,egg_x,egg_y,hawk_x,hawk_y,time1,time2,compensateTime):
    if (head_y == mouse_y) and (mouse_x == head_x): # if snake head hits mouse, flash green
        body_x,body_y,snakeLength,compensateTime = flashGreen(body_x,body_y,snakeLength,compensateTime)
        #munch.play()                                # play munch sound
        
        if snakeLength%2 == 1:                      # if snake at an odd number
            time1 = perf_counter()                  # record time of mouse eaten
        elif snakeLength%2 == 0:                    # if snake at an even num
            time2 = perf_counter()                  # record time of mouce eaten
        if snakeLength > 1:                         # if the snake has eaten 2 mice already
            if abs(time1-time2) < 3:                # if time difference is less than 3
                compensateTime += 4                 # compesate time with 5 seconds
            
        while True:
            mouse_x,mouse_y = spawnMouse()          # spawn new mouse and make sure it is not is a spot with an egg or hawk
            if (egg_x.count(mouse_x) == 0) and (egg_x.count(mouse_y) == 0) and (hawk_x.count(mouse_x) == 0) and (hawk_y.count(mouse_y) == 0):
                break

        # spawn potential egg or hawk (depends on snakelength)
        egg_x,egg_y = spawnRottenEgg(snakeLength,egg_x,egg_y,mouse_x,mouse_y, hawk_x,hawk_y)
        hawk_x,hawk_y = spawnhawk(snakeLength,egg_x,egg_y,mouse_x,mouse_y,hawk_x,hawk_y)
        
    return mouse_y,mouse_x,body_x,body_y,snakeLength,egg_x,egg_y,hawk_x,hawk_y,time1,time2,compensateTime

#######################################
#    Function for spawning an egg     #
#######################################
def spawnRottenEgg(snakeLength,egg_x,egg_y,mouse_x,mouse_y, hawk_x,hawk_y):
    if str(snakeLength/2)[-1] == '0':                           # if snakelength is a multiple of 2
        while True:                             
            obstx = (randint(1,(1140//30))*30)                  # choose integers on gridlines
            obsty = (randint(4,(840//30))*30)                   # \/ if new egg is not at a hawk or mouse
            if (obstx != mouse_x) and (obsty != mouse_y) and (hawk_x.count(obstx)==0) and (hawk_y.count(obsty) == 0):    
                egg_x.append(obstx)                             # add egg coords to egg list
                egg_y.append(obsty)                             #
                break                                           # break loop
    return egg_x,egg_y

#######################################
#   Function for spawning an hawk    #
#######################################
def spawnhawk(snakeLength,egg_x,egg_y,mouse_x,mouse_y,hawk_x,hawk_y):
    if snakeLength > 0:                                         # if snakelength is greater than 0
        if str(snakeLength/5)[-1] == '0':                       # if snakelength at multiple of 5
            while True:                                         #
                dangx = (randint(1,(1140//30))*30)              # choose coord integer on gridlines
                dangy = (randint(4,(840//30))*30)               # \/ if new hwak is not at egg or mouse
                if (dangx != mouse_x) and (dangy != mouse_y) and (egg_x.count(dangx)==0) and (egg_y.count(dangy) == 0):
                    hawk_x.append(dangx)                        # add hawk coords to hawk list
                    hawk_y.append(dangy)                        #
                    break                                       # break loop

    return hawk_x,hawk_y

#######################################
#  Function for controlling borders   #
#######################################
def borderControl(head_x,speed_x,head_y,speed_y,gameOn):
    if 149 < head_y :            # if snake is lower than top of grid
        head_y += speed_y        # add speed to snake Y
    else:                        # if snake higher than top of grid
        gameOn = False           # turn game off
        
    if 841 > head_y:             # if snake higher than bottom of grid
        head_y += speed_y        # add speed to snake Y
    else:                        # if lower than bottom
        gameOn = False           # turn game off
        
    if 59 < head_x:              # if snake to the right of left border
        head_x += speed_x        # add speed to snake X  
    else:                        # if left of left-border
        gameOn = False           # turn game off
        
    if 1141 > head_x:            # if snake to the left of right border
        head_x += speed_x        # add speed to snake X
    else:                        # if right of right-border
        gameOn = False           # turn game off
        
    return gameOn,head_x,head_y

#######################################
# Function for the snake being eaten  #
#######################################
def eatenSnake():
    for i in range(len(body_x)): # for loop size of snake body
        redrawGameBoard(0,True)  # draw snake without head
        body_x.pop(-1)           # remove last item of snake body
        body_y.pop(-1)           #
        pygame.time.delay(200)   # delay 0.2 secs
    
#######################################
#  Function for the game over screen  #
#######################################
def gameOverScreen():
    message = "Game Over!"                                  # game over and score text  
    count = "Score: "+str(snakeLength)                      #
    conclude = gameOverFont.render(message,1,black)         # render text and button text
    counter = countFont.render(count,1,black)               #
    keepPlaying = gameFont.render(play_again,1,black)       #
    stopPlaying = gameFont.render(play_stop,1,black)        #
    game_window.blit(conclude,(50,300))                     # blit game over, score and buttons
    game_window.blit(counter,(450,550))                     #
    game_window.blit(keepPlaying,(90, 710))                 #
    game_window.blit(stopPlaying,(800,710))                 #

    pygame.draw.rect(game_window,grey,(50,700,500,150),20)  # draw buttons
    pygame.draw.rect(game_window,grey,(650,700,500,150),20) # 

    pygame.display.update()                                 # display on screen
#-------------------------------------------------------------------------------------#
    
#Main
introScreen = True
while introScreen:                                                  # while loop for intro screen
    intro_screen()                                                  #
    cursor_x,cursor_y = pygame.mouse.get_pos()                      # gets position of mouse
    for event in pygame.event.get():                                #
        if event.type == pygame.MOUSEBUTTONDOWN:                    # if mouse clicked
            if (50 < cursor_x < 1150) and (700 < cursor_y <850 ):   # and touching play button
                introScreen = False                                 # break loop
                                                                    #
keepPlaying = True                                                  # while loop for game and outro
while keepPlaying:                                                  #
    #----------Snake properties-------------------------------------#
    speed_x = 15                                                    # intial speed to the right
    speed_y = 0                                                     #
    head_x = 300                                                    # intital position of snake mid left of center screen
    head_y = 450                                                    #
    snakeLength = 0                                                 # intital snake is only head
    body_x = list()                                                 # lists for snakebody, eggs, and eagles coords
    body_y = list()                                                 #
    egg_x = list()                                                  #
    egg_y = list()                                                  #
    hawk_x = list()                                                 #
    hawk_y = list()                                                 #
                                                                    #
    time1 = 0                                                       # time differences to test mouse eaten intervals
    time2 = 120                                                     #
    compensateTime = 0                                              # compensate time variable for delays
                                                                    #
    head = pygame.image.load("graphics/snakehead.png")                       # load snakehead looking to the right
    head = head.convert_alpha()                                     #
    head = pygame.transform.scale(head,(40,40))                     #
    head = pygame.transform.rotate(head,90)                         #
                                                                    #
    difficultyScreen = False                                        #
    while not difficultyScreen:                                     # while loop for difficulty screen
        difficulty_screen()                                         # call difficulty screen function
        cursor_x,cursor_y = pygame.mouse.get_pos()                  # gets position of mouse
        for event in pygame.event.get():                            #
            if event.type == pygame.MOUSEBUTTONDOWN:                # if mouse clicked and between one of the boxes
                    if (50 < cursor_x < 1150) and (50 < cursor_y < 245):
                        difficulty = 65                             # easy delay
                        difficultyScreen = True                     # exit difficulty screen
                    if (50 < cursor_x <1150) and (250 < cursor_y < 445):
                        difficulty = 50                             # medium delay
                        difficultyScreen = True                     # exit difficulty screen
                    if (50 < cursor_x <1150) and (450 < cursor_y < 645):
                        difficulty = 35                             # hard delay
                        difficultyScreen = True                     # exit difficulty screen
                    if (50 < cursor_x <1150) and (650 < cursor_y < 850):
                        difficulty = 20                             # impossible delay
                        difficultyScreen = True                     # exit difficulty screen
                                                                    #
    mouse_x,mouse_y = spawnMouse()                                  # chooses intital mouse spot
    time = '30'                                                     # time for start screen
    redrawGameBoard()                                               # draws board
    gameFieldIntro()                                                # counts down from 3
    timeCorrect = perf_counter()                                    # timecorrect at time of the start of game
    snakeAttack = False                                             # snake attack variable
    gameOn = True                                                   #
    #pygame.mixer.music.play(-1,2.0)                                     # start playing music when game begins
                                                                    #
    while gameOn:                                                   # while loop for playing game
        for event in pygame.event.get():                            # if game is closed
            if event.type == pygame.QUIT:                           #
                gameOn = False                                      # exit game
                keepPlaying = False                                 #
                                                                    #
        delay = difficulty                                          # makes difficulty placeholder variable
        for i in range(0,snakeLength,2):                            # for range of every 2 snakelengths
            delay -=1                                               # make delay less 1
                                                                    #
        speed_x,speed_y,head = keyPressed(speed_x,speed_y,head)     # checks if keys are pressed
                                                                    #
        #-Check  and set time---------------------------------------#
        time = 30 + compensateTime - perf_counter() + timeCorrect   # time counts down from 30 and adds a time correction
                                                                    #
        if time <= 0:                                               # if time hits 0
            time = 0                                                # draw gameboard with 0 time and exit game
            redrawGameBoard()                                       #
            gameOn = False                                          #
                                                                    #
        # Checks if snake head eats a bad apple --------------------#
        for i in range(len(egg_x)):                                 # for loop for all eggs
            if (head_y == egg_y[i]) and (head_x == egg_x[i]):       # if snake hits egg
                #fart.play()                                        # play fart noise and flash red
                body_x,body_y,snakeLength,compensateTime = flashRed(body_x,body_y,snakeLength,compensateTime)
                egg_x.pop(i)                                        # remove last snake item
                egg_y.pop(i)                                        #
                break                                               # break loop 
        for i in range(len(hawk_x)):                                # for loop for all hawks
            if (head_y == hawk_y[i]) and (head_x == hawk_x[i]):     # if snake hits hawk
                #hawk.play()                                        # play snake noise
                pygame.time.delay(200)                              # pause 0.2 sec
                snakeAttack = True                                  # snake attack true and exits game
                gameOn = False                                      #
                                                                    #
        # Check if blocks are touching -----------------------------#
        for i in range(len(body_x)-1):                              # for loop in range of all blocks
            if ((head_x == body_x[i]) and (head_y == body_y[i])) and ((head_y != mouse_y) and (mouse_x != head_x)):
                gameOn = False                                      # if head touches body exit game
                                                                    #
        #-Checks if snake is at border of game----------------------#
        gameOn,head_x,head_y = borderControl(head_x,speed_x,head_y,speed_y,gameOn)
                                                                    #
        # Makes blocks have previous location ----------------------#
        if len(body_x) > 1:                                         # if snake has eaten 2 mice already
            for i in range(len(body_x)-1,0,-1):                     # for loop in range of body from end to start 
                body_x[i] = body_x[i-1]                             # make the snake body in place of the last one
            for i in range(len(body_y)-1,0,-1):                     # 
                body_y[i] = body_y[i-1]                             #
                                                                    #
        # Gives first addition block location ----------------------#
        if len(body_x) > 0:                                         # if snake has eaten an item
            body_x[0] = head_x - speed_x*2                          # make first body segement the head previous head position
            body_y[0] = head_y - speed_y*2                          #
                                                                    #
        #---mouse eat function--------------------------------------#
        mouse_y,mouse_x,body_x,body_y,snakeLength,egg_x,egg_y,hawk_x,hawk_y,time1,time2,compensateTime = mouseEat(head_y,head_x,mouse_y,mouse_x,body_x,body_y,snakeLength,egg_x,egg_y,hawk_x,hawk_y,time1,time2,compensateTime)
                                                                    #
        #-----------------------------------------------------------#
        if gameOn == False:                                         # checks if game is off
            break                                                   # 
        redrawGameBoard(0)                                          # redraws board with snake black
        pygame.time.delay(delay)                                    # delays game by difficulty
                                                                    #
    pygame.mixer.music.stop()                                       #
    if snakeAttack == True:                                         # if snake attack is true play animation
            eatenSnake()                                            #
                                                                    #
    if keepPlaying == True:                                             #
        while not gameOn:                                               # while game is not being played in game loop
            gameOverScreen()                                            # shows game over screen
            for event in pygame.event.get():                            #
                cursor_x,cursor_y = pygame.mouse.get_pos()              # gets position of mouse
                if event.type == pygame.MOUSEBUTTONDOWN:                # if mouse is clicked
                    if (50 < cursor_x < 550) and (700 < cursor_y <850): # if play again is clicked
                        gameOn = True                                   # exit this loop and play again
                        break                                           # breaks for loop
                    elif (650 < cursor_x < 1150) and (700 < cursor_y <850): # if quit is clicked
                        keepPlaying = False                             # stops playing game again
                        gameOn = True                                   # exits loop and quits
                        break                                           # breaks for loop
pygame.quit()                                                           # quit game when finished
    
