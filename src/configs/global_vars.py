WIN_WIDTH = 500
WIN_HEIGHT = 800

import pygame,os

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