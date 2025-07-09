import pygame, random

from pygame.locals import *

WIDTH, HEIGHT = 500, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ninja Escape")
groundscroll = 0
scrollspeed = 2
score=0
hurdlesfrequency=1500 # miliseconds
flying = False
passhurdles = False
gameover = False
background_img = pygame.image.load("orangesky.jpg")
land_img = pygame.image.load("tanah.png")

class Hurdles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("hurdles.png")
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x -= scrollspeed
        if self.right.rect<0:
            self.kill

class Ninja(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # initialize sprite
        self.images = []
        self.index = 0
        self.counter = 0
        for i in range(3):
            img = pygame.image.load(f"bird{i+1}.png") # every Ninja(+1, 2, 3).png images
            self.images.append(img) #don't forget to always append
        self.image = self.images[self.index] # the img displayed will follow the flow of self.images in the count of index.
        self.rect = self.image.get_rect() # get the rect of the image
        self.rect.center = [x,y]
        self.velocity = 0 # function?
        
        def update(self):
            if flying:
                self.velocity += 0.5
                print(self.velocity, self.y)
                # if self.velocity > 8:
                    # self.velocity = 8
                if self.rect.bottom < 700:
                    self.rect.y += self.velocity # drags down
            if not gameover: # not gameover vs flying? 
                if pygame.mouse.get_pressed()[0]==True:
                    self.velocity-=10 # lifts the ninja up
                self.counter+=1
                flapdown = 5 # berapa lama setiap frame itu.
                if self.counter > flapdown:
                    self.counter = 0 # durasi untuk 1 frame sebelum berganti
                    self.index+= 1 # after finishing one frame, move to the next one with index's help
                    if self.index>=len(self.images): # function?
                        self.index = 0 # resets pictures's next index to move on
                self.image = self.images[self.index]
                self.image = pygame.tramsform.rotate(self.images[self.index], self.velocity)
            else:
                self.image = pygame.transform.rotate(self.images[self.index], -90) # why is it red
        
ninjagroup = pygame.sprite.Group() # what's the function?
ninja1 = Ninja(100, HEIGHT/2) # function? why only ninjaONE? not ninja2 ninja3 also?
ninjagroup.add(ninja1)
hurdlesgroup = pygame.sprite.Group()

run = True
while run:
    screen.blit(background_img, (0,0))
    ninjagroup.draw(screen)
    hurdlesgroup.draw(screen)
    ninjagroup.update()
    screen.blit(background_img, (groundscroll, 700)) # meaning?
    if ninja1.rect.bottom>=700:
        gameover = True
        flying = False
    if len(hurdlesgroup)>0: # get finish on current hurdle before proceed to next hurdle in which index resets.
        if ninjagroup.sprites()[0].rect.left>hurdlesgroup.sprites()[0].rect.left and hurdlesgroup.sprites()[0].rect.right<pipegroup.sprites()[0].rect.right and passpipes==False: #if bird is in the middle
            passpipes=True #passpipes means only when the bird is in the middle and or the end (have just exited)
        if passpipes:
            if hurdlesgroup.sprites()[0].rect.left>hurdlesgroup.sprites()[0].rect.right:  # if bird had COMPLETELY exited the pipe
                score += 1
                passpipes=False
    if pygame.sprite.groupcollide(ninjagroup, hurdlesgroup, False, False) or ninja1.rect.top<0: # parameter False, False is to destroy the obj, respectively
        gameover=True
    if not gameover :
        print(pygame.time.get_ticks())
        timenow=pygame.time.get_ticks()
        if timenow-lasthurdles>hurdlesfrequency:
            lasthurdles=timenow
        hurdlesgroup.update()
        ground_scroll-=scrollspeed
        if ground_scroll<-100:
            ground_scroll=0
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            pygame.quit()
            run = False
        if i.type == pygame.MOUSEBUTTONDOWN and not flying and gameover == False: #
            flying=True
        
    pygame.display.update()
pygame.quit()