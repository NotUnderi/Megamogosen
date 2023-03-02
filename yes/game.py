import pygame
import os
import random


# sets working directory to python file folder to fix errors when running game through vscode
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

#Backround and window
win = pygame.display.set_mode((1000, 500))
bg_img = pygame.image.load("swamp.png")
bg = pygame.transform.scale(bg_img, (1000, 500))
win_width = 1000
win_height = 500


#Global variables for tracking stuff
lastshot = 0 # for shooting cooldown
lastspawn = 0 #for spawning enemies once in a while
enemies = [] #support for multiple enemies
obstacles = [] 
groundlevel = 390

#Initializing music
pygame.mixer.init()
pygame.mixer.music.load('Retrogame_music_1.mp3')
pygame.mixer.music.play()
death_sound = pygame.mixer.Sound("death.mp3")


pygame.display.set_caption("Game name")

standing = pygame.image.load("standing.png")
bullet_img = pygame.transform.scale(pygame.image.load("new_bullet.png"), (10, 10))



def draw_game():
    win.fill((0,0,0))
    win.blit(bg, (0, 0))
    player.draw(win)
    for e in enemies:
        e.draw(win)
    for bullet in player.bullets:
        bullet.draw_bullet()
    for o in obstacles:
        o.draw(win)
    pygame.time.delay(30)
    pygame.display.update()


class Hero:
    left = [None]*10
    for picIndex in range(1, 10):
      left[picIndex-1] = pygame.image.load("L" + str(picIndex)+ ".png")

    right = [None]*10
    for picIndex in range(1, 10):
     right[picIndex-1] = pygame.image.load("R" + str(picIndex)+ ".png")

    def __init__(self, x, y):
        self.rect = pygame.Rect(x,y,25,50)
        self.x = x
        self.y = y
        self.velx = 10      
        self.vely = 10     
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        self.jump = False
        self.ontop = False
        self.tolerance = 10
        self.bullets = []


    def move(self, userInput):
        for e in enemies:
            if abs(self.rect.bottom - e.rect.top) < 5 and abs(self.rect.x - e.rect.x) < e.rect.w:
                self.ontop = True
                #self.vely = 0
            else:
                self.ontop = False
            if abs(self.rect.top - e.rect.top) < self.tolerance:
                if abs(self.rect.right - e.rect.left) < self.tolerance:
                    self.x -= self.velx
                    self.stepIndex = 0
                if abs(self.rect.left - e.rect.right) < self.tolerance:
                    self.x += self.velx
                    self.stepIndex = 0
        #rint(self.rect.bottom - e.rect.top)
        if self.rect.collidelist(obstacles)!=-1:
            self.x -= self.velx * self.direction()

        if self.rect.collidelist(enemies)==-1 or self.ontop == True:
            if userInput[pygame.K_d] and self.rect.x <= win_width - 55:
                self.x += self.velx
                self.face_right = True
                self.face_left = False
            elif userInput[pygame.K_a] and self.x >= 0:
                self.x -= self.velx
                self.face_right = False
                self.face_left = True
            else:
                self.stepIndex = 0
        self.rect.x = self.x

    def draw(self, win):
        if self.stepIndex >= 4:
            self.stepIndex = 0
        if self.face_left:
            win.blit(self.left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(self.right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        


    def jump_motion(self, userInput):
        if userInput[pygame.K_w] and self.jump is False:
            self.jump = True
        
        if self.jump == True and self.ontop == False:
            if self.y <= groundlevel: self.y -= self.vely*1.5 # jump height and speed
            self.vely -= 1
        if self.vely < -10:
            self.jump = False
            self.vely = 10
        self.rect.y = self.y

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1


    def shoot(self):
        global lastshot
        cdamount = 200

        if userInput[pygame.K_SPACE] and lastshot+cdamount < pygame.time.get_ticks():  #shoots only if cdamount (milliseconds) has passed
            lastshot = pygame.time.get_ticks() #update time

            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
        for bullet in self.bullets:
            bullet.move()

class Obstacle:
    box_image = pygame.image.load("box.png")
    def __init__(self,x,y):
        self.rect = pygame.Rect(x-25,y-25,50,50)
        self.x = x
        self.y = y

    def draw(self, win):
        win.blit(self.box_image, (self.x, self.y))


class Enemy:
    left = [None]*10
    for picIndex in range(1, 10):
          left[picIndex-1] = pygame.image.load("L" + str(picIndex)+ "E.png")

    right = [None]*10
    for picIndex in range(1, 10):
        right[picIndex-1] = pygame.image.load("R" + str(picIndex)+ "E.png")
    def __init__(self, x, y, end):
        self.rect = pygame.Rect(x,y,25,50)
        self.x = x
        self.y = y
        self.velx = 5      
        self.vely = 10 
        self.face_right = True
        self.face_left = False
        self.stepIndex = 0
        self.end = end
        self.path = [self.x,self.end]


    def move(self):
        if self.rect.colliderect(player.rect):
           pass
        if self.velx > 0:
            if self.x + self.velx < self.end:
                self.x += self.velx
                self.face_right = True
                self.face_left = False
            else:
                self.velx = self.velx*-1
                self.face_right = False
                self.face_left = True
                self.stepIndex = 0
        else:
            if self.x - self.velx > self.path[0]:
                self.x += self.velx
            else:
                self.velx = self.velx *-1
                self.face_right = False
                self.face_left = True
                self.stepIndex = 0
        self.rect.x = self.x

    def draw(self, win):
        self.move()
        if self.stepIndex >= 4:
            self.stepIndex = 0
        if self.face_left:
            win.blit(self.left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(self.right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
    def death(self):
        pygame.mixer.Sound.play(death_sound)





class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 25
        self.direction = direction
        self.rect = pygame.Rect(x,y,10,10)


    def draw_bullet(self):
        win.blit(bullet_img, (self.x, self.y))

    def move(self):
        if self.direction == 1:
            self.x += 35        #bullet speed
            
        if self.direction == -1:
            self.x -= 35   
        self.rect.x = self.x
        if self.rect.collidelist(enemies)!=-1:
            i = self.rect.collidelist(enemies)
            enemies[i].death()
            del player.bullets[enemies[i].rect.collidelist(player.bullets)]
            del enemies[i]
            


player = Hero(250, groundlevel)
enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))
enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))
enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))
obstacles.append(Obstacle(450,groundlevel))
#enemies.append(Enemy(200,groundlevel,0))


run = True
while run: 

    #print(pygame.time.get_ticks())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
   
    #if lastspawn+1500 < pygame.time.get_ticks():
    #    lastspawn = pygame.time.get_ticks()
    #    enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))


    
    print(player.ontop)
    #input
    userInput = pygame.key.get_pressed()

    #shoot
    player.shoot()
    
    #movement
    player.move(userInput)
    player.jump_motion(userInput)
    #draw game
    draw_game()

