import pygame, random, pyautogui

from pygame.locals import *
pygame.init()

font=pygame.font.SysFont("Arial", 40)
font2=pygame.font.SysFont("Arial", 120)
WIDTH, HEIGHT = pyautogui.size()
print(pyautogui.size())
ground_scroll=0
scroll_speed=2
screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
background_img=pygame.image.load("bg.png")
background_img=pygame.transform.scale(background_img, (WIDTH, HEIGHT))
ground_img=pygame.image.load("ground.png")
ground_img=pygame.transform.scale(ground_img, (WIDTH+100, HEIGHT/5))
flying=False
gameover=False
gap=270
pipefrequency=2500 #milisecond
score = 0
passpipes = False

lastpipe=pygame.time.get_ticks()-pipefrequency

# 1 is top pipe, -1 is bottom pipe
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pipe.png")
        self.rect=self.image.get_rect()
        if position==1:
            self.image=pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft=[x, y]
        elif position==-1:
            self.rect.topleft=[x, y+gap]
        
    def update(self):
        self.rect.x-=scroll_speed
        if self.rect.right<0:
            self.kill()



class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        self.index=0
        self.counter=0
        for i in range(3):
            img=pygame.image.load(f"bird{i+1}.png")
            self.images.append(img)
        self.image=self.images[self.index]
        self.rect=self.image.get_rect()
        self.rect.center=[x, y]
        self.velocity=0
    def update(self):
        if flying:
            self.velocity += 0.5
            if self.velocity > 8:
                self.velocity=8
            if self.rect.bottom<700:
                self.rect.y+=self.velocity
        if not gameover:
            if pygame.mouse.get_pressed()[0]==True :
                self.velocity=-10
            self.counter+=1
            flapdown=5
            if self.counter>flapdown:
                self.counter=0
                self.index+=1
                if self.index>=len(self.images):
                    self.index=0
            self.image=self.images[self.index]
            self.image = pygame.transform.rotate(self.images[self.index], self.velocity)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)

birdgroup=pygame.sprite.Group()
bird1=Bird(100, HEIGHT/2)
birdgroup.add(bird1)     
pipegroup=pygame.sprite.Group()

def drawtext(text, font, color, x, y):
    announce=font.render(text, True, color)
    screen.blit(announce, (x, y))


run = True
while run:
    screen.blit(background_img, (0,0))
    birdgroup.draw(screen)
    pipegroup.draw(screen)
    birdgroup.update()
    screen.blit(ground_img, (ground_scroll, HEIGHT-200))
    if bird1.rect.bottom>=HEIGHT-200:
        gameover = True
        flying = False
    if len(pipegroup)>0: # get finish on current pipe before proceed to next pipe in which index resets.
        if birdgroup.sprites()[0].rect.left>pipegroup.sprites()[0].rect.left and birdgroup.sprites()[0].rect.right<pipegroup.sprites()[0].rect.right and passpipes==False: #if bird is in the middle
            passpipes=True #passpipes means only when the bird is in the middle and or the end (have just exited)
        if passpipes:
            if birdgroup.sprites()[0].rect.left>pipegroup.sprites()[0].rect.right:  # if bird had COMPLETELY exited the pipe
                score += 1
                passpipes=False
    drawtext(f"Score={score}", font, "white", 20, 20)
    if pygame.sprite.groupcollide(birdgroup, pipegroup, False, False) or bird1.rect.top<0: # parameter False, False is to destroy the obj, respectively
        gameover=True
    if not gameover :
        # print(pygame.time.get_ticks())
        timenow=pygame.time.get_ticks()
        if timenow-lastpipe>pipefrequency:
            pipeheight=random.randint(200, 500)
            bottompipe=Pipe(WIDTH, pipeheight, -1)
            toppipe=Pipe(WIDTH, pipeheight, 1)
            pipegroup.add(bottompipe)
            pipegroup.add(toppipe)
            lastpipe=timenow
        pipegroup.update()
        ground_scroll-=scroll_speed
        if ground_scroll<-35:
            ground_scroll=0
    for i in pygame.event.get():
        if i.type==pygame.QUIT:
            pygame.quit()
            run = False
        if i.type == pygame.MOUSEBUTTONDOWN and not flying and gameover == False:
            flying=True
    if gameover:
        # screen.fill("black")
        drawtext("Gameover.", font2, "red", WIDTH/2, HEIGHT/2)
    pygame.display.update()
pygame.quit()