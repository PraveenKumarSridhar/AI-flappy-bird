import pygame, neat, time, os, random
from configs.global_vars import *

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

