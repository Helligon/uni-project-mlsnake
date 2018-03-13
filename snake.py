import pygame
import random
from pygame.locals import *

displayWidth = 640
displayHeight = 640
fps = 10
blockSize = 10
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (160,214,180)

pygame.init()

clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 20)

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
pygame.display.set_caption("Snake Time!")


def messageToScreen(text, colour, yDisplace = 0):

    textSurface = font.render(text, True, colour)
    textBox = textSurface.get_rect()
    textBox.center = (displayWidth/2, displayHeight/2 - yDisplace)

    gameDisplay.blit(textSurface, textBox)


def drawSegment(colour, x, y, blockSize):

    pygame.draw.rect(gameDisplay, colour, [x, y, blockSize, blockSize])


def drawSnake(blockSize, snakeList):
    for segmentPos in snakeList:
        drawSegment(green, segmentPos[0], segmentPos[1], blockSize)


def gameLoop():

    score = 0
    headX = displayWidth/2
    headY = displayHeight/2
    headXChange = 0
    headYChange = 0
    gameExit = False
    gameOver = False
    snakeList = []
    snakeLength = 5

    appleX = random.randrange(0, (displayWidth-blockSize)/10)*10
    appleY = random.randrange(0, (displayWidth-blockSize)/10)*10

    while not gameExit:

        while gameOver:
            messageToScreen("Game Over...", red, 0)
            messageToScreen("Press SPACE to play again or Q to quit.", red, -20)
            messageToScreen("Score:  " + str(score), green, 20)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    gameOver = False
                    gameExit = True
                elif event.type == KEYDOWN:
                    if event.key == K_q:
                        gameExit = True
                        gameOver = False
                    elif event.key == K_SPACE:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == QUIT:
                gameExit = True
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    headYChange = -blockSize
                    headXChange = 0
                elif event.key == K_DOWN:
                    headYChange = blockSize
                    headXChange = 0
                elif event.key == K_RIGHT:
                    headYChange = 0
                    headXChange = blockSize
                elif event.key == K_LEFT:
                    headYChange = 0
                    headXChange = -blockSize

        if headX >= displayWidth or headY >= displayHeight or headX <= 0 or headY <= 0:
            gameOver = True

        headX += headXChange
        headY += headYChange

        gameDisplay.fill(black)

        drawSegment(red, appleX, appleY, blockSize)

        snakeHead = []

        snakeHead.append(headX)
        snakeHead.append(headY)

        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        drawSnake(blockSize, snakeList)

        pygame.display.update()

        if headX == appleX and headY == appleY:
            appleX = random.randrange(0, (displayWidth - blockSize) / 10) * 10
            appleY = random.randrange(0, (displayWidth - blockSize) / 10) * 10
            snakeLength += 1
            score += 1

        clock.tick(fps)

    pygame.quit()
    quit()

gameLoop()
