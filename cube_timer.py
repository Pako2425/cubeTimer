import pygame
import time
from enum import Enum

class rubiksCube:
    rCubeRect1 = pygame.Rect(0, 0, 0, 0)
    rCubeRect2 = pygame.Rect(0, 0, 0, 0)
    rCubeRect3 = pygame.Rect(0, 0, 0, 0)
    rCubeRect4 = pygame.Rect(0, 0, 0, 0)
    rCubeRect5 = pygame.Rect(0, 0, 0, 0)
    rCubeRect6 = pygame.Rect(0, 0, 0, 0)
    rCubeRect7 = pygame.Rect(0, 0, 0, 0)
    rCubeRect8 = pygame.Rect(0, 0, 0, 0)
    rCubeRect9 = pygame.Rect(0, 0, 0, 0)

    def rCubeDrawing(self):
        pygame.draw.rect(gameWindow, green, self.rCubeRect1)
        pygame.draw.rect(gameWindow, yellow, self.rCubeRect2)
        pygame.draw.rect(gameWindow, green, self.rCubeRect3)
        pygame.draw.rect(gameWindow, red, self.rCubeRect4)
        pygame.draw.rect(gameWindow, white, self.rCubeRect5)
        pygame.draw.rect(gameWindow, blue, self.rCubeRect6)
        pygame.draw.rect(gameWindow, orange, self.rCubeRect7)
        pygame.draw.rect(gameWindow, green, self.rCubeRect8)
        pygame.draw.rect(gameWindow, orange, self.rCubeRect9)

myCube = rubiksCube()

class TimerState(Enum):
    READY = 0,
    WAITING = 1,
    SOLVING = 2,
    PENALTY = 3,
    DNF = 4,
    STOP = 5,
    DISPLAYING = 6

class Screen:
    def stringDisplay(self, str, str_size, str_x_pos, str_y_pos, str_colour):
        font = pygame.font.SysFont("arial", str_size)
        textForDisplay = font.render(str, True, str_colour)
        gameWindow.blit(textForDisplay, (str_x_pos, str_y_pos))

myScreen = Screen()

class EventsHandling:
    spaceDown = False
    spaceUp = False
    escapeDown = False
    escapeUp = False
    programQuite = False

    def eventsHandling(self):
        self.spaceUp = False
        self.spaceDown = False
        self.programQuite = False
        self.escapeUp = False
        self.escapeDown = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.spaceDown = True
                elif event.key == pygame.K_ESCAPE:
                    self.escapeDown = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.spaceUp = True
            elif event.type == pygame.QUIT:
                self.programQuite = True

myEvents = EventsHandling()

class Timer:
    startTime = 0.0
    mTime = 0.0
    mTime_str = " "
    def timer(self, reset=0):
        if reset == 1:
            self.startTime = time.time()
        self.mTime = time.time() - self.startTime
        minutes = int(self.mTime/60)
        seconds = int(self.mTime) % 60
        miliseconds = int((self.mTime % 1)*1000)
        if miliseconds < 100:
            self.mTime_str = str(minutes) + ":" + str(seconds) + ".0" + str(miliseconds)
        else:
            self.mTime_str = str(minutes) + ":" + str(seconds) + "." + str(miliseconds)

myTimer = Timer()

white = (255, 255, 255)
yellow = (255, 255, 0)
green = (0, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
orange = (255, 130, 0)
background_colour = (0, 0, 100)

textForUser = " "
timeField = "0:0.000"

gameWindow = pygame.display.set_mode((400, 600))
currentState = TimerState.READY
textXPOS = 0   #przenieść do myScreen
textYPOS = 0   #przenieść do myScreen

class ProgramLogic:
    GameIsRunning = False

    def programQuite(self):
        self.GameIsRunning = True
        if myEvents.programQuite or myEvents.escapeDown:
            self.GameIsRunning = False

myProgramLogic = ProgramLogic()

def init():
    myCube.rCubeRect1 = pygame.Rect(150, 10, 30, 30)
    myCube.rCubeRect2 = pygame.Rect(185, 10, 30, 30)
    myCube.rCubeRect3 = pygame.Rect(220, 10, 30, 30)
    myCube.rCubeRect4 = pygame.Rect(150, 45, 30, 30)
    myCube.rCubeRect5 = pygame.Rect(185, 45, 30, 30)
    myCube.rCubeRect6 = pygame.Rect(220, 45, 30, 30)
    myCube.rCubeRect7 = pygame.Rect(150, 80, 30, 30)
    myCube.rCubeRect8 = pygame.Rect(185, 80, 30, 30)
    myCube.rCubeRect9 = pygame.Rect(220, 80, 30, 30)

    myProgramLogic.GameIsRunning = True
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Rubik's Cube Timer")

    myEvents.spaceDown = False
    myEvents.spaceUp = False


init()
myTimer.timer(1)
while myProgramLogic.GameIsRunning:
    gameWindow.fill(background_colour)
    myTimer.timer()
    myCube.rCubeDrawing()
    myEvents.eventsHandling()
    if currentState == TimerState.READY:
        if myEvents.spaceUp:
            currentState = TimerState.WAITING
            myTimer.timer(1)
        else:
            currentState = TimerState.READY
            textForUser = "Ready?"
            textXPOS = 130
            textYPOS = 130
            timeField = " "

    elif currentState == TimerState.WAITING:
        textForUser = "You have 15 sec"
        textXPOS = 54
        textYPOS = 130
        if myEvents.spaceUp:
            currentState = TimerState.SOLVING
            myTimer.timer(1)
        elif not myEvents.spaceUp and myTimer.mTime < 15:
            currentState = TimerState.WAITING
            timeField = "    " + str(15 - int(myTimer.mTime))
        else:
            currentState = TimerState.PENALTY
            myTimer.timer(1)

    elif currentState == TimerState.SOLVING:
        textForUser = " "
        textXPOS = 54
        textYPOS = 130
        if myEvents.spaceDown:
            currentState = TimerState.STOP
        else:
            currentState = TimerState.SOLVING
            timeField = myTimer.mTime_str

    elif currentState == TimerState.PENALTY:
        if myEvents.spaceUp:
            currentState = TimerState.SOLVING
            myTimer.timer(1)
        elif not myEvents.spaceUp:
            if myTimer.mTime <= 2:
                currentState = TimerState.PENALTY
                timeField = "+2 sec"
            elif myTimer.mTime > 2:
                currentState = TimerState.DNF

    elif currentState == TimerState.DNF:
        if myEvents.spaceUp:
            currentState = TimerState.READY
        else:
            currentState = TimerState.DNF
            timeField = "  DNF"

    elif currentState == TimerState.STOP:
        textForUser = "Your time:"
        textXPOS = 110
        textYPOS = 130
        if myEvents.spaceUp:
            currentState = TimerState.DISPLAYING
    else:
        if myEvents.spaceUp:
            currentState = TimerState.READY
            timeField = "0:0.000"
            spaceDown = 0

    myScreen.stringDisplay(textForUser, 40, textXPOS, textYPOS, white)
    myScreen.stringDisplay(timeField, 50, 115, 400, white)
    pygame.display.update()
    myProgramLogic.programQuite()
