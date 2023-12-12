# final project: Breakout


# Each part of the game that needs to be done:

# create the game loop

# create the game window

# create the bricks

# create the paddle

# get the paddle to move

# create the ball

# get the ball to move

# figure out how to make ball collide with walls

# ball collide with paddle

# ball collide with bricks

# ball initiates game over

# create game over for both win and lose

# reset the game

# put text on the screen



import pygame
from pygame.locals import *
pygame.init()

# Sound:
pygame.mixer.init()
pygame.mixer.music.load('breakout.mp3')
pygame.mixer.music.play(-1)
endSound = pygame.mixer.Sound("gameOver.mp3")
hit = pygame.mixer.Sound("hit.mp3")


# Setting the game window:

screenW = 800
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("Breakout")


font = pygame.font.SysFont("Comic Sans", 30)

# These are varriables that set the colors for the game:
backgroundColor = (217, 217, 217)
blackBrick = (0,0,0)
darkGrayBrick = (60, 60, 60)
lighterGrayBrick = (110, 110, 110)
lighestGrayBrick = (140, 140, 140)
paddleColor = (80, 80, 240)
paddleOColor = (100, 100, 250)
textColor = (0,0,0)

# variables
columns = 6
rows = 8
clock = pygame.time.Clock()
fps = 60 # to make sure that they are moving at the correct speed
ballIsMoving = False
game_over = 0


# this code writes the text on the screen (because you cannot write directly on screen)

def writeText(text, font, textColor, x, y):
    img = font.render(text, True, textColor)
    screen.blit(img, (x,y))




# this class creates the wall of bricks
class wall():
    def __init__(self): # "self" represents the instance of the class
        self.width = screenW // columns # divide by the number of columns to ensure that the bricks are spaced out evenly
        self.height = 40 # sets the height of the brick
    # this creates the wall of bricks
    def create_wall(self):
        
        self.bricks = [] # this is an empty lisk for the bricks
        # this creates an empty list for each individual brick
        individualBrick = []
        for row in range(rows):
            # resets the brick row list
            brickRow = []
            # iterate through each column in that row
            for col in range(columns):
                # this code creates x and y positions usign the height and width for each block and creates a rectangle from that
                brickX = col * self.width
                brickY = row * self.height
                rect = pygame.Rect(brickX, brickY, self.width, self.height) # creates the rectangle (the brick)
                # this assigns each brick in a certain row their "strength" based on what row they are in:
                if row < 2:
                    strength = 4
                elif row < 4:
                    strength = 3
                elif row < 6:
                    strength = 2
                elif row <8:
                    strength = 1
                    
                # this list is used to store the rectangle data and the colors
                individualBrick = [rect, strength]
                # append that individual brick to the brick row
                brickRow.append(individualBrick)
            # append the row of bricks to the full list of bricks in order to get all of the bricks
            self.bricks.append(brickRow)

    def makeWall(self):
        for row in self.bricks:
            for brick in row:
                # based on what row the bricks are in, which we can tell from the brick "strength," we can assign them a color:
                if brick[1] == 4: # use brick[1] (index 1) because thats where the strength was stored
                    brickColor = lighestGrayBrick
                elif brick[1] == 3:
                    brickColor = lighterGrayBrick
                elif brick[1] == 2:
                    brickColor = darkGrayBrick
                elif brick[1] == 1:
                    brickColor = blackBrick
                pygame.draw.rect(screen, brickColor, brick[0])
                pygame.draw.rect(screen, backgroundColor, (brick[0]), 2)


                
