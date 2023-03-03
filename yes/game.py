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

#Initializing sounds
pygame.mixer.init()
pygame.mixer.music.load('Retrogame_music_1.mp3')
pygame.mixer.music.play()
death_sound = pygame.mixer.Sound("death.mp3")


pygame.display.set_caption("Game name")

standing = pygame.image.load("standing.png") #not used ?
bullet_img = pygame.transform.scale(pygame.image.load("new_bullet.png"), (10, 10))



def draw_game():
    win.fill((0,0,0))
    win.blit(bg, (0, 0))
    player.draw(win)
    pygame.draw.rect(win,50,player.rect)
    for e in enemies:
        e.draw(win)
        pygame.draw.rect(win,255,e.rect)            #comment draw.rects out, only for debugging hitboxes
    for bullet in player.bullets:
        bullet.draw_bullet()
        #pygame.draw.rect(win,255,bullet.rect)
    for o in obstacles:
        #pygame.draw.rect(win,255,o.rect)
        o.draw(win)
    pygame.time.delay(30)
    pygame.display.update()


class Hero:
    left = []
    for picIndex in range(1, 5):
        left.append(pygame.image.load("L" + str(picIndex)+ ".png"))

    right = []
    for picIndex in range(1, 5):
        right.append(pygame.image.load("R" + str(picIndex)+ ".png"))

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
        self.tolerance = 16
        self.bullets = []


    def move(self, userInput):
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
            
        
        if userInput[pygame.K_w] and self.jump is False:
            self.jump = True
        
        if self.jump == True: 
            self.y -= self.vely*1.5 
            self.vely -= 1
        if self.y>=groundlevel: #stops character from falling under the ground
            self.jump = False
            self.vely = 10
        if self.jump == False : self.vely = 10  #reset velocity for next jump
    
        self.rect.x = self.x+20    #update rect pos
        self.rect.y = self.y+15


    def draw(self, win):
        if self.stepIndex >= 4:
            self.stepIndex = 0
        if self.face_left:
            win.blit(self.left[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.face_right:
            win.blit(self.right[self.stepIndex], (self.x, self.y))
            self.stepIndex += 1
        if self.y > groundlevel: self.y=groundlevel
        

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1


    def shoot(self):
        global lastshot
        cdamount = 250

        if userInput[pygame.K_SPACE] and lastshot+cdamount < pygame.time.get_ticks():  #shoots only if cdamount (milliseconds) has passed
            lastshot = pygame.time.get_ticks() #update time

            bullet = Bullet(self.x, self.y, self.direction())
            self.bullets.append(bullet)
        for bullet in self.bullets:
            bullet.move()

class Obstacle:
    box_image = pygame.image.load("box.png")
    def __init__(self,x,y,width,height):
        self.rect = pygame.Rect(x,y,width,height)
        self.x = x
        self.y = y
        self.tolerance = 5

    def draw(self, win):
        win.blit(self.box_image, (self.x, self.y))

        #collision detection
        if self.rect.colliderect(player.rect) and abs(self.rect.top - player.rect.top) < 20:    #if player is colliding and about on the same level
            if abs(player.rect.right - self.rect.left) < 7:     #if players right side is close to obstacles left side, push player to the left
                player.x -= player.velx
            if abs(player.rect.left-self.rect.right)<12:        #above but right side with larger tolerance for weird hitbox
                player.x+= player.velx
        
        if abs(player.rect.bottom - self.rect.top) < self.tolerance and self.rect.left<player.rect.centerx and self.rect.right>player.rect.centerx: #if player is above obstacle and players center is between obstacles left and right side
            player.jump = False #prevents from falling through
            if player.rect.right < self.rect.centerx or player.rect.left > self.rect.centerx:   #make player fall off the side
                player.vely = 0
                player.jump = True
       

class Enemy:
    left = []
    for picIndex in range(1, 10):
        left.append(pygame.image.load("L" + str(picIndex)+ "E.png"))

    right = []
    for picIndex in range(1, 10):
        right.append(pygame.image.load("R" + str(picIndex)+ "E.png"))
    def __init__(self, x, y, end):
        self.rect = pygame.Rect(x,y+15,25,50)
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
        if self.rect.colliderect(player.rect): #might have future use idk
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
        self.rect.x = self.x+20
        

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
        
        if self.rect.colliderect(player.rect) and abs(self.rect.top - player.rect.top) < 20:    #check if player is colliding and on the same level
            if abs(player.rect.right - self.rect.left) < 7:     #check which side is closer to determine direction to push player
                player.x -= player.velx
            if abs(player.rect.left-self.rect.right)<7:
                player.x+= player.velx

        if abs(player.rect.bottom - self.rect.top) < 5 and self.rect.left-10<player.rect.centerx and self.rect.right+10>player.rect.centerx: #if player is above obstacle and players center is between obstacles left and right side
            player.jump = False #prevents from falling through
            if player.rect.right < self.rect.centerx or player.rect.left > self.rect.centerx:   #make player fall off the side
                player.vely = 0
                player.jump = True
        

    def death(self): pygame.mixer.Sound.play(death_sound)





class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 25
        self.direction = direction
        self.rect = pygame.Rect(x+15,y+25,10,10)


    def draw_bullet(self):
        win.blit(bullet_img, (self.x, self.y))

    def move(self):
        if self.direction == 1:
            self.x += 35        #bullet speed
            
        if self.direction == -1:
            self.x -= 35   
        self.rect.x = self.x

        if self.rect.collidelist(enemies)!=-1:
            i = self.rect.collidelist(enemies)      #save collided enemy index
            enemies[i].death()                      #call death sound           
            del player.bullets[enemies[i].rect.collidelist(player.bullets)]    #deletes the bullet instance that collided with the enemy
            del enemies[i]                                                      #deletes enemy instance that collided
            


player = Hero(250, groundlevel)
enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))        #always append to enemies list when creating new instances
enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))        #in Enemy(x,y,z), x is x pos, y is y pos and z is the lenght of the enemy's travel
enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))
obstacles.append(Obstacle(450,groundlevel,50,50))
enemies.append(Enemy(200,groundlevel,0))


run = True
while run: 

    #print(pygame.time.get_ticks())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
   
    #if lastspawn+1500 < pygame.time.get_ticks():                   #for spawning enemies every 1.5 second
    #    lastspawn = pygame.time.get_ticks()
    #    enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))


    
    
    #input
    userInput = pygame.key.get_pressed()

    #shoot
    player.shoot()
    
    #movement
    player.move(userInput)
    #draw game
    draw_game()

