#======Zombie Apocalypse======#
#======Abdul  Abu Libda=======#

from pygame import*
from math import*
from random import*

width,height = 800,600
screen = display.set_mode((width,height))
screen.fill((255,255,255))
cover = Surface((800,600),SRCALPHA)
wave = Surface((800,600),SRCALPHA)

mixer.init()
mixer.set_num_channels(100) #Allows for multiple overlapping audio files
myClock = time.Clock()
font.init()
myFont = font.SysFont("Tw Cen MT Condensed Extra",60)
pauseFont = font.SysFont("Tw Cen MT Condensed Extra",20)
roundFont = font.SysFont("Tw Cen MT Condensed Extra",200)

class Menu: #Menu class handles what parts of the game are being used
    def __init__(self,screen):
        self.screen = screen
        self.rect = []
        self.running = True
        self.round = 1
        self.zombies = []
        self.ready = 1
        self.deaditems = []
        self.items = []
        self.nuke = image.load("gfx/screens/nuke.jpg")
        self.roundpic = image.load("gfx/screens/roundpic.jpg").convert()
        self.nukealpha = 0
        self.pause = -1
        
    def update(self): #Changes screen to suit selected mode
        if self.screen == "start":
            screen.blit(start,(0,0))
            self.rect1 = Rect(28,93,185,95)
            self.rect2 = Rect(28,215,185,95)
            self.rect3 = Rect(28,341,185,95)
            self.rect4 = Rect(28,463,185,95)
            self.rects = [self.rect1,self.rect2,self.rect3,self.rect4]
            for rect in self.rects:
                if rect.collidepoint(mx,my):
                    draw.rect(screen,(100,100,100),rect)
                    if mb[0] == 1:
                        if self.rects.index(rect) == 0:
                            self.screen = "play"
                        elif self.rects.index(rect) == 1:
                            self.screen = "controls"             
                        elif self.rects.index(rect) == 2:
                            self.screen = "credits"
                        else:
                            self.running = False
        if self.screen == "controls":
            screen.blit(image.load("gfx/screens/controls.jpg"),(0,0))
            backRect = Rect(650,0,150,100)
            if backRect.collidepoint(mx,my) and click:
                self.screen = "start"
        if self.screen == "credits":
            screen.blit(image.load("gfx/screens/credits.jpg"),(0,0))
            backRect = Rect(650,0,150,100)
            if backRect.collidepoint(mx,my) and click:
                self.screen = "start"
        if self.screen == "play": #This code allows for 'pausing' in-game
            if self.pause == 1:
                screen.blit(background,(0,0))
                guy.draw() #It does so by stopping any updating of the classes
                killcheck() #Though it does draw them
                cover.fill((0,0,0,200))
                pauseRects = [Rect(320,185,160,45),Rect(350,265,100,45),Rect(350,345,100,45),Rect(350,425,90,45)]
                texts = ["Resume","Save","Load","Exit"]

                for rect in pauseRects:
                    screen.blit(myFont.render((texts[pauseRects.index(rect)]),1,(255,255,255,100)),(rect[0],rect[1]))
                    if rect.collidepoint(mx,my):
                        draw.rect(cover,(50,50,50,200),rect)
                        if click:
                            if pauseRects.index(rect) == 0:
                                self.pause = -1
                                break
                            if pauseRects.index(rect) == 1:
                                savegame()
                            if pauseRects.index(rect) == 2:
                                global load
                                load = 1
                            if pauseRects.index(rect) == 3:
                                self.running = False
                screen.blit(cover,(0,0))

            else:
                screen.blit(background,(0,0))
                killcheck() 
                guy.update()
                guy.draw()
                drawhud()
                if self.nukealpha > 0:
                    self.nuke.set_alpha((self.nukealpha))
                    screen.blit(self.nuke,(0,0))
                    self.nukealpha -= 3
            self.ready -= (1/50)
            if self.ready < 0:
                self.ready = 0
            if len(self.zombies) < 1 and len(enemies) == 0 and self.ready == 0 and self.nukealpha < 10:                
                self.newround() #Calls new round when all zombies are dead
            elif len(self.zombies) > 0: #The main releasing of the zombie
                if self.ready == 0 and self.pause == -1:
                    self.makezombie(self.zombies[0])
                    del(self.zombies[0])
                    self.ready = 1
        display.flip()
        
    def makezombie(self,name): #Creates a new zombie based on zombie dict
        loc = randint(1,2)
        loc2 = randint(1,2) #Randomly chooses which side enemies come in from
        if loc == 1:
            if loc2 == 1:
                enemies.append(Enemy(randint(335,465),0,name))
            else:
                enemies.append(Enemy(randint(335,465),600,name))
        else:
            if loc2 == 1:
                enemies.append(Enemy(0,randint(255,388),name))
            else:
                enemies.append(Enemy(800,randint(255,388),name))
        for enemy in enemies:
            enemy.move()

                
    def newround(self): #Creates a new round entirely
        for alpha in range(255,0,-1):
            screen.fill((0,0,0))
            self.roundpic.set_alpha(alpha)
            screen.blit(roundFont.render((str(int(self.round))),1,(230,0,0,alpha)),(350,320))

            screen.blit(self.roundpic,(0,0))
            display.flip()
        self.round += 1
        self.zombies = ["N"]*(self.round*2) #Always creates normal zombies
        for item in self.items: #Clear out items after each round
            item.picked = True
        for i in range(len(storeitems)):
            if i == 0:
                x = 50
            elif i == 1:
                x = 150
            elif i == 2:
                x = 550
            elif i == 3:
                x = 650
            if i == 4:
                x = 720
            self.items.append(Item(x,0,storeitems[i]))
        if self.round > 2: #Adds in special zombies on occaisons
            for i in range(self.round):
                self.zombies.append("S")
        if self.round > 3:
            for i in range(self.round*2):
                self.zombies.append("E")
        if self.round > 4:
            for i in range(self.round):
                self.zombies.append("T")
        if self.round > 4:
            for i in range(self.round*3):
                self.zombies.append("H")
        if self.round > 5:
            for i in range(int(self.round/3)):
                self.zombies.append("A")
                
        shuffle(self.zombies) #Randomizes the order zombies come in
        for enemy in dead:
            enemy.alpha = 0

