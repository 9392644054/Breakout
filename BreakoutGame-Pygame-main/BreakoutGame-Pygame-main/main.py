import math
import time
import pygame
import random

# initialize the pygame
pygame.init()

# screen dimensions configuration
width = 626
height = 417
screen = pygame.display.set_mode((width, height))

# set caption and icon
pygame.display.set_caption('Block Game')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# game background music
pygame.mixer.music.load('hip-hop-red-alert-redux-14092.mp3')
pygame.mixer.music.play(-1)

# load background image
bgImage = pygame.image.load('background.png')

# blocks
blockWidth = 50
blockHeight = 20
blockColors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 165, 0),  # Orange
    (128, 0, 128),  # Purple
    (255, 192, 203),  # Pink
    (0, 255, 255),  # Cyan
    (165, 42, 42),  # Brown
    (255, 255, 255),  # White
]


# get blocks
def getBlocks(blockWidth, blockHeight, blockColors):
    blocks = []
    for x in range(51, 564, blockWidth + 3):
        for y in range(30, 191, 40):
            color = blockColors[random.randint(0, len(blockColors) - 1)]
            block = {'color': color, 'x': x, 'y': y, 'width': blockWidth, 'height': blockHeight}
            blocks.append(block)
    return blocks


blocks = getBlocks(blockWidth, blockHeight, blockColors)

# paddle
paddleX = (width - 100) // 2
paddleY = 370
paddleWidth = 100
paddleHeight = 20

# ball
ballSize = 16
ballX = paddleX + paddleWidth // 2 - ballSize // 2
ballY = paddleY - ballSize
ballImage = pygame.image.load('ball.png')
ballAngle = 60
ballDir = "top-right"

# gameover
gameover = False
gameoverFont = pygame.font.Font('MonomaniacOne-Regular.ttf', 64)


# set background
def setBackground():
    screen.blit(bgImage, (0, 0))


# set blocks
def showBlocks(blocks):
    for block in blocks:
        pygame.draw.rect(screen, block['color'], (block['x'], block['y'], block['width'], block['height']),
                         border_radius=3)


# show paddle
def showPaddle(x, y, width, height):
    pygame.draw.rect(screen, (92, 240, 12), (x, y, width, height), border_radius=20)


# display ball
def displayBall(x, y):
    screen.blit(ballImage, (x, y))


# display gameover
def displayGameover():
    gameoverSurface = gameoverFont.render("Game Over", True, (255, 255, 0))
    screen.blit(gameoverSurface, (185, 100))


# game loop
while not gameover:
    setBackground()

    # events handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                paddleX += (paddleWidth // 2)
            if event.key == pygame.K_LEFT:
                paddleX -= (paddleWidth // 2)

    # paddle movement
    if paddleX > (width - paddleWidth - 13):
        paddleX = width - paddleWidth
    if paddleX < 13:
        paddleX = 0

    # ball movement
    if ballDir == "top-right":
        ballX += 1
        ballY -= math.floor(math.tan(math.radians(ballAngle)))
    if ballDir == "top-left":
        ballX -= 2
        ballY -= math.floor(2 / math.tan(math.radians(ballAngle)))
    if ballDir == "bottom-left":
        ballX -= 1
        ballY += math.floor(math.tan(math.radians(ballAngle)))
    if ballDir == "bottom-right":
        ballX += 2
        ballY += math.floor(2 / math.tan(math.radians(ballAngle)))

    # handle ball directions when paddle hits
    if ballX >= (width - ballSize):
        ballDir = "top-left" if ballDir == "top-right" else "bottom-left"
    if ballY <= ballSize:
        ballDir = "bottom-left" if ballDir == "top-left" else "bottom-right"
    if ballX <= ballSize:
        ballDir = "bottom-right" if ballDir == "bottom-left" else "top-right"
    if ballY >= (paddleY - ballSize):
        if paddleX <= ballX <= (paddleX + 20):
            ballDir = "top-left"
        if (paddleX + 20) <= ballX <= (paddleX + paddleWidth - ballSize - 20):
            ballDir = "top-right" if ballDir == "bottom-right" else "top-left"
        if (paddleX + paddleWidth - ballSize - 20) <= ballX <= (paddleX + paddleWidth - 2):
            ballDir = "top-right"

    # when ball falls down
    if ballY >= (height - ballSize):
        gameover = True

    # handle ball directions when it hits a block
    for block in blocks:
        x, y = block['x'], block['y']
        collided = False
        if ballDir == "top-right":
            if (x - ballSize) <= ballX <= (x - ballSize + 1) and (y - ballSize) <= ballY <= (y + blockHeight):
                ballDir = "top-left"
                collided = True
            if (x - ballSize + 1) < ballX <= (x + blockWidth) and (y - ballSize) <= ballY <= (y + blockHeight):
                ballDir = "bottom-right"
                collided = True
        elif ballDir == "top-left":
            if (x + blockWidth - 1) <= ballX <= (x + blockWidth) and (y - ballSize) <= ballY <= (y + blockHeight):
                ballDir = "top-right"
                collided = True
            if x < ballX <= (x + blockWidth - 1) and (y - ballSize) <= ballY <= (y + blockHeight):
                ballDir = "bottom-left"
                collided = True
        elif ballDir == "bottom-left":
            if (x + blockWidth - 1) <= ballX <= (x + blockWidth) and (y - ballSize) <= ballY <= (y + blockHeight):
                ballDir = "bottom-right"
                collided = True
            if x < ballX <= (x + blockWidth - 1) and (y - ballSize) <= ballY <= (y + blockHeight):
                ballDir = "top-left"
                collided = True
        else:
            if (x - ballSize) <= ballX <= (x - ballSize + 1) and (y - ballSize) <= ballY <= (y + blockHeight):
                ballDir = "bottom-left"
                collided = True
            if x < ballX <= (x + blockWidth - 1) and (y - ballSize) <= ballY <= (y + blockHeight):
                ballDir = "top-right"
                collided = True
        if collided:
            pygame.mixer.Sound('mixkit-basketball-ball-hard-hit-2093.wav').play()
            blocks.remove(block)
            break
    # display blocks, paddle
    showBlocks(blocks)
    showPaddle(paddleX, paddleY, paddleWidth, paddleHeight)
    displayBall(ballX, ballY)

    if gameover:
        pygame.mixer.music.stop()
        displayGameover()
        pygame.display.update()
        pygame.mixer.Sound('gameoverSound.mp3').play()
        time.sleep(2)
    pygame.display.update()
    time.sleep(0.01)
