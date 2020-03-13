import pygame, random, neat, os, pickle, math

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
        self.disE = [100]
        self.disM = [100]
        self.disX = [100]

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

            elif self.img_count == 2:

                self.img = self.R_imgs[1]

            elif self.img_count == 4:

                self.img = self.R_imgs[2]

            elif self.img_count == 6:

                self.img = self.R_imgs[3]
            elif self.img_count == 8:

                self.img = self.R_imgs[4]
            elif self.img_count == 10:

                self.img = self.R_imgs[5]
                self.img_count = 0

        if self.left:
            if self.img_count == 0:

                self.img = self.L_imgs[0]

            elif self.img_count == 2:

                self.img = self.L_imgs[1]

            elif self.img_count == 4:

                self.img = self.L_imgs[2]

            elif self.img_count == 6:

                self.img = self.L_imgs[3]

            elif self.img_count == 8:

                self.img = self.L_imgs[4]

            elif self.img_count == 10:

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

    def Xdis(self, p1):
        if p1.x > self.x:
            DisXP1 = p1.x - self.x
        else:
            DisXP1 = self.x - p1.x

        return DisXP1


class projectile:

    def __init__(self):
        self.x = random.randint(50, win_w - 50)
        self.y = 0
        self.width = 50
        self.height = 145
        self.vel = 10
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
        return pygame.Rect(self.x, self.y, 50, 50)


def draw_window(players, project1, score):
    win.fill((255, 255, 255))
    for play in players:
        play.draw()
    for p in project1:
        p.draw()
    text = score_font.render(('Score: ' + str(int(score))), 1, (0, 0, 0))
    win.blit(text, (0, 15))
    alive_label = score_font.render("Alive: " + str(len(players)), 1, (215, 0, 215))
    win.blit(alive_label, (0, 50))
    pygame.display.update()


newNum = 700
gen = 0
DisProjectP1 = 0


# main fitness function
def main(genomes, config):
    global win, gen, newNum, DisProjectP1
    nets = []
    ge = []
    players = []

    # implementing NEAT
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        players.append(player())
        genome.fitness = 0
        ge.append(genome)
    p1 = projectile()

    project1 = [p1]

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
            for p1 in project1:

                DistEuclideanP1 = math.sqrt((play.x - p1.x) ** 2 + (play.y - p1.y) ** 2)
                DisManhattanP1 = abs(play.x - p1.x) + abs(play.y - p1.y)

                DisYP1 = play.y + play.height - p1.y
                Xdis = play.Xdis(p1)
                play.disE.append(int(DistEuclideanP1))
                play.disM.append(DisManhattanP1)
                play.disX.append(Xdis)

                output = nets[players.index(play)].activate(
                    (play.x, play.y, p1.x, p1.y, DisManhattanP1, DistEuclideanP1, play.width, play.height,
                     p1.width, p1.height, Xdis, DisYP1))

                # move the projectiles
                for p in project1:
                    p.move()

                # moving right
                if output[0] > 0 and output[1] < 0:
                    # ge[x].fitness += 0.05
                    play.moveRight()
                # moving left
                if output[0] < 0 and output[1] > 0:
                    # ge[x].fitness += 0.05
                    play.moveLeft()

                # standing
                if output[0] == 0 and output[1] == 0:
                    # ge[x].fitness += 0.05
                    play.stand = True
                    play.right = False
                    play.left = False
                    play.x += 0

                # checking the activation function tanh
                # print ('output 0: ', output[0])

                # if projectile passes main block add fitness
                if p1.y == 450:
                    p1.x = random.randint(15, 485)
                    p1.y = 0
                    score += 1
                    ge[x].fitness += 10
                    # if projectile passes main block add fitness

                # print('MANHATTAN: ', DisManhattanP1)
                # print('EUCLIDEAN: ', DistEuclideanP1)
                if DisManhattanP1 < 220 and DistEuclideanP1 < 180 and Xdis < 85:
                    ge[x].fitness -= 1

                if p1.get_Rect().colliderect(play.getRect()):
                    # print ('GameOver')
                    # p.vel = 0
                    # play.vel = 0
                    ge[x].fitness -= 20
                    players.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    gen += 1

                # pop out on other side of screen if screen exceeded
                if play.x >= win_w - play.width and play.right:
                    play.x = 12
                if play.x <= 11 and play.left:
                    play.x = win_w - play.width - 1

        draw_window(players, project1, score)

        # saving best model
        if score > newNum:
            pickle.dump(nets[0], open("best3.pickle", "wb"))
            newNum += 15

            break


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,

                                neat.DefaultSpeciesSet, neat.DefaultStagnation,

                                config_file)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 1500)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)

    config_path = os.path.join(local_dir, 'NEAT.txt')

    run(config_path)
