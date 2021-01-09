import pygame, random, neat, os, pickle

pygame.init()
pygame.font.init()
win_w = 500
win_h = 500
win = pygame.display.set_mode((win_w, win_h))
clock = pygame.time.Clock()
score_font = pygame.font.SysFont('comicsans', 35)
projectile_imgs = [pygame.transform.scale(pygame.image.load("fireballsxl1.png"), (50, 145)),
                   pygame.transform.scale(pygame.image.load("fireballsxl2.png"), (50, 145)),
                   pygame.transform.scale(pygame.image.load("fireballsxl3.png"), (50, 145))]


class player:
    def __init__(self):
        self.x = 235
        self.y = 400
        self.vel = 10
        self.left = False
        self.right = False
        self.stand = False
        self.width = 50
        self.height = 50
        self.img_count = 0

        self.R_imgs = [pygame.transform.scale(pygame.image.load('right1.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('right2.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('right3.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('right4.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('right5.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('right6.jpg'), (self.height, self.width))]
        self.L_imgs = [pygame.transform.scale(pygame.image.load('left1.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('left2.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('left3.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('left4.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('left5.jpg'), (self.height, self.width)),
                       pygame.transform.scale(pygame.image.load('left6.jpg'), (self.height, self.width))]
        self.img = self.R_imgs[0]

    def draw(self):
        # pygame.draw.rect (win, (0, 0, 0), (self.x, self.y, self.width, self.height))
        self.img_count += 1
        if self.right:
            if self.img_count == 0:

                self.img = self.R_imgs[0]

            elif self.img_count == 1:

                self.img = self.R_imgs[1]

            elif self.img_count == 2:

                self.img = self.R_imgs[2]

            elif self.img_count == 3:

                self.img = self.R_imgs[3]
            elif self.img_count == 4:

                self.img = self.R_imgs[4]
            elif self.img_count == 5:

                self.img = self.R_imgs[5]
                self.img_count = 0

        if self.left:
            if self.img_count == 0:

                self.img = self.L_imgs[0]

            elif self.img_count == 1:

                self.img = self.L_imgs[1]

            elif self.img_count == 2:

                self.img = self.L_imgs[2]

            elif self.img_count == 3:

                self.img = self.L_imgs[3]

            elif self.img_count == 4:

                self.img = self.L_imgs[4]

            elif self.img_count == 5:

                self.img = self.L_imgs[5]
                self.img_count = 0

        if self.stand:
            self.img = self.L_imgs[0]
            self.img_count = 0

        win.blit(self.img, (self.x, self.y))

    def getRect(self):
        return pygame.Rect(self.x, self.y, 50, 50)

    def moveLeft(self):
        self.x -= 10
        self.left = True
        self.right = False
        self.stand = False

    def moveRight(self):
        self.x += 10
        self.right = True
        self.left = False
        self.stand = False


class projectile:

    def __init__(self):
        self.x = random.randint(50, 450)
        self.y = 0
        self.width = 50
        self.height = 145
        self.vel = 15
        self.ANIMATION_TIME = 5
        self.img_count = 0
        self.IMGS = projectile_imgs
        self.img = self.IMGS[0]

    def draw(self):
        # pro_img = pygame.image.load ('knife.jpg')
        # pro_img = pygame.transform.scale (pro_img, (50, 70))
        # win.blit (pro_img, (self.x, self.y))
        # pygame.draw.rect (win, (0, 255, 0), (self.x, self.y, 50, 50))
        self.img_count += 1
        if self.img_count == 0:

            self.img = self.IMGS[0]

        elif self.img_count == 2:

            self.img = self.IMGS[1]

        elif self.img_count == 3:

            self.img = self.IMGS[2]
            self.img_count = 0

        win.blit(self.img, (self.x, self.y))

    def set_pos(self):
        pass

    def move(self):
        self.y += self.vel

    def get_Rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


def draw_window(players, project, score):
    win.fill((255, 255, 255))
    for play in players:
        play.draw()
    for p in project:
        p.draw()
    text = score_font.render(('Score: ' + str(int(score))), 1, (0, 0, 0))
    win.blit(text, (0, 15))
    alive_label = score_font.render("Alive: " + str(len(players)), 1, (215, 0, 215))
    win.blit(alive_label, (0, 50))
    pygame.display.update()


gen = 0
newNum = 1000


# main fitness function
def main(genomes, config):
    global win, gen, newNum
    nets = []
    ge = []
    players = []
    load_in = open('BEST!(2).pickle', 'rb')
    bestNet = pickle.load(load_in)

    # implementing NEAT
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        # nets.append(net)
        nets.append(bestNet)
        players.append(player())
        genome.fitness = 0
        ge.append(genome)

    project = [projectile()]
    clock = pygame.time.Clock()
    score = 0

    # Main loop
    run = True
    while run:
        # FPS
        clock.tick(23)

        # if x out quit application
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        # if all players died start new generation
        if len(players) > 0:
            run = True

        else:

            break

        # inputs for activation function
        for x, play in enumerate(players):
            for p in project:
                ydis_from_p = play.y - p.y - play.height
                xdis_from_p = abs(play.x + p.x - play.width)
                rdis_wall = play.x - win_w - play.width
                ldis_wall = play.x + play.width
                output = nets[players.index(play)].activate(
                    (play.x, play.y, p.x, p.y, abs(play.y + p.height), ydis_from_p, xdis_from_p, rdis_wall, ldis_wall,
                     win_w, play.width, play.height, p.width, p.height))

                # move right add fitness for survival
                if output[0] > 0 and output[1] > 0 and play.x < win_w - play.width:
                    # ge[x].fitness += 0.5
                    play.moveRight()
                if output[0] > 0 and output[1] < 0 and play.x < win_w - play.width:
                    # ge[x].fitness += 0.5
                    play.moveRight()
                if output[0] > 0 and play.x < win_w - play.width:
                    # ge[x].fitness += 0.5
                    play.moveRight()

                # move left add fitness for survival
                if output[0] < 0 and output[1] < 0 and play.x > 0 + 15:
                    # ge[x].fitness += 0.5
                    play.moveLeft()
                if output[0] < 0 and output[1] > 0 and play.x > 0 + 15:
                    # ge[x].fitness += 0.5
                    play.moveLeft()
                if output[0] < 0 and play.x > 0 + 15:
                    # ge[x].fitness += 0.5
                    play.moveLeft()

                # standing
                if output[0] == 0 or output[1] == 0:
                    # ge[x].fitness += 0.5
                    play.stand = True
                    play.left = False
                    play.right = False
                    play.x += 0

                # checking the activation function tanh
                # print ('output 0: ', output[0])

                # move the projectiles
                p.move()

                # if projectile passes main block add fitness
                if p.y == win_h - 50:
                    p.y = 0
                    p.x = random.randint(15, win_w - 15)
                    score += 1
                    ge[x].fitness += 10

                # if main block is under projectile block take away fitness
                if xdis_from_p <= 50:
                    ge[x].fitness -= 1

                if p.get_Rect().colliderect(play.getRect()) or play.x < 0 or play.x > win_w:
                    # print ('GameOver')
                    # p.vel = 0
                    # play.vel = 0
                    ge[x].fitness -= 20
                    players.pop(x)
                    nets.pop(x)
                    ge.pop(x)

        draw_window(players, project, score)
        if score > newNum:
            pickle.dump(nets[0], open("BEST!(2).pickle", "wb"))
            newNum += 50

            break


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,

                                neat.DefaultSpeciesSet, neat.DefaultStagnation,

                                config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 500)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)

    config_path = os.path.join(local_dir, 'NEAT.txt')

    run(config_path)
