import pygame, neat, time, os, random,pickle
from configs.global_vars import *
from components.bird_component import *
from components.pipe_component import *
from components.base_component import *

GEN = 0

def draw_window (win,birds,pipes,base,score, gen):
    win.blit(BG_IMG,(0,0))

    for pipe in pipes:
        pipe.draw(win)
    
    text = STAT_FONT.render("Score : "+str(score),1,(255,255,255))
    win.blit(text,(WIN_WIDTH- 10 - text.get_width(),10))

    text = STAT_FONT.render("Generation : "+str(gen),1,(255,255,255))
    win.blit(text,(10,10))

    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()

def fitness_function(genomes,config):
    global GEN
    GEN += 1

    nets = []  # neural networks that control each bird in the pop.
    ge = []    # to eval their fitness to see how far they moved and if they hit a pipe and so on.
    birds = [] # induvidual birds in the pop.

    for _, g in genomes: #genomes -> (genome_id,genome_obj)
        net = neat.nn.FeedForwardNetwork.create(g, config) # init the net wrt the bird
        nets.append(net) 
        birds.append(Bird(230,350)) # init the bird
        g.fitness = 0 # init the fitness for this genome/ the network for the corresponding bird.
        ge.append(g)

    base = Base(730)
    pipes = [Pipe(600)]

    run = True
    win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0 # GAME SCORE

    # GAME LOOP
    while run and len(birds) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break 

        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        # else:
        #     run = False
        #     break
        
        for index, bird in enumerate(birds):
            ge[index].fitness += 0.1
            bird.move()
            output = nets[index].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom))) 
            if output[0] > 0.50: # output is a list of prob for each o/p neuron, in this case len(output) = 1.
                bird.jump()
        base.move()
        
        rem = []
        add_pipe = False
        for pipe in pipes:
            for index, bird in enumerate(birds):
                if pipe.collide(bird):
                    ge[index].fitness -= 1 # its gonna a penalize a bird when it hits a pipe by 1.
                    birds.pop(index) 
                    nets.pop(index)
                    ge.pop(index)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0: #check if the pipe is off screen.
                rem.append(pipe)

            pipe.move()

        if add_pipe:
            for g in ge:
                g.fitness += 5 # award more points for birds that pass through the pipes.
            score += 1
            pipes.append(Pipe(600))
        
        for r in rem:
            pipes.remove(r)
        
        for index, bird in enumerate(birds):
            if bird.y + bird.img.get_height() - 10 >=  730 or bird.y < -50: # if bird move all they above the screen or hit the base.
                birds.pop(index) # lack of penalization as bird did not hit the pipe. 
                nets.pop(index)
                ge.pop(index)

        draw_window(win,birds,pipes,base,score,GEN)
        # break if score gets large enough
        '''
        if score > 20:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break
        '''

def run(config_path):
    # The headers of sorts in the txt file are the params we are feeding in.
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,neat.DefaultSpeciesSet,neat.DefaultStagnation,config_path)

    # Create the population.
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    
    winner = p.run(fitness_function,50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,'configs','config-feedforward.txt')
    run(config_path)


