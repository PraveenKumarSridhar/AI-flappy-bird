import pygame, neat, time, os, random
from configs.global_vars import *

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