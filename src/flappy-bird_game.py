import pygame, neat, time, os, random
from configs.global_vars import *

# load the bird images.
BIRDS_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("src","imgs","bird1.png"))),\
    pygame.transform.scale2x(pygame.image.load(os.path.join("src","imgs","bird2.png"))),\
        pygame.transform.scale2x(pygame.image.load(os.path.join("src","imgs","bird3.png")))]
# load the pipe image.
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("src","imgs","pipe.png")))
# load the base image.
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("src","imgs","base.png")))
# load the background image.
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("src","imgs","bg.png")))

pygame.font.init()
STAT_FONT = pygame.font.SysFont("Comicsans",50)

# BIRD class
class Bird:
    IMGS = BIRDS_IMGS
    MAX_ROTATION = 25  # How much the bir is going to tilt up or down.
    ROT_VEL = 20       # How much we are going to rotate every time we tilt the bird.
    ANIMATION_TIME = 5 # How long we are going to show the animation (speed of flaping the wings).
    def __init__(self,x,y):
        self.x = x    # Starting x position
        self.y = y    # Starting y position
        self.tilt = 0 # initial tilt for the bird i.e be horizontal.
        self.tick_count = 0 # figure out the physics
        self.vel = 0        # velocity
        self.height = self.y # needed to move and tilt the bird
        self.img_count = 0   # keep track of the bird image [0,1,2].
        self.img = self.IMGS[0] # the initial bird = bird0.
    
    # method to control the bird to jump up and move upwards.
    def jump(self):
        self.vel = -10.5 # in pygame to move up it req -ve velocity.
        self.tick_count = 0 # keep track when we last jumped.
        self.height = self.y # where the bird jumped from?
    
    # every single frame to move the bird.
    def move(self):
        self.tick_count += 1 # tick happened,frame went by,and we have moved.
        
        d = self.vel*self.tick_count + 1.5*self.tick_count**2 # displacement how many pixels we are moving up or down this frame,this is what we are moving when changing the y position of the bird.
        
        #velocity moving way to far up or down.
        if d >= 16:
            d = 16 # if you're moving down more than 16 just move down by 16.
        if d< 0:
            d-= 2 # if you're moving upward move up a bit more, this is to fine tune our movement.

        self.y = self.y + d # once you found the disp, now actually move the y pos of the img.

        if d < 0 or self.y < self.height + 50: # d<0->moving upwards or (cond)-> every time we jump we keep track where we jump from.
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION # restrict how much it goes up here restrict to 25 when going up
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL  # when going down nose dive to the ground.
    
    def draw (self, win):
        self.img_count += 1 # how many times the game loop has run? how many ticks we have shown one image.
        
        # TODO: Try to optimize
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
        
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME

        rotated_image = pygame.transform.rotate(self.img,self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center) # rotates the image at the center
        win.blit(rotated_image ,new_rect.topleft)

    # get collision for due collisions
    def get_mask(self):
        return pygame.mask.from_surface(self.img)


class Pipe:
    GAP = 200
    VEL = 5
    def __init__(self,x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        # get the image for the pipes
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG,False,True)
        self.PIPE_BOTTOM = PIPE_IMG 

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height-self.PIPE_TOP.get_height() #(x,50-160)->rect(x,-110)
        self.bottom = self.height + self.GAP
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self,win):
        win.blit(self.PIPE_TOP,(self.x,self.top)) # draws the image , here the tuple signifies rectage (len,width)
        win.blit(self.PIPE_BOTTOM,(self.x,self.bottom))

    def collide(self,bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # how far the masks are from each other.
        top_offset = (self.x - bird.x,self.top - round(bird.y))
        bottom_offset = (self.x - bird.x,self.bottom - round(bird.y))

        # point of collision.
        b_point = bird_mask.overlap(bottom_mask,bottom_offset)  #if doesn't collide returns None
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True
        
        return False

class Base:
    VEL  = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        # have 2 base images
        self.x1 -= self.VEL # move both at save vel
        self.x2 -= self.VEL # move both at save vel

        # when one move off screen: cycle it back to the end of the current image on screen (x1 or x2).
        if self.x1 +self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 +self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG,(self.x1,self.y))
        win.blit(self.IMG,(self.x2,self.y))






def draw_window (win,bird,pipes,base,score):
    win.blit(BG_IMG,(0,0))

    for pipe in pipes:
        pipe.draw(win)
    
    text = STAT_FONT.render("Score : "+str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH- 10 - text.get_width(),10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(230,350)
    base = Base(730)
    pipes = [Pipe(600)]

    run = True
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0 # GAME SCORE

    # GAME LOOP
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # bird.move()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass
            
            if pipe.x + pipe.PIPE_TOP.get_width() < 0: #check if the pipe is off screen.
                rem.append(pipe)
            
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True 
            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)
        
        if bird.y + bird.img.get_height() >=  730:
            pass

        base.move()
        draw_window(win,bird,pipes,base,score)

    pygame.quit()
    quit() 

main()