class Player: #The main Player class
    def __init__(self,x,y,hp,speed,name):#Taking in and defining common vars
        self.x = x
        self.y = y
        self.hp = hp
        self.dead = False
        self.speed = speed
        self.initspeed = speed
        self.name = name
        self.pic = image.load("gfx/player/"+self.name+"P.png")
        self.ang = 0
        self.midx = 0
        self.midy = 0
        self.primary = weapons["M4A1"] #Certain instance of Weapon class
        self.secondary = weapons["USP"]
        self.melee = weapons["Machete"]
        self.weapon = self.primary
        self.shots = []
        self.rect = None
        self.killed = []
        self.reloading = False
        self.width = self.pic.get_width()
        self.height = self.pic.get_height()
        self.ready = 0
        self.grens = 200
        self.grenready = 0
        self.reloadready = 1
        self.pickready = 1
        self.legpos = 0
        self.bloody = 255
        self.grenades = []
        self.key = [K_w,K_s,K_a,K_d]
        self.money = 0
        self.armor = 0
        self.blood = gfx['Bloodscreen']
        self.bloody = 0
        self.nukes = 1
        
    def update(self): #The main method used to change character's attributes
        self.moving = False
        if self.hp < 0:
            self.dead = True
        self.midx = self.x +self.pic.get_rect()[2]//2
        self.midy = self.y - self.pic.get_rect()[3]//2
        self.ang = atan2(my-self.y,mx-self.x)
        self.newpic = rotate(self.pic,self.ang,1,1) #Adjusting picture to suit
        self.gunx = self.x + 16*cos(self.ang)
        self.guny = self.y + 16*sin(self.ang)
        self.keys = key.get_pressed()

        self.lleg = rotate(legs["L"+str(floor(self.legpos))],self.ang,1,1)
        self.rleg = rotate(legs["R"+str(floor(self.legpos))],self.ang,1,1)
        self.legpos += 0.1

        if self.legpos > 4: #Reset switcher for the legs' movement
            self.legpos = 0
        self.rect = Rect(self.x-16,self.y-16,32,32)

        if self.pickready < 0: #Resets switcher for pickup, later stops spamming
            self.pickready = 0

        if self.keys[K_w]:
            if self.collidecheck(0,-self.speed): #Calls method to check collision
                self.y -= self.speed #If nothing collides, it moves
                self.moving = True
                
        if self.keys[K_s]:
            if self.collidecheck(0,self.speed):
                self.y += self.speed
                self.moving = True
                
        if self.keys[K_d]:
            if self.collidecheck(self.speed,0):
                self.x += self.speed
                self.moving = True
                
        if self.keys[K_a]:
            if self.collidecheck(-self.speed,0):
                self.x -= self.speed
                self.moving = True
                
        if self.keys[K_e] and self.pickready == 0: #Picking up items
            for item in menu.items: #Iterates through the list and finds distance
                item.dist = sqrt((item.pickx-self.x)**2+(item.picky-self.y)**2)
                if item.dist < 35 and item.picked != True:

                    if item.name in weapons.keys(): #Equips item if in range
                        if weapons[item.name].slot == "P" or weapons[item.name].slot == "Ps":
                            self.weapon = weapons[item.name]
                            self.primary = weapons[item.name]
                        elif weapons[item.name].slot == "S":
                            self.weapon = weapons[item.name]
                            self.secondary = weapons[item.name]
                    elif item.name.lower() == "pammo": #Changes the player attributes accordingly
                        self.primary.ammo = self.primary.fullclip*6
                    elif item.name.lower() == "sammo":
                        self.secondary.ammo = self.secondary.fullclip*6
                    elif item.name.lower() == "speed":
                        self.initspeed += 0.1
                    elif item.name.lower() == "medkit": #Each item has its own use to the player
                        if self.hp < 100:
                            self.hp = 100
                        else: self.hp += 10
                        self.alpha = 0 
                    elif item.name.lower() == "he":
                        self.grens += 1
                    elif item.name.lower() == "lightarmor":
                        if self.money > 500:
                            self.armor = 20
                            self.money -= 500
                        else: break
                    elif item.name.lower() == "armor":
                        if self.money > 2000:
                            self.armor = 35
                            self.money -= 2000
                        else: break
                    elif item.name.lower() == "heavyarmor":
                        if self.money > 5000:
                            self.armor = 50
                            self.money -= 5000
                        else: break
                    elif item.name.lower() == "superarmor":
                        if self.money > 10000:
                            self.armor = 75
                            self.money -= 10000
                        else: break
                    elif item.name.lower() == "nuke":
                        if self.money > 5000:
                            self.nukes += 1
                            self.money -= 5000
                        else: break
                    sounds['Pickup'].play() #Plays a sound to indicate pickup
                    item.picked = True
                    self.pickready = 1
                    break
                
        if numkeys(self.keys,self.key) > 1: #Sees how many direction keys are pressed
            self.speed = sqrt(2*self.initspeed**2)/2 #Prevents faster diagonal movement
        else:
            self.speed = self.initspeed
        
        if self.keys[K_g] and self.grenready == 0 and self.grens > 0:
            self.grenades.append(Grenade("HE",100,100,image.load("gfx/weapons/HE.bmp"),self.x,self.y,self.ang,1))
            self.grens -= 1 #Used to lob grenades around the map
            self.grenready = 1
            
        if self.keys[K_r]: #Reloading for the currently equipped weapon
            if self.weapon.ammo > 0 and self.weapon.clip < self.weapon.fullclip:
                self.reloading = True

        if self.legpos > 3 or self.moving != True: #Changes leg position
            self.legpos = 0

        if self.keys[K_1]: #Change through weapons
            self.weapon = self.primary
        if self.keys[K_2]:
            self.weapon = self.secondary
        if self.keys[K_3]:
            self.weapon = self.melee
            
        self.changestance() #Change model to accomodate weapon

        if self.reloading == True:
            if self.weapon.reload():
                self.reloading = False
        
        self.newgun = rotate(self.weapon.pic,self.ang,1,1)
        self.pickready -= (1/20)
        self.shoot()
        if self.armor != 0:
            self.armorpic = rotate(armor[str(self.armor)],self.ang,1,1)
        self.blood = gfx['Bloodscreen']
        self.bloody -= 3
        
    def shoot(self): #Method used to launch bullets from the player
        self.removelist = []
        self.removegren = []
        mb = mouse.get_pressed()
        self.ready -= (1/self.weapon.speed)
        self.grenready -= (1/40)
        if self.ready < 0:
            self.ready = 0
        if self.grenready < 0:
            self.grenready = 0
        #Adding in Bullet class instances
        if mb[0] == 1 and self.ready == 0 and self.weapon.clip > 0 and self.weapon.reloadready == 1:
            if self.weapon.slot == "Ps":
                for i in range(-3,3,1): #Adds in extra bullets for shotgun
                    self.shots.append(Bullet(self.weapon.dmg,self.gunx,self.guny,self.ang+radians(2*i),10,1))
            else: self.shots.append(Bullet(self.weapon.dmg,self.gunx,self.guny,self.ang,20,1))
            self.weapon.clip -= 1
            self.weapon.sound.play()
            self.ready = 1
        elif mb[0] == 1 and self.ready == 0 and self.weapon.slot != "M":
            sounds['Click'].play() #Special conditions for the knife
            self.ready = 1
        if mb[0] == 1 and self.ready == 0 and self.weapon.slot == "M":
            self.shots.append(Bullet(self.weapon.dmg,self.gunx,self.guny,self.ang,20,1))
            self.weapon.sound.play()
            self.ready = 1
        
        for shot in self.shots: #Iterate through bullets and updates them
            shot.update()
            shot.dist = sqrt((shot.x1-self.midx)**2+(shot.y1-self.midy)**2)
            self.maxdist = 1000
            if self.weapon.slot == "Ps":
                self.maxdist = 200
            if self.weapon.slot == "M":
                self.maxdist = 50
                shot.display = False
            if shot.dist > self.maxdist: #Removes bullet if out of range
                self.removelist.append(shot)
            elif shot.kill:
                self.removelist.append(shot)
        for delete in self.removelist: #Deletes bullet from list
            self.shots.remove(delete)
        for grenade in self.grenades: #Updates grenades and removes if necessary
            grenade.update()
            if grenade.kill:
                self.removegren.append(grenade)
        for delete in self.removegren:
            self.grenades.remove(delete)
        
    
    
    def changestance(self): #Change model to accomodate weapon       
        if self.weapon.slot == "P" or self.weapon.slot == "Ps":
            self.pic = image.load("gfx/player/"+self.name+"P"+".png")
        elif self.weapon.slot == "S":
            self.pic = image.load("gfx/player/"+self.name+self.weapon.slot+".png")
        elif self.weapon.slot == "M":
            self.pic = image.load("gfx/player/"+self.name+self.weapon.slot+".png")
        if self.reloading:
            self.pic = image.load("gfx/player/"+self.name+"R"+".png")
            
    def collidecheck(self,horiz,vert): #Checking collide with mask.png
        if inrange(self.x,self.y): #Uses the color Green for walls
            if mask.get_at((int(self.x + horiz+16*(horiz/self.speed)),int(self.y +vert+16*(vert/self.speed)))) == ((0,255,0)):
                return False
            else: return True
            
    def draw(self): #Draws only aspects of the player (Bullets, grenades,etc.)
        screen.blit(self.lleg,(halfer(self.x,self.lleg,1),halfer(self.y,self.lleg,2)))
        screen.blit(self.rleg,(halfer(self.x,self.rleg,1),halfer(self.y,self.rleg,2)))
        screen.blit(self.newgun,(halfer(self.gunx,self.newpic,1),halfer(self.guny,self.newpic,2)))
        screen.blit(self.newpic,(halfer(self.x,self.newpic,1),halfer(self.y,self.newpic,2)))
        if self.bloody > 0:
            self.blood.set_colorkey((255,255,255))
            self.blood.set_alpha((self.bloody))
            screen.blit(self.blood,(0,0))
        if self.armor != 0:
            screen.blit(self.armorpic,(halfer(self.x,self.armorpic,1),halfer(self.y,self.armorpic,2)))
        for shot in self.shots:
            if shot.display:
                shot.draw()
        for grenade in self.grenades:
            grenade.draw()
        
        
        
        

