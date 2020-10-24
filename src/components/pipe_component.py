import pygame, neat, time, os, random
from configs.global_vars import *

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