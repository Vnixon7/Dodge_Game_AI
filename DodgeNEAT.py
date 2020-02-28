import pygame, random, neat, os

pygame.init ()
pygame.font.init ()
win_w = 500
win_h = 500
win = pygame.display.set_mode ((win_w, win_h))
clock = pygame.time.Clock ()
score_font = pygame.font.SysFont ('comicsans', 35)


class player:
    def __init__(self):
        self.x = 235
        self.y = 400
        self.vel = 10
        self.left = 0
        self.right = 0
        self.width = 50
        self.height = 50

    def draw(self):
        pygame.draw.rect (win, (0, 0, 0), (self.x, self.y, self.width, self.height))

    def getRect(self):
        return pygame.Rect (self.x, self.y, 50, 50)

    def moveLeft(self):
        self.x -= 10
        #self.left = True
        #self.right = False

    def moveRight(self):
        self.x += 10
        #self.right = True
        #self.left = False


class projectile:
    def __init__(self):
        self.x = random.randint (50, 450)
        self.y = 0
        self.vel = 10
        self.hit = False

    def draw(self):
        pygame.draw.rect (win, (0, 255, 0), (self.x, self.y, 50, 50))

    def set_pos(self):
        pass

    def move(self):
        self.y += self.vel

    def get_Rect(self):
        return pygame.Rect (self.x, self.y, 50, 50)


def draw_window(players, project, score):
    win.fill ((255, 255, 255))
    for play in players:
        play.draw ()
    for p in project:
        p.draw ()
    text = score_font.render (('Score: ' + str (int (score))), 1, (0, 0, 0))
    win.blit (text, (0, 15))
    alive_label = score_font.render ("Alive: " + str (len (players)), 1, (215, 0, 215))
    win.blit(alive_label,(0,50))
    pygame.display.update ()

#main fitness function
def main(genomes, config):
    global win, gen
    nets = []
    ge = []
    players = []

    #implementing NEAT
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create (genome, config)
        nets.append (net)
        players.append (player ())
        genome.fitness = 0
        ge.append (genome)

    project = [projectile ()]
    clock = pygame.time.Clock ()
    score = 0

    #Main loop
    run = True
    while run:
        #FPS
        clock.tick (30)

        #if x out quit application
        for event in pygame.event.get ():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit ()
                quit ()

        #if all players died start new generation
        if len (players) > 0:
            run = True

        else:

            break
        #inputs for activation function
        for x, play in enumerate (players):
            for p in project:
                ydis_from_p = play.y - p.y + 50
                rxdis_from_p = play.x + p.x - 50
                lxdis_from_p = play.x - p.x + 50
                rdis_wall = play.x - 500 - play.width
                output = nets[players.index (play)].activate (
                    (play.x, play.y, p.x, p.y, abs (play.y - 50), ydis_from_p,rxdis_from_p,lxdis_from_p,rdis_wall,win_w))
                #move right add fitness for survival
                if output[0] >= 0 and play.x < 500 - 50:
                    ge[x].fitness += 1
                    play.moveRight ()
                #move left add fitness for survival
                if output[0] < 0 and play.x > 0 + 15:
                    ge[x].fitness += 1
                    play.moveLeft ()

                #checking the activation function tanh
                #print ('output 0: ', output[0])


                #move the projectiles
                p.move ()

                #if projectile passes main block add fitness
                if p.y == 450:
                    p.y = 0
                    p.x = random.randint (0, 500)
                    score += 1
                    ge[x].fitness += 10

                #if main block is under projectile block take away fitness
                if p.x == play.x:
                    ge[x].fitness -= 10

                if p.get_Rect ().colliderect (play.getRect ()) or play.x < 0 or play.x > 500:
                    # print ('GameOver')
                    # p.vel = 0
                    # play.vel = 0
                    ge[x].fitness -= 20
                    players.pop (x)
                    nets.pop (x)
                    ge.pop (x)

        draw_window (players, project, score)


def run(config_file):
    config = neat.config.Config (neat.DefaultGenome, neat.DefaultReproduction,

                                 neat.DefaultSpeciesSet, neat.DefaultStagnation,

                                 config_file)

    p = neat.Population (config)
    p.add_reporter (neat.StdOutReporter (True))
    stats = neat.StatisticsReporter ()
    p.add_reporter (stats)
    winner = p.run (main, 500)
    print ('\nBest genome:\n{!s}'.format (winner))


if __name__ == '__main__':
    local_dir = os.path.dirname (__file__)

    config_path = os.path.join (local_dir, 'NEAT.txt')

    run (config_path)