class Enemy: #Main Class for all enemies in the game
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
        self.hp = zombies[name][0] #Gets attributes of zombie
        self.speed = zombies[name][1]
        self.money = zombies[name][2]
        self.dmg = zombies[name][3]
        self.pic = zombies[name][4]
        self.ang = 0
        self.legpos = 0
        self.dead = False
        self.ready = 0
        self.attackspeed = (1/50)
        self.blood = 1
        self.alpha = 255
        self.width = self.pic.get_rect()[2]
        self.height = self.pic.get_rect()[3]
        self.shots = []
        self.grenades = []
        self.removegren = []
        self.rect = Rect(self.x-self.width //2,self.y-self.height//2,self.width,self.height)

    def move(self): #Gets the enemy moving towards the player
        if self.hp < 0:
            self.dead = True
        self.lleg = rotate(legs["L"+str(floor(self.legpos))],self.ang,1,1)
        self.rleg = rotate(legs["R"+str(floor(self.legpos))],self.ang,1,1)
        #Gets appropriate coordinates and angle
        self.midx = self.x + self.pic.get_rect()[2]//2
        self.midy = self.y + self.pic.get_rect()[3]//2
        self.rect = Rect(self.x-16,self.y-16,32,32)
        self.ang = atan2(guy.y-self.y,guy.midx-self.midx)
        self.newpic = rotate(self.pic,self.ang,1,1)
        self.gunx = self.x + 16*cos(self.ang)
        self.guny = self.y + 16*sin(self.ang)
        self.legx = self.x - 0.5*cos(self.ang)
        self.legy = self.y - 0.5*sin(self.ang)
        keys = key.get_pressed()

        
        self.rect = Rect(self.x-self.width //2,self.y-self.height//2,self.width,self.height)
        self.dist = sqrt((self.x-guy.x)**2+(self.y-guy.y)**2)
        #Repelling formula to prevent group clustering/clumping
        
        self.dx = (guy.x-self.x)/self.dist
        self.dy = (guy.y-self.y)/self.dist
        self.vx = self.speed*self.dx
        self.vy = self.speed*self.dy
        self.vx -= 20*(guy.x-self.x)/(self.dist**2) #Change velocity according
        self.vy -= 20*(guy.y-self.y)/(self.dist**2) #to repelling forces

        for enemy in enemies:
            if enemy != self: #Repelling zombies from others
                dx = self.x - enemy.x
                dy = self.y - enemy.y
                dist = sqrt(dx**2 + dy**2)
                if dist**2 > 0:
                    self.vx += 10*dx/dist**2
                    self.vy += 10*dy/dist**2

        if self.name == "A":
            if self.dist < 75:
                self.speed = zombies[self.name][1]*3
            if self.dist < 26:
                self.legpos = 0
                self.attack()
            else:
                self.x += self.vx
                self.y += self.vy
                self.legpos += 0.05
                if self.legpos > 3:
                    self.legpos = 0
            if self.dist > 100:
                self.speed = zombies[self.name][1]
                
                
        if self.name not in ["S","A"]: #Differentiates ranges for Normal and Soldiers
            if self.dist > 26: #Stops when range is reach
                self.x += self.vx
                self.y += self.vy
                self.legpos += 0.05
                if self.legpos > 3:
                    self.legpos = 0
            else:
                self.legpos = 0
                self.attack() #Begins attack once in range
        
        elif self.name == "S":
            if self.dist > 100:
                self.x += self.vx
                self.y += self.vy
                self.legpos += 0.05
                if self.legpos > 3:
                    self.legpos = 0
            else:
                self.legpos = 0
                self.attack()
        self.removelist = []
        for shot in self.shots: #Updates bulllets of the Soldier Enemy
            shot.update()
            shot.dist = sqrt((shot.x1-self.midx)**2+(shot.y1-self.midy)**2)
            self.maxdist = 100
            if shot.kill:
                self.removelist.append(shot)
            elif shot.dist > self.maxdist:
                self.removelist.append(shot)
        for delete in self.removelist:
            self.shots.remove(delete)
        for grenade in self.grenades: # "Grenades" for self-destruction
            if grenade.kill:
                self.removegren.append(grenade)
        for delete in self.removegren:
            self.grenades.remove(delete)
            
    def draw(self): 
        if self.dead: #Draws a pool of blood instead of enemy
            screen.blit(self.newpic,(halfer(self.x,self.newpic,1),halfer(self.y,self.newpic,2)))
            self.shots = []
        else:
            if self.name != "H":
                screen.blit(self.lleg,(halfer(self.legx,self.lleg,1),halfer(self.legy,self.lleg,2)))
                screen.blit(self.rleg,(halfer(self.legx,self.rleg,1),halfer(self.legy,self.rleg,2)))
            screen.blit(self.newpic,(halfer(self.x,self.newpic,1),halfer(self.y,self.newpic,2)))
        for shot in self.shots:
            if shot.display:
                shot.draw()
        for grenade in self.grenades:
            grenade.update()
            if grenade.kill == False:
                grenade.draw()
                
    def attack(self):
        self.ready -= self.attackspeed # Attack with appropriate method
        if self.ready < 0:             # Depends on zombie type
            self.ready = 0
        if self.ready == 0:
            if self.name in ["N","T","H","A"]:
                guy.hp -= self.dmg*((100-guy.armor)/100)
                guy.bloody = 255
                sounds['Zmhit'].play()
                self.ready = 1
            elif self.name == "E":
                self.grenades.append(Grenade("HE",self.dmg,100,image.load("gfx/weapons/HE.bmp"),self.x,self.y,0,0))
                self.ready = 1000
            elif self.name == "S":
                weapons['MP5'].sound.play()
                self.shots.append(Bullet(self.dmg,self.gunx,self.guny,self.ang,20,0))
                self.ready  = 1
                
    def die(self): #Changes picture to a pool of blood instead
        if self.dead and self.blood > 0 and menu.pause == -1:
            self.alpha -= 1
            self.blood -= (1/255)
            self.newpic = rotate(gfx['Blood'],self.ang,1,0)
            self.newpic.set_alpha((self.alpha))

        
        

class Weapon: #Main Weapon Class
    def __init__(self,slot,price,dmg,clip,speed,pic,sound): #Important attributes
        self.slot = slot
        self.price = price
        self.dmg = dmg
        self.fullclip = clip
        self.clip = clip
        self.pic = pic
        self.sound = sound
        self.range = 0
        self.speed = 50/(speed/60)
        self.ready = 0
        self.shots = []
        self.clipin = mixer.Sound("sfx/weapons/w_clipin.wav")
        self.clipout = mixer.Sound("sfx/weapons/w_clipout.wav")
        self.reloadready = 1
        self.ammo = self.clip *6
        
    def reload(self): #Reloading of the gun, straightforward
        if self.clip < self.fullclip and self.slot != "M":
            if self.reloadready == 1: 
                self.clipout.play()
            self.reloadready -= 0.02
            if self.reloadready < 0:
                self.clipin.play()
                if (self.ammo - self.fullclip) >= 0:
                    self.ammo -= self.fullclip
                    self.ammo += self.clip
                    self.clip = self.fullclip
                    self.reloadready = 1
                elif self.ammo-self.fullclip <= self.fullclip:
                    self.clip = self.ammo
                    self.ammo = 0
                    self.reloadready = 1
                return True



class Bullet: #The main Class for bullet projectiles
    def __init__(self,dmg,x1,y1,ang,speed,source):
        self.dmg = dmg
        self.x1 = x1
        self.y1 = y1
        self.ang = ang
        self.speed = speed
        self.kill = False
        self.display = True
        self.source = source
        
    def update(self): #Moving the bullet towards the angle
        self.x1 += self.speed*cos(self.ang)
        self.y1 += self.speed*sin(self.ang)
        self.x2 = self.x1 + 15 *cos(self.ang)
        self.y2 = self.y1 + 15 *sin(self.ang)
        
        for enemy in enemies: #Stops when collision with enemy
            if enemy.rect.collidepoint((self.x1,self.y1)):
                enemy.hp -= self.dmg #Damages enemy
                if enemy.hp > 0 and enemy.name != "T":
                    enemy.x += self.dmg/2*cos(self.ang)
                    enemy.y += self.dmg/2*sin(self.ang)
                self.kill = True
                self.display = False
                sounds["Zmattack"+str(randint(1,4))].play()
                break
            
        if self.source == 0: #Checks source from enemy or player
            if guy.rect.collidepoint((self.x1,self.y1)):
                guy.hp -= self.dmg*((100-guy.armor)/100) #Soldier bullets can collide with player
                guy.bloody = 255
                guy.x += self.dmg*2*cos(self.ang)
                guy.y += self.dmg*2*sin(self.ang)
                self.kill = True
                self.display = False
                
        if inrange(self.x2,self.y2):
            if mask.get_at((int(self.x2),int(self.y2))) == ((0,255,0)):
                self.kill = True
                self.display = False
                
    def draw(self):
        if self.display and self.kill != True: #Draw lines with anti-aliasing
            draw.aaline(screen,(255,0,100),(int(self.x1),int(self.y1)),(int(self.x2),int(self.y2)))

class Item: #Class for items that may be dropped
    def __init__(self,x,y,name):
        self.x = x
        self.y = y
        self.name = name
        self.pic = image.load("gfx/weapons/"+name.lower()+"_d.bmp")
        self.newpic = rotate(self.pic,0,0,1)
        self.alpha = 255
        self.picked = False
        self.pickx = self.x + self.pic.get_rect()[2]//2
        self.picky = self.y + self.pic.get_rect()[3]// 2
        
    def draw(self):
        screen.blit(self.newpic,(self.x,self.y))
        
    def disappear(self):
        self.alpha -= 5
        self.newpic.set_alpha((int(self.alpha)))
        
class Grenade: #Class for throwable Grenades
    def __init__(self,slot,dmg,delay,pic,x,y,ang,source):
        self.slot = slot
        self.delay = delay
        self.x = x
        self.y = y
        self.dmg = dmg
        self.pic = pic
        self.sound = sounds["Explosion"]
        self.source = source
        self.mx,self.my = mouse.get_pos()
        self.ang = atan2(my-self.y,mx-self.x)
        self.moving = True
        self.kill = False
        self.explode = 0
        self.rotang = 0
        self.radius = 100
        self.dmg = 200
        
    def update(self): #Updates position of the object
        if self.source == 0 and self.moving:
            self.mx = self.x
            self.my = self.y
            for enemy in enemies:
                distance = sqrt((enemy.x-self.x)**2+(enemy.y-self.y)**2)
                if distance < self.radius:
                    enemy.hp -= self.dmg-distance #Damages based on distance
            guy.hp -= self.dmg/4*((100-guy.armor)/100)
            guy.bloody = 255
            self.moving = False
            
        if self.source == 1 and self.moving: #Checks for 'source'
            self.newpic = rotate(self.pic,self.rotang,1,1)
            self.x += 5*cos(self.ang)
            self.y += 5*sin(self.ang)
            self.dist = sqrt((self.x-self.mx)**2+(self.y-self.my)**2)
            self.rotang += radians(20)
            if self.dist <= 5:
                self.moving = False
                self.sound.play()
                for enemy in enemies:
                    distance = sqrt((enemy.x-self.x)**2+(enemy.y-self.y)**2)
                    if distance < self.radius:
                        enemy.hp -= self.dmg-distance
                        
        if self.moving == False and self.kill == False:
            self.explode += 0.3
            self.newpic = rotate(explosions[str(floor(self.explode))],0,1,0)
            if self.explode > 9.6:
                self.kill = True
    def draw(self):
        screen.blit(self.newpic,(halfer(self.x,self.newpic,1),halfer(self.y,self.newpic,2)))

def rotate(img,ang,deg,col): #Rotate images to an angle
    if col == 1: #Also includes transparency options, black or magenta
        col = (255,0,255) #Deg allows for rotation if images are facing up or side
    elif col == 0:
        col = (0,0,0)
    elif col == 2:
        col = (255,255,255)
    img.set_colorkey(col)
    return transform.rotate(img,-degrees(ang) - deg *90)

def halfer(var,pic,coord): #Changes coordinates to prevent resizing of images
    return var - pic.get_rect()[1+coord]//2

def numkeys(keys,target): #Grabs the number of movement keys pressed
    tot = 0
    for key in target: #Allows for movement diagonally with proper speed
        if keys[key]:
            tot += 1
    return tot

def inrange(x,y): #Makes sure points are valid for rect collision
    if x < width and y < height and x > 0 and y > 0:
        return True
    else: return False

def savegame():
    primary = list(weapons.values()).index(guy.primary) #Finding name of equipped 
    secondary = list(weapons.values()).index(guy.secondary) #Weaponry
    save = open("save.txt","w") #Opening file for IO
    save.write("guy.x = " + str(guy.x)+"\n")
    save.write("guy.y = " + str(guy.y)+"\n")
    save.write("guy.gunx = " + str(guy.gunx)+"\n")
    save.write("guy.guny = " + str(guy.guny)+"\n")
    save.write("guy.hp = " + str(guy.hp)+"\n") #Saving key attributes
    save.write("guy.grens = " + str(guy.grens)+"\n")
    save.write("guy.money = " + str(guy.money)+"\n")
    save.write("guy.initspeed = " + str(guy.initspeed)+"\n")
    save.write("guy.armor = " + str(guy.armor)+"\n")
    save.write("guy.nukes = " + str(guy.nukes)+"\n")
    save.write("guy.primary = weapons['" + str((list(weapons.keys())[primary]))+"']\n")
    save.write("guy.primary.clip  = " + str(guy.primary.clip)+"\n")
    save.write("guy.primary.ammo = " + str(guy.primary.ammo)+"\n")
    save.write("guy.secondary = weapons['" + str((list(weapons.keys())[secondary]))+"']\n")
    save.write("guy.secondary.clip  = " + str(guy.secondary.clip)+"\n")
    save.write("guy.secondary.ammo = " + str(guy.secondary.ammo)+"\n")
    save.write("enemies = [] \n")
    save.write("dead = [] \n")
    for enemy in enemies: #Getting and placing all enemies as they were
        save.write("enemies.append(Enemy(%s,%s,'%s')) \n" %(str(enemy.x),str(enemy.y),str(enemy.name)))
    save.write("menu.items = [] \n")
    for item in menu.items: #Doing the same for items
        if item.picked != True:
            save.write("menu.items.append(Item(%s,%s,'%s')) \n" %(str(item.x),str(item.y),str(item.name)))
    save.write("menu.round = " +str(menu.round)+"\n")
    save.write("menu.zombies = " +str(menu.zombies)+"\n")
    save.close()

def nuke(): #Eradicates all enemies on the map
    menu.nukealpha = 170
    for enemy in enemies:
        enemy.dead = True
    sounds["Explosion"].play()

def drawhud():
    nuke = image.load("gfx/screens/nuke.png").convert()
    nuke.set_colorkey((255,255,255))
    nuke = transform.scale(nuke,(48,48))
    health = image.load("gfx/screens/healthicon.jpg")
    health.set_colorkey((255,255,255))
    health = transform.scale(health,(48,48))
    armor = image.load("gfx/screens/armoricon.jpg")
    armor.set_colorkey((255,255,255))
    money = image.load("gfx/screens/moneyicon.png").convert()
    money.set_colorkey((0,0,0))
    grenade = image.load("gfx/screens/grenadeicon.jpg")
    grenade.set_colorkey((255,255,255))
    screen.blit(health,(0,550))
    screen.blit(myFont.render((str(int(guy.hp))),1,(0,0,0)),(55,555))
    screen.blit(armor,(140,550))
    screen.blit(myFont.render((str(guy.armor)),1,(0,0,0)),(195,555))
    screen.blit(nuke,(240,550))
    screen.blit(myFont.render((str(guy.nukes)),1,(0,0,0)),(295,555))
    screen.blit(grenade,(470,550))
    screen.blit(myFont.render((str(guy.grens)),1,(0,0,0)),(515,555))
    screen.blit(money,(600,550))
    screen.blit(myFont.render((str(guy.money)),1,(0,0,0)),(650,555))
def killcheck():
    for killed in dead:
        if killed.blood > 0: #Allows for the pool of blood to drain
            killed.die()
            killed.draw()
        if killed in enemies:
            sounds["Zmdie"].play()
            drop = randint(1,15)
            if drop > 12: #Randomly choose (or not to) drop an item or weapon
                if drop < 15:
                    menu.items.append(Item(killed.x,killed.y,choice(fullitems)))
                elif drop == 15:
                    menu.items.append(Item(killed.x,killed.y,choice(list(weapons))))
############menu.items.append(Item(killed.x,killed.y,choice(armoritems)))
            guy.money += killed.money #Give the player money for the kill
            enemies.remove(killed)
            
    for enemy in enemies:
        if menu.pause == -1: #Stop movement when screen is paused
            enemy.move()
        if enemy.dead:
            dead.append(enemy)
        else: enemy.draw()
        
    for item in menu.items:
        if item.picked:
            item.disappear() #Allows for cool fade effect for weapons
            if item.alpha == 0:
                menu.deaditems.append(item)
        elif item.alpha == 0:
            if item not in menu.deaditems:
                menu.deaditems.append(item)
        item.draw()
        
    for deaditem in menu.deaditems: #Removes picked up weapons from list
        if deaditem in menu.items:
            menu.items.remove(deaditem)
    


weapons = { #Dictionary of weapons corresponding to instance of weapon class
    'USP': Weapon("S",500,24,12,166,image.load("gfx/weapons/usp"+".bmp"),mixer.Sound("sfx/weapons/usp.wav")),
    'Glock': Weapon("S",400,21,20,166,image.load("gfx/weapons/glock"+".bmp"),mixer.Sound("sfx/weapons/glock18.wav")),
    'Deagle': Weapon("S",650,34,7,100,image.load("gfx/weapons/deagle"+".bmp"),mixer.Sound("sfx/weapons/deagle.wav")),
    'P228': Weapon("S",600,22,13,166,image.load("gfx/weapons/p228"+".bmp"),mixer.Sound("sfx/weapons/p228.wav")),
    'Elite': Weapon("S",1000,22,15,187,image.load("gfx/weapons/elite"+".bmp"),mixer.Sound("sfx/weapons/elite.wav")),
    'FiveSeven': Weapon("S",750,21,20,214,image.load("gfx/weapons/fiveseven"+".bmp"),mixer.Sound("sfx/weapons/fiveseven.wav")),


    'AK47': Weapon("P",2500,22,30,500,image.load("gfx/weapons/ak47"+".bmp"),mixer.Sound("sfx/weapons/ak47.wav")),
    'SG552': Weapon("P",3500,24,30,375,image.load("gfx/weapons/sg552"+".bmp"),mixer.Sound("sfx/weapons/sg552.wav")),
    'M4A1': Weapon("P",3100,22,30,500,image.load("gfx/weapons/m4a1"+".bmp"),mixer.Sound("sfx/weapons/m4a1.wav")),
    'AUG': Weapon("P",3500,24,30,375,image.load("gfx/weapons/aug"+".bmp"),mixer.Sound("sfx/weapons/aug.wav")),			
    'Galil': Weapon("P",2000,13,35,500,image.load("gfx/weapons/galil"+".bmp"),mixer.Sound("sfx/weapons/galil.wav")),
    'Famas': Weapon("P",2250,14,25,500,image.load("gfx/weapons/famas"+".bmp"),mixer.Sound("sfx/weapons/famas.wav")),


    'MP5': Weapon("P",1500,13,30,500,image.load("gfx/weapons/mp5"+".bmp"),mixer.Sound("sfx/weapons/mp5.wav")),
    'TMP': Weapon("P",1250,9,30,750,image.load("gfx/weapons/tmp"+".bmp"),mixer.Sound("sfx/weapons/tmp.wav")),
    'P90': Weapon("P",2350,11,50,750,image.load("gfx/weapons/p90"+".bmp"),mixer.Sound("sfx/weapons/p90.wav")),
    'Mac10': Weapon("P",1400,9,30,750,image.load("gfx/weapons/mac10"+".bmp"),mixer.Sound("sfx/weapons/mac10.wav")),
    'UMP45': Weapon("P",1700,13,25,375,image.load("gfx/weapons/ump45"+".bmp"),mixer.Sound("sfx/weapons/ump45.wav")),
    
    'Scout': Weapon("P",2750,45,10,75,image.load("gfx/weapons/scout"+".bmp"),mixer.Sound("sfx/weapons/scout.wav")),
    'AWP': Weapon("P",4750,400,10,23,image.load("gfx/weapons/awp"+".bmp"),mixer.Sound("sfx/weapons/awp.wav")),
    'G3SG1': Weapon("P",5000,32,30,250,image.load("gfx/weapons/g3sg1"+".bmp"),mixer.Sound("sfx/weapons/g3sg1.wav")),
    'SG550': Weapon("P",4200,30,30,250,image.load("gfx/weapons/sg550"+".bmp"),mixer.Sound("sfx/weapons/sg550.wav")),


    'M3': Weapon("Ps",1700,26,8,75,image.load("gfx/weapons/m3"+".bmp"),mixer.Sound("sfx/weapons/m3.wav")),
    'XM1014': Weapon("Ps",3000,22,7,125,image.load("gfx/weapons/xm1014"+".bmp"),mixer.Sound("sfx/weapons/xm1014.wav")),


    'Machete': Weapon("M",0,75,0,100,image.load("gfx/weapons/machete"+".bmp"),mixer.Sound("sfx/weapons/machete_hit.wav")),


}
explosions = {}
legs = {}
for i in range(0,10):
    explosions[str(i)] = image.load("gfx/weapons/explosion" + str(i)+".png")
    if i < 4:
        legs["L"+str(i)] = image.load("gfx/guys/leg"+str(i)+"1.png")
        legs["R"+str(i)] = image.load("gfx/guys/leg"+str(i)+"2.png")

sounds = { #Organizing common sound files
    'Hit1': mixer.Sound("sfx/player/hit1.wav"),
    'Hit2': mixer.Sound("sfx/player/hit2.wav"),
    'Hit3': mixer.Sound("sfx/player/hit3.wav"),
    'Click': mixer.Sound("sfx/weapons/click.wav"),
    'Pickup': mixer.Sound("sfx/items/pickup.wav"),
    'Zmhit': mixer.Sound("sfx/player/zm_hit.wav"),
    'Zmdie': mixer.Sound("sfx/player/zm_die.wav"),
    'Zmattack1': mixer.Sound("sfx/player/zm_attack1.wav"),
    'Zmattack2': mixer.Sound("sfx/player/zm_attack2.wav"),
    'Zmattack3': mixer.Sound("sfx/player/zm_attack3.wav"),
    'Zmattack4': mixer.Sound("sfx/player/zm_attack4.wav"),
    'Explosion': mixer.Sound("sfx/weapons/explode2.wav")
}

gfx = {
    'Blood': image.load("gfx/npc/blood.png"),
    'Bloodscreen': image.load("gfx/player/blood.png").convert()
}

zombies = { #Attributes: Health, Speed, Money, Damage, Picture
    'N': [50,2,100,5,image.load("gfx/npc/classiczombie.bmp")],
    'S': [50,2,200,3,image.load("gfx/npc/soldier.bmp")],
    'E': [50,2,150,80,image.load("gfx/npc/exploder.png")],
    'T': [300,1,500,10,image.load("gfx/npc/tank.png")],
    'H': [15,4,100,3,image.load("gfx/npc/headcrab.bmp")],
    'A': [150,1.5,500,15,image.load("gfx/npc/alien.bmp")]
    }

armor = {
    '20': image.load("gfx/weapons/lightarmor.bmp"),
    '35': image.load("gfx/weapons/armor.bmp"),
    '50': image.load("gfx/weapons/heavyarmor.bmp"),
    '75': image.load("gfx/weapons/superarmor.bmp")
    }

fullitems = ["Pammo","Sammo","Medkit","Speed","HE"]
storeitems = ["Lightarmor","Armor","Heavyarmor","Superarmor","Nuke"]
AK47 = Item(100,400,"Deagle")
Pammo = Item(200,400,"Pammo")
Sammo = Item(300,400,"Sammo")
Medkit = Item(400,400,"Medkit")
Speed = Item(500,400,"Speed")
Gren = Item(600,400,"HE")
guy = Player(400,300,100,4,"swat")
menu = Menu("start")
mask = image.load("gfx/screens/mask.png")
load = -1
dead = []
enemies = []
background = image.load("gfx/screens/map.png").convert()
start = image.load("gfx/screens/start.png").convert()
diedpic = image.load("gfx/screens/deadpic.jpg").convert()

click = False
while menu.running:
    for e in event.get():
        if e.type == QUIT:
            menu.running = False
        if e.type == MOUSEBUTTONDOWN:
            click = True
        if e.type == KEYDOWN:
            if chr(e.key) == "p":
                menu.pause *= -1
            if chr(e.key) == "z":
                savegame()
            
            if chr(e.key) == "b":
                if guy.nukes > 0:
                    nuke()
                    guy.nukes -= 1
    if load == 1:
        save = open("save.txt","r")
        for i in save.read().strip().split("\n"):
            exec(i)
        save.close()
        for enemy in enemies:
            enemy.move()
        load = -1
    
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    menu.update()
    myClock.tick(50)
    click = False
    if guy.dead:
        for alpha in range(255,0,-1):
            screen.fill((0,0,0))
            diedpic.set_alpha(alpha)
            screen.blit(diedpic,(0,0))
        guy = Player(400,300,100,4,"swat")
        menu = Menu("start")
        enemies = []
        items = []
        guy.dead = False
quit()
