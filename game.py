import pygame
import os
import random


# sets working directory to python file folder to fix errors when running game through vscode
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

#Backround and window
win_width = 1000
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
bg_img = pygame.image.load("./assets/img/background.png")
bg = pygame.transform.scale(bg_img, (win_width, win_height))

fonts = pygame.font.get_fonts()
font1 = pygame.font.SysFont(None,48)
font2 = pygame.font.SysFont(None,100)



#Global variables for tracking stuff
lastshot = 0 # for shooting cooldown
lastspawn = 0 #for spawning enemies once in a while
lastdmg = 0 #for not getting instakilled
enemies = [] #support for multiple enemies
obstacles = [] 
groundlevel = 390
run = True
winning = True
#Initializing sounds
pygame.mixer.init()
pygame.mixer.music.load('./assets/audio/Retrogame_music_1.ogg')
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play()

death_sound = pygame.mixer.Sound("./assets/audio/UOHu.ogg")
olkapaa = pygame.mixer.Sound("./assets/audio/Ai_vittu_mun_olkapaa.ogg")
shoot = pygame.mixer.Sound("./assets/audio/Ampuskelu.ogg")
iced = pygame.mixer.Sound("./assets/audio/Jaassssa.ogg")
player_death = pygame.mixer.Sound("./assets/audio/Kertaakaa.ogg")
point = pygame.mixer.Sound("./assets/audio/Pisteaani.ogg")

enemyDeathSounds = [olkapaa,death_sound,iced]

pygame.display.set_caption("Megamogosen")

standing = pygame.image.load("./assets/img/standing.png") #not used ?
bullet_img = pygame.transform.scale(pygame.image.load("./assets/img/new_bullet.png"), (10, 10))



def draw_game():
    win.fill((0,0,0))
    win.blit(bg, (0, 0))
    player.draw(win)
    #pygame.draw.rect(win,(0,255,0),player.rect)
    for e in enemies:
        e.draw(win)
        #pygame.draw.rect(win,(255,0,0),e.rect)            #comment draw.rects out, only for debugging hitboxes
    for bullet in player.bullets:
        bullet.draw_bullet()
        #pygame.draw.rect(win,(255,0,0),bullet.rect)
    for o in obstacles:
        pygame.draw.rect(win,(255,255,255),o.rect)
        o.draw(win)
    pygame.time.delay(30)
    pygame.display.update()


class Hero:
    left = []
    #for picIndex in range(1, 5):
    #    left.append(pygame.image.load("./assets/img/L" + str(picIndex)+ ".png"))
    left.append(pygame.image.load("./assets/img/PL1.png"))
    right = []
    #for picIndex in range(1, 5):
    #    right.append(pygame.image.load("./assets/img/R" + str(picIndex)+ ".png"))
    right.append(pygame.image.load("./assets/img/PR1.png"))
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
        self.ammo = 25
        self.points = 0
        self.health = 100


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
        #if self.stepIndex >= 4:
        #    self.stepIndex = 0
        if self.face_left:
            win.blit(self.left[0], (self.x+self.left[0].get_width()/2, self.y+self.left[0].get_height()/3))
        #    self.stepIndex += 1
        if self.face_right:
            win.blit(self.right[0], (self.x+self.left[0].get_width()/2, self.y+self.left[0].get_height()/3))
         #   self.stepIndex += 1
        if self.y > groundlevel: self.y=groundlevel
        ammotext = font1.render("Ammo: "+str(self.ammo), True, (255,255,255))
        win.blit(ammotext,(0,35))
        
        pointtext = font1.render("Points: "+str(self.points), True, (255,255,255))
        win.blit(pointtext,(0,70))

        healthtext = font1.render("HP: "+str(self.health), True, (255,0,0))
        win.blit(healthtext,(0,0))
        if self.health <= 0:
            self.death()
        

    def direction(self):
        if self.face_right:
            return 1
        if self.face_left:
            return -1


    def death(self):
        global winning 
        pygame.mixer.music.pause()
        pygame.mixer.Sound.play(player_death)
        winning = False
        deathtext = font2.render("GAME OVER", True, (255,0,0))
        win.blit(deathtext,(300,250))
        
    def shoot(self):
        global lastshot
        cdamount = 200

        if userInput[pygame.K_SPACE] and lastshot+cdamount < pygame.time.get_ticks() and self.ammo > 0:  #shoots only if cdamount (milliseconds) has passed
            pygame.mixer.Sound.play(shoot)
            lastshot = pygame.time.get_ticks() #update time
            self.ammo -= 1
            bullet = Bullet(self.x, self.y+10, self.direction())
            self.bullets.append(bullet)
        for bullet in self.bullets:
            bullet.move()

class Obstacle:
    def __init__(self,x,y,width,height):
        self.rect = pygame.Rect(x,y,width,height)
        self.x = x
        self.y = y
        self.tolerance = 5

    def draw(self, win):
        #win.blit(self.box_image, (self.x, self.y))

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
        left.append(pygame.image.load("./assets/img/L" + str(picIndex)+ "E.png"))

    right = []
    for picIndex in range(1, 10):
        right.append(pygame.image.load("./assets/img/R" + str(picIndex)+ "E.png"))
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
        global lastdmg
        if abs(self.rect.centerx-player.rect.centerx) < 30 and abs(self.rect.top - player.rect.bottom)>25 and lastdmg+1000 < pygame.time.get_ticks(): 
           lastdmg = pygame.time.get_ticks() 
           player.health -= 10
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
        

    def death(self): 
        pygame.mixer.Sound.play(random.choice(enemyDeathSounds))
        player.ammo += 2
        player.points += 1
        if player.points%10 == 0: pygame.mixer.Sound.play(point)






class Bullet:
    def __init__(self, x, y, direction):
        self.x = x + 15
        self.y = y + 25
        self.direction = direction
        self.rect = pygame.Rect(x+15,y+25,10,10)
        self.visible = True
        


    def draw_bullet(self):
        if self.visible:
            win.blit(bullet_img, (self.x, self.y))

    def move(self):
        self.rect.x = self.x
        obstaclec = self.rect.collidelist(obstacles)
        enemyc = self.rect.collidelist(enemies)
        if self.visible:
            if self.direction == 1:
                self.x += 35        #bullet speed
                
            if self.direction == -1:
                self.x -= 35   
            if obstaclec!=-1:
                self.visible = False
            if enemyc!=-1:
                enemies[enemyc].death()                      #call death sound           
                del enemies[enemyc]                          #deletes enemy instance that collided
                self.visible = False
                


player = Hero(250, groundlevel)
#enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))        #always append to enemies list when creating new instances
#enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))        #in Enemy(x,y,z), x is x pos, y is y pos and z is the lenght of the enemy's travel
#enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,800)))
obstacles.append(Obstacle(450,groundlevel,50,50))
#enemies.append(Enemy(200,groundlevel,0))


while run: 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if winning:
        if lastspawn+2500 < pygame.time.get_ticks():                   #for spawning enemies every 1.5 second
            lastspawn = pygame.time.get_ticks()
            enemies.append(Enemy(random.randint(0,500),groundlevel,random.randint(200,900)))
        userInput = pygame.key.get_pressed()
        player.shoot()
        player.move(userInput)
        draw_game()

