import pygame, sys, random, time, os, math
from datetime import datetime

#Set up stuff
pygame.init()
pygame.mixer.pre_init()

TITLE = "QWER Piano Game"
WIDTH = 400
HEIGHT = 1000

#Screen stuff
FPS = 144
GRID = 100

#Control Shortcuts
Q = pygame.K_q
W = pygame.K_w
E = pygame.K_e
R = pygame.K_r

#Colors
PURPLE = (105,41,196)
BLUE = (80,75,232)
PINK = (158,67,158)
RED = (196,19,41)
BLACK = (0,0,0)
WHITE = (230,230,230)


#FONT
FONT = pygame.font.Font("minya_nouvelle_bd.ttf",36)

#High score file
try:
    scoreFile = open("scores.txt", "r")
    highScore = int(scoreFile.read())
except:
    scoreFile.close()
    scoreFile = open("scores.txt", "w")
    scoreFile.write("0")
    scoreFile.close()

scoreFile = open("scores.txt" , "r")
highScore = int(scoreFile.read())
scoreFile.close()
scoreFile = open("scores.txt", "w")


#Sounds
#HIT = pygame.mixer.Sound("hit.wav")
#MISS = pygame.mixer.Sound("miss.wav")\
#Something wrong with sound files and they won't play :(


def play_sound(sound):
    sound.play(0,0,0)

def play_music():
    pygame.mixer.music.play(-1)

def load_image(file_path):
    img = pygame.image.load(file_path)
    img = pygame.transform.scale(img, (GRID, GRID))

    return img


class Game():
    PLAYING = 0
    PAUSED = 1
    TIMEUP = 2
    def __init__(self):
        self.window = pygame.display.set_mode([WIDTH,HEIGHT])
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.done = False

        self.STAGE = 1
        self.active_layer = pygame.Surface([WIDTH,HEIGHT], pygame.SRCALPHA, 32)

        self.score = 0
        self.currentSquare = Q
        self.index = 0
        
        self.startMin = 0
        self.startSec = 0
        self.scoreWritten = False
        self.keys = []
        self.SQUARES = [Q,W,E,R]
        
    def start(self):
        for i in range(1000):
            r = random.randint(0,3)
            self.keys.append(self.SQUARES[r])
        self.scoreWritten = False

    def reset(self):
        
        self.keys = []
        self.score = 0
        self.index = 0
        self.start()
        self.STAGE = self.PAUSED
        
              
        
    def display_message(self,surface,text,x,y, color):
        text = FONT.render(text,1,color)
        surface.blit(text, (x,y))

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
                scoreFile.close()
            elif event.type == pygame.KEYDOWN and self.STAGE == self.PLAYING:
                if event.key == Q:
                    self.process(Q)
                if event.key == W:
                    self.process(W)
                if event.key == E:
                    self.process(E)
                if event.key == R:
                    self.process(R)
            elif event.type == pygame.KEYDOWN and self.STAGE == self.PAUSED:
                if event.key == pygame.K_SPACE:
                    self.STAGE = self.PLAYING
                    now = datetime.now()
                    self.startMin = int(now.strftime("%M"))
                    self.startSec = int(now.strftime("%S"))
                
            elif event.type == pygame.KEYDOWN and self.STAGE == self.TIMEUP:
                time.sleep(2)
                self.reset()
                
    def update(self):
        self.currentSquare = self.keys[self.index+1]
        now = datetime.now()
        curMin = int(now.strftime("%M"))
        curSec = int(now.strftime("%S"))
        
        if self.startMin + 1 == curMin and curSec == self.startSec:
            self.STAGE = self.TIMEUP
            if self.score > int(highScore) and not self.scoreWritten:
                scoreFile.write(str(self.score))
                self.scoreWritten = True
                
    def process(self, key):
        if self.currentSquare == key:
            self.score += 2
            self.index += 1
            #play_sound(HIT)
        else:
            self.score -= 1
            #play_sound(MISS)
    def draw(self):
        self.active_layer.fill(WHITE)
        if self.STAGE == self.PLAYING:
            for i in range(6):
                kee = self.keys[self.index + i]
                if kee == Q:
                    pygame.draw.rect(self.active_layer, RED, [0, (1000 - (i*200)), 100, 200])
                if kee == W:
                    pygame.draw.rect(self.active_layer, BLUE, [100, (1000 - (i*200)), 100, 200])
                if kee == E:
                    pygame.draw.rect(self.active_layer, PURPLE, [200, (1000 - (i*200)), 100, 200])
                if kee == R:
                    pygame.draw.rect(self.active_layer, PINK, [300, (1000 - (i*200)), 100, 200])
            scoreString = "Score : " +  str(self.score)
            self.display_message(self.active_layer, scoreString, 200, 50, BLACK)    
            self.window.blit(self.active_layer, [0,0])
        elif self.STAGE == self.PAUSED:
            self.display_message(self.active_layer, "PRESS SPACE TO START", 10, 455, BLACK)
        elif self.STAGE == self.TIMEUP:
            self.display_message(self.active_layer, "TIME UP, SCORE: "+str(self.score), 10, 455, BLACK)
            
            
        self.window.blit(self.active_layer, [0,0])
        pygame.display.flip()
    def loop(self):
        while not self.done:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
    
    
game = Game()
game.start()
game.loop()
pygame.quit()
sys.exit()
