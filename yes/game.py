import pygame

pygame.init()

#Backround and window
win = pygame.display.set_mode((1000, 500))
bg_img = pygame.image.load("swamp.png")
bg = pygame.transform.scale(bg_img, (1000, 500))
win_width = 1000
win_height = 500

pygame.display.set_caption("First game")

standing = pygame.image.load("standing.png")
bullet_img = pygame.transform.scale(pygame.image.load("new_bullet.png"), (10, 10))

left = [None]*10
for picIndex in range(1, 10):
    left[picIndex-1] = pygame.image.load("L" + str(picIndex)+ ".png")
    picIndex+=1

right = [None]*10
for picIndex in range(1, 10):
    right[picIndex-1] = pygame.image.load("R" + str(picIndex)+ ".png")
    picIndex+=1


def draw_game():
    global stepIndex
    win.fill((0,0,0))
    win.blit(bg, (0, 0))
    player.draw(win)
    for bullet in player.bullets:
        bullet.draw_bullet()
    pygame.time.delay(30)
    pygame.display.update()


class Hero:
    def __init__(self, x, y):
        #walk
        self.x = x
        self.y = y
        self.velx = 10
        self.vely = 10
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        #jump
        self.jump = False
        #bullet
        self.bullets = []


    def move_hero(self, userInput):
        if userInput[pygame.K_d] and self.x <= win_width - 62:
            self.x += self.velx
            self.face_right = True
            self.face_left = False
        elif userInput[pygame.K_a] and self.x >= 0:
            self.x -= self.velx
            self.face_right = False
            self.face_left = True
        else:
            self.stepIndex = 0

    def draw(self, win):
        if self.stepIndex >= 9:
            self.stepIndex = 0
        if self.face_left:
            win.blit(left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1

    def jump_motion(self, userInput):
        if userInput[pygame.K_SPACE] and self.jump is False:
            self.jump = True
        if self.jump:
            self.y -= self.vely*4
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1


    def shoot(self):
        if userInput[pygame.K_f]:
            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
        for bullet in self.bullets:
            bullet.move()

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 25
        self.direction = direction


    def draw_bullet(self):
        win.blit(bullet_img, (self.x, self.y))

    def move(self):
        if self.direction == 1:
            self.x += 15
        if self.direction == -1:
            self.x -= 15

player = Hero(250, 385)

run = True
while run:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #input
    userInput = pygame.key.get_pressed()

    #shoot
    player.shoot()

    #movement
    player.move_hero(userInput)
    player.jump_motion(userInput)

    #draw game
    draw_game()

