import pygame

pygame.init()
screen_width = 500
screen_height= 480
win = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()


background = pygame.image.load('bg.jpg')

# Vihollisen luokka
class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'),pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'),pygame.image.load('R9E.png'),pygame.image.load('R10E.png'),pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'),pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y+2, 31, 57)
        self.health = 10
        self.visible = True

    def draw(self, win): #Hahmon piirtäminen
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            self.hitbox = (self.x + 17, self.y+2, 31, 57)
            #pygame.draw.rect(win, (255,0,0), self.hitbox ,2) #piirtää hahmon hitboxin kommentoi pois
    
    def move(self): #hahmon liikkuminen
        if self.vel > 0:
            if self.x  + self.vel < self.path[1]:
                self.x+=self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

def redrawGameWindow():
    win.blit(background, (0,0))
    goblin.draw(win)

    pygame.display.update()

#main loop
font = pygame.font.SysFont('comicsans',30, True, True)
goblin = enemy(100,410,64,64,450)
run = True

while run:
    clock.tick(27)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False



    redrawGameWindow()

    
pygame.quit()
