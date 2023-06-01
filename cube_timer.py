import pygame
import time
import Stoper

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 130, 0)
BACKGROUND_COLOUR = (80, 80, 120)

WIN_WIDTH = 400
WIN_HEIGHT = 600

USER_TIMES_HISTORY = []

def addTimeToTimesHistory(value):
    USER_TIMES_HISTORY.append(value)

def deleteTimeFromTimesHistory():
    USER_TIMES_HISTORY.pop(-1)

def clearTimesHistory():
    USER_TIMES_HISTORY.clear()

def getBestTimeFromTimesHistory():
    if len(USER_TIMES_HISTORY) > 0:
        return min(USER_TIMES_HISTORY)
    else:
        return -1

def getUpToFiveLastTimesFromTimesHistory():
    if len(USER_TIMES_HISTORY) == 0:
        return -1
    elif len(USER_TIMES_HISTORY) < 6:
        return USER_TIMES_HISTORY[:]
    else:
        return USER_TIMES_HISTORY[-5:]

pygame.init()
gameWindow = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

def drawCubeGraphic(xpos, ypos):
    pygame.draw.rect(gameWindow, GREEN, pygame.Rect(xpos+0, ypos+0, 30, 30))
    pygame.draw.rect(gameWindow, YELLOW, pygame.Rect(xpos+30, ypos+0, 30, 30))
    pygame.draw.rect(gameWindow, GREEN, pygame.Rect(xpos+60, ypos+0, 30, 30))
    pygame.draw.rect(gameWindow, RED, pygame.Rect(xpos+0, ypos+30, 30, 30))
    pygame.draw.rect(gameWindow, WHITE, pygame.Rect(xpos+30, ypos+30, 30, 30))
    pygame.draw.rect(gameWindow, BLUE, pygame.Rect(xpos+60, ypos+30, 30, 30))
    pygame.draw.rect(gameWindow, ORANGE, pygame.Rect(xpos+0, ypos+60, 30, 30))
    pygame.draw.rect(gameWindow, GREEN, pygame.Rect(xpos+30, ypos+60, 30, 30))
    pygame.draw.rect(gameWindow, ORANGE, pygame.Rect(xpos+60, ypos+60, 30, 30))

def stringDisplay(str, str_size, str_x_pos, str_y_pos, str_colour):
    font = pygame.font.SysFont("arial", str_size)
    textForDisplay = font.render(str, True, str_colour)
    gameWindow.blit(textForDisplay, (str_x_pos, str_y_pos))

def timeToString(time):
    minutes = int(time / 60)
    seconds = int(time) % 60
    miliseconds = int((time % 1) * 1000)
    if miliseconds < 100:
        strTime = str(minutes) + ":" + str(seconds) + ".0" + str(miliseconds)
    else:
        strTime = str(minutes) + ":" + str(seconds) + "." + str(miliseconds)

    return strTime


pygame.init()
pygame.font.init()
pygame.display.set_caption("Rubik's Cube Timer")
textForUser = " "
textForUser_xpos = 0
textForUser_ypos = 0
timeField = "0:0.000"
timeField_xpos = 115
timeField_ypos = 400
gameIsRunning = True
myStoper = Stoper.Stoper()

plus2sec_flag = False
dnf_flag = False

state = "IDLE"

while gameIsRunning:
    spaceDown = False
    spaceUp = False
    #spacePressed = pygame.key.get_pressed()[pygame.K_SPACE]
    escapeDown = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                spaceDown = True
            if event.key == pygame.K_ESCAPE:
                gameIsRunning = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                spaceUp = True

        elif event.type == pygame.QUIT:
            gameIsRunning = False

    if state == "IDLE":
        if spaceUp:
            state = "INSPECTION"
            myStoper.start()

        else:
            state = "IDLE"
            textForUser = "Ready?"
            textForUser_xpos = 130
            textForUser_ypos = 130

    elif state == "INSPECTION":
        textForUser = "You have 15 sec"
        textForUser_xpos = 54
        textForUser_ypos = 130
        if spaceUp:
            state = "SOLVING"
            myStoper.reset()
        else:
            time = myStoper.read()
            if time < 15.0:
                state = "INSPECTION"
                timeField = "    " + str(15 - int(time))
            elif time < 17.0:
                state = "INSPECTION"
                timeField = "+2 sec"
                plus2sec_flag = True
            else:
                state = "INSPECTION"
                timeField = "  DNF"
                dnf_flag = True

    elif state =="SOLVING":
        textForUser = " "
        textForUser_xpos = 54
        textForUser_ypos = 130
        solveTime = myStoper.read()
        timeField = timeToString(solveTime)
        if spaceUp:
            state = "IDLE"
            if plus2sec_flag:
                solveTime += 2.0
                plus2sec_flag = False
            elif dnf_flag:
                solveTime = 9999.0
                dnf_flag = False
            USER_TIMES_HISTORY.append(solveTime)
        else:
            state = "SOLVING"


    gameWindow.fill(BACKGROUND_COLOUR)
    drawCubeGraphic(155, 10)
    stringDisplay(textForUser, 40, textForUser_xpos, textForUser_ypos, WHITE)
    stringDisplay(timeField, 50, timeField_xpos, timeField_ypos, WHITE)
    bestTime = getBestTimeFromTimesHistory()
    stringDisplay("Best time:", 20, 280, 470, WHITE)
    if bestTime != -1:
        stringDisplay(timeToString(bestTime), 20, 280, 490, WHITE)
    stringDisplay("Last 5 times:", 20, 20, 470, WHITE)
    times = getUpToFiveLastTimesFromTimesHistory()
    if times != -1:
        ypos = 490
        for t in times:
            stringDisplay(timeToString(t), 20, 20, ypos, WHITE)
            ypos += 20
    pygame.display.update()