#create the paddle class:        
class paddle():
    def __init__(self):
        self.reset()
    

    def move(self):
        # reset the direction in which the paddle moves:
        self.direction = 0
        key = pygame.key.get_pressed()

        #left press:
        if key[pygame.K_LEFT] and self.rect.left >0: # this code is saying that when the left key is pressed, the paddle moves left.
            self.rect.x -= self.speed # set the x coordinate to the neg value to go left
            self.direction  = -1 # tells what direction it is in

        #right press:
        if key[pygame.K_RIGHT] and self.rect.right < screenW:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self): # draws the paddle onto the screen
        pygame.draw.rect(screen, paddleColor, self.rect)
        pygame.draw.rect(screen, paddleOColor, self.rect, 3)

        
    def reset(self):
         # the paddle variables:
        self.height = 20
        self.width = int(screenW / columns) # makes sure it is even with everything else
        self.x = int((screenW/2) - (self.width/2))
        self.y = screenH - (self.height *2)
        self.speed = 10
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
        

# ball class
class gameBall():
    playSound = True

    # initializes
    def __init__(self,x,y):
        self.reset(x,y)
        self.hitNum = 0

    def move(self):

        
        # collision threshold

        
        threshold = 5

        # set the wall that it was destroyed
        wallWasBroken = 1
        row_count = 0

        
        for row in wall.bricks:
            item_count = 0
            for item in row:


                
                # check to see if there was a collision with the ball and an object/wall



                if self.rect.colliderect(item[0]):


                    # check if it was hit on left
                    if abs(self.rect.right - item[0].left) < threshold and self.speedX > 0:
                        self.speedX *= -1
                        hit.play()

                        
                    # hit on right
                    if abs(self.rect.left - item[0].right) < threshold and self.speedX < 0:
                        self.speedX *= -1
                        hit.play()


                    # hit above:
                    if abs(self.rect.bottom - item[0].top) < threshold and self.speedY > 0:
                        self.speedY *= -1
                        hit.play()



                    # hit below:
                    if abs(self.rect.top - item[0].bottom) < threshold and self.speedY < 0:
                        self.speedY *= -1
                        hit.play()



                   

                    # when the brick is hit, reduce its (strength)
                    if wall.bricks[row_count][item_count][1] > 1:
                        wall.bricks[row_count][item_count][1] -= 1


                    # this says the brick is gone, and that it was completely hit and has no strength left
                    else:
                        wall.bricks[row_count][item_count][0] = (0, 0, 0, 0)






                # check if block still exists, in which case the wall is not destroyed
                if wall.bricks[row_count][item_count][0] != (0, 0, 0, 0):




                    wallWasBroken = 0
                    #iterate through bricks
                    
                # increase item counter
                item_count += 1

            # increase row counter
            row_count += 1

        # this checks to see if all the bricks were destroyed. if they were game is over
        if wallWasBroken == 1:
            self.game_over = 1




        # check for collision with walls
        if self.rect.left < 0 or self.rect.right > screenW: #if it goes right more that width, switch direction, if goes all the way to zero, switch direction
            self.speedX *= -1


            

        # check for collision with top and bottom of the screen
        if self.rect.top < 0:
            self.speedY *= -1
        if self.rect.bottom > screenH:
            self.game_over = -1



            

        # look for collision with paddle
        
        if self.rect.colliderect(player):



            
            # see if its hitting the top of the paddle
            
            if abs(self.rect.bottom - player.rect.top) < threshold and self.speedY > 0:
                self.speedY *= -1
                self.speedX += player.direction
                if self.speedX > self.speedMax:
                    self.speedX = self.speedMax
                elif self.speedX < 0 and self.speedX < -self.speedMax:
                    self.speedX = -self.speedMax
                self.hitNum +=1

            else:
                self.speedX *= -1
        
        


        self.rect.x += self.speedX
        self.rect.y += self.speedY

        return self.game_over
        return hit_counter
    

    def draw(self):
        # this creates a circle using pygame and all of its attributes
        
        pygame.draw.circle(screen, paddleColor, (self.rect.x + self.ballRadius, self.rect.y + self.ballRadius), self.ballRadius)
        pygame.draw.circle(screen, paddleOColor, (self.rect.x + self.ballRadius, self.rect.y + self.ballRadius), self.ballRadius, 3)


    #reset the game ball when the game needs reset
    def reset(self, x, y):
        self.ballRadius = 10
        self.x = x- self.ballRadius
        self.y = y
        self.rect = Rect(self.x, self.y, self.ballRadius * 2, self.ballRadius * 2)
        self.speedX = 4
        self.speedY = -4
        self.speedMax = 5
        self.game_over = 0




