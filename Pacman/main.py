import pygame, sys, random, math, time
from pygame.locals import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.pacman = pygame.image.load("pacman.png")
        # self.pacman = pygame.transform.scale(self.pacman, (25, 25))
        self.rect = self.pacman.get_rect()
        # self.prev_position = self.rect.x, self.rect.y
        self.power = False
        self.n = 500
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # out of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width-200:
            self.rect.right = width-200
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height
        if pygame.sprite.spritecollideany(self, walls):
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, 5)
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, -5)
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(5, 0)
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(-5, 0)
        if pygame.sprite.spritecollideany(self, specialballs):
            self.power = True
            self.n = 500
        if self.n == 0:
            self.power = False
            self.n = 500

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.ball = pygame.image.load("ball.png")
        self.ball = pygame.transform.scale(self.ball, (10, 10))
        self.rect = self.ball.get_rect(center=(random.randint(0, width-200), random.randint(0, height)))
    def update(self, score):
        if pygame.sprite.collide_rect(self, walls[0]):
            self.kill()
        if pygame.sprite.collide_rect(self, walls[1]):
            self.kill()
        if pygame.sprite.collide_rect(self, walls[2]):
            self.kill()
        if pygame.sprite.collide_rect(self, player):
            self.kill()
            score[0] += 1

class SpecialBall(pygame.sprite.Sprite):
    def __init__(self):
        super(SpecialBall, self).__init__()
        self.special = pygame.image.load("special.png")
        self.special = pygame.transform.scale(self.special, (13, 13))
        self.rect = self.special.get_rect(center=(random.randint(0, width-200), random.randint(0, height)))
    def update(self, score):
        if pygame.sprite.collide_rect(self, walls[0]):
            self.kill()
        if pygame.sprite.collide_rect(self, walls[1]):
            self.kill()
        if pygame.sprite.collide_rect(self, walls[2]):
            self.kill()
        if pygame.sprite.collide_rect(self, player):
            self.kill()
            score[0] += 3

class Wall():
    def __init__(self):
        self.x = random.randrange(0, 300)
        self.y = random.randrange(0, 300)
        self.surface = pygame.Surface((self.x, self.y))
        self.surface.fill(blue)
        self.rect = self.surface.get_rect(center=(random.randrange(self.x//2+35, 800-(self.x//2+35)), random.randrange(self.y//2+35, height-(self.y//2+35))))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.number = random.randint(0, 20)
        self.enemy = pygame.image.load("orange.png")
        if self.number >= 15:
            self.enemy = pygame.image.load("pink.png")
        elif self.number >= 10:
            self.enemy = pygame.image.load("red.png")
        elif self.number >= 5:
            self.enemy = pygame.image.load("blue.png")
        self.enemy = pygame.transform.scale(self.enemy, (20, 20))
        self.pos_x = random.randint(0, width-200)
        self.pos_y = random.randint(0, height)
        self.rect = self.enemy.get_rect(center=(self.pos_x, self.pos_y))
        self.angle = 0
        self.speed = 0
        self.speed_x = 0
        self.speed_y = 0
        self.dx = 0
        self.dy = 0
        self.change = False
        while pygame.sprite.spritecollideany(self, walls):
            self.pos_x = random.randint(0, width-200)
            self.pos_y = random.randint(0, height)
            self.rect = self.enemy.get_rect(center=(self.pos_x, self.pos_y))
    def update(self, score):
        self.pos_x = self.rect.x
        self.pos_y = self.rect.y
        self.dx, self.dy = player.rect.x - self.pos_x, player.rect.y - self.rect.y
        if player.power:
            self.angle = math.atan2(self.dy, self.dx) - 180
            self.speed = 4
        else:
            self.angle = math.atan2(self.dy, self.dx)
            self.speed = 3
            if self.change:
                self.enemy = pygame.image.load("orange.png")
                if self.number >= 15:
                    self.enemy = pygame.image.load("pink.png")
                elif self.number >= 10:
                    self.enemy = pygame.image.load("red.png")
                elif self.number >= 5:
                    self.enemy = pygame.image.load("blue.png")
                self.enemy = pygame.transform.scale(self.enemy, (20, 20))
                self.change = False
        self.speed_x = self.speed * math.cos(self.angle)
        self.speed_y = self.speed * math.sin(self.angle)
        self.rect.x += int(self.speed_x)
        self.rect.y += int(self.speed_y)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width-200:
            self.rect.right = width-200
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height
        if pygame.sprite.spritecollideany(self, walls):
            self.rect.x = self.pos_x
            self.rect.y = self.pos_y
        if pygame.sprite.collide_rect(self, player):
            if player.power == False:
                score[0] = -1
            else:
                if self.change == False:
                    self.enemy = pygame.transform.scale(self.enemy, (5, 5))
                    self.change = True
                    score[0] += 10

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super(Food, self).__init__()
        self.number = random.randint(0, 20)
        self.fruit = pygame.image.load("banana.png")
        if self.number >= 10:
            self.fruit = pygame.image.load("strawberries.png")
        self.fruit = pygame.transform.scale(self.fruit, (20, 20))
        self.rect = self.fruit.get_rect(center=(random.randint(0, width-200), random.randint(0, height)))
    def update(self, score):
        if pygame.sprite.collide_rect(self, walls[0]):
            self.kill()
        if pygame.sprite.collide_rect(self, walls[1]):
            self.kill()
        if pygame.sprite.collide_rect(self, walls[2]):
            self.kill()
        if pygame.sprite.collide_rect(self, player):
            self.kill()
            score[0] += 5

pygame.init()
clock = pygame.time.Clock()

size = width, height = 1000, 600
black = 0, 0, 0
blue = 0, 200, 200
game = 1

table = pygame.Surface((200, 600))
table.fill(blue)
rectangle = table.get_rect(center=(900, 300))

score = [0]
font = pygame.font.SysFont(None, 55)
font1 = pygame.font.SysFont(None, 150)

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Pacman')
player = Player()

balls = pygame.sprite.Group()
for i in range(40):
    balls.add(Ball())

specialballs = pygame.sprite.Group()
for i in range(4):
    specialballs.add(SpecialBall())

food = pygame.sprite.Group()
for i in range(4):
    food.add(Food())

walls = []
for i in range(3):
    walls.append(Wall())

enemies = pygame.sprite.Group()
for i in range(5):
    enemies.add(Enemy())


while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    balls.update(score)
    specialballs.update(score)
    food.update(score)
    enemies.update(score)
    screen.fill(black)
    screen.blit(table, rectangle)

    for b in balls:
        screen.blit(b.ball, b.rect)
    for s in specialballs:
        screen.blit(s.special, s.rect)
    for w in walls:
        screen.blit(w.surface, w.rect)
    for e in enemies:
        screen.blit(e.enemy, e.rect)
    for f in food:
        screen.blit(f.fruit, f.rect)
    screen.blit(player.pacman, player.rect)


    if player.power:
        text = font.render("POWER", True, (255, 0, 0))
        screen.blit(text, (830, 100))
        player.n -= 1


    if score[0] == -1:
        text = font1.render("GAME OVER", True, (255, 0, 0))
        clock.tick(30)
        screen.blit(text, (125, 200))
        game = 0
    else:
        text = font.render("Score: " + str(score[0]), True, (255, 255, 255))
        screen.blit(text, (810, 200))

    if len(balls.sprites()) == 0:
        text = font1.render("YOU WON!", True, (0, 255, 0))
        clock.tick(30)
        screen.blit(text, (125, 200))
        game = 0

    pygame.display.update()
    clock.tick(60)


pygame.quit()
quit()