# make the wall of bricks
wall = wall()
wall.create_wall()


# make the paddle
player = paddle()


# make the ball
ball = gameBall(player.x + (player.width // 2), player.y - player.height)



run = True
paused = False



# the game loop:
while run:
    
    stopSound = True

    #how fast its running:
    clock.tick(fps)


    

    #set the background color
    screen.fill(backgroundColor)


    # make the objects --> has to be after setting background
    wall.makeWall()
    player.draw()
    ball.draw()

    

    
    
    
    # checks to see if the game is still in play and hasnt been won or lost
    if ballIsMoving and not paused :
        
        
        player.move()

        game_over = ball.move()
        if game_over != 0:
            ballIsMoving = False

    #player ints


    # these are the different conditions on why the game is over:
    
    if not ballIsMoving:

        #this is the first game
        if game_over == 0:
            writeText("Click Anywhere to Start Playing!", font, textColor, 175, screenH//2 + 100)

        #the player won the game
        #set all the colors on scree to green for win
        elif game_over == 1:
            backgroundColor = (0,200,0)
            blackBrick = (0,200,0)
            darkGrayBrick = (0,200,0)
            lighterGrayBrick = (0,200,0)
            lighestGrayBrick = (0,200,0)
            paddleColor = (0,200,0)
            paddleOColor = (0,200,0)
            writeText("You Won the Game!", font, textColor, 275, screenH//2 + 25)
            writeText("To Play Again, Click Anywhere!", font, textColor, 175, screenH//2 + 100)


        #the player lost the game
        #set all the colors on scree to red for lost
        #stop the game background music
        elif game_over == -1:
            backgroundColor = (200, 0, 0)
            blackBrick = (200, 0, 0)
            darkGrayBrick = (200, 0, 0)
            lighterGrayBrick = (200, 0, 0)
            lighestGrayBrick = (200, 0, 0)
            paddleColor = (200, 0, 0)
            paddleOColor = (200, 0, 0)
            """
            I want to try to get rid of all of the bricks
            """
            pygame.mixer.music.stop() #stop the game background music
            
    
            writeText("You Lost the Game!", font, textColor, 275, screenH//2 - 50 )
            writeText("To Play Again, Click Anywhere on the Screen!", font, textColor, 100, screenH//2 + 25)

            
    
    
     

    for event in pygame.event.get():


        # quits window when x is pressed
        if event.type == pygame.QUIT:
            run = False


        #starts the game with a click
        if event.type == pygame.MOUSEBUTTONDOWN and ballIsMoving == False:
            ballIsMoving = True
            pygame.mixer.music.load('breakout.mp3')
            pygame.mixer.music.play(-1) # puts the music back on


            #sets all the colors back to correct color:
            backgroundColor = (217, 217, 217)
            blackBrick = (0,0,0)
            darkGrayBrick = (60, 60, 60)
            lighterGrayBrick = (110, 110, 110)
            lighestGrayBrick = (140, 140, 140)
            paddleColor = (80, 80, 240)
            paddleOColor = (100, 100, 250)
            textColor = (0,0,0)


            # reset the ball
            ball.reset(player.x + (player.width // 2), player.y - player.height)
            player.reset()
            wall.create_wall()

        # here is where i tried to implement a pause function
        if event.type == pygame.K_p:
            paused == True
        if event.type == pygame.K_u:
            paused = False
            


    #continuously updates the screen
    pygame.display.update()

pygame.quit()

