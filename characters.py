#!/usr/bin/python

"""A character"""

import math

import pygame
from pygame.locals import *
from pygame.compat import geterror

import random

from constant import *
from pvector import PVector

class Bounds:
    @staticmethod
    def outside(x, y):
        if Bounds.top_out(x) \
            or Bounds.bottom_out(x) \
            or Bounds.left_out(y) \
            or Bounds.right_out(y):
            return True
        else:
            return False

    @staticmethod
    def top_out(x):
        return x < (0 - 20)

    @staticmethod
    def bottom_out(x):
        return x > (Constant.SCREEN_WIDTH + 20)

    @staticmethod
    def left_out(y):
        return y < (0 - 20)

    @staticmethod
    def right_out(y):
        return y > (Constant.SCREEN_HEIGHT + 20)


def random_direction():
    if random.randint(0, 1) == 0:
        return -1
    else:
        return 1


class Point(pygame.sprite.Sprite):
    def __init__(self, position, color = Color("blue"), width = 3, height = 3):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.center = position

class Player(pygame.sprite.Sprite):

    animation_cycle = 30

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = pygame.Surface([16, 16])
        self.image.fill(Color("blue"))

        self.rect = self.image.get_rect()

        self.pos_x = Constant.SCREEN_WIDTH/2
        self.pos_y = Constant.SCREEN_HEIGHT/2

        self.speed = 5

        self.image = self.images[0]
        self.rect = self.images[0].get_rect()
        self.rect.move_ip(Constant.SCREEN_RECT.width/2, Constant.SCREEN_RECT.bottom)
        self.mask = pygame.mask.from_surface(self.image)
        self.frame = 0

        self.angle = 0
        self.turn()

    @property
    def position(self):
        return (self.pos_x, self.pos_y)

    def move(self, direction):

        if direction == "up":
            self.pos_y -= self.speed
        elif direction == "down":
            self.pos_y += self.speed
        elif direction == "left":
            self.pos_x -= self.speed
        elif direction == "right":
            self.pos_x += self.speed

        # if Bounds.top_out(self.pos_x):
        #     self.pos_x = 8

        # if Bounds.bottom_out(self.pos_y):
        #     self.pos_x = Constant.SCREEN_HEIGHT - 8

        # if Bounds.left_out(self.pos_y):
        #     self.pos_y = 8

        # if Bounds.right_out(self.pos_y):
        #     self.pos_y = Constant.SCREEN_WIDTH - 8

    def turn(self):
        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(mouse_pos[0] - self.pos_x,  mouse_pos[1] - self.pos_y) + math.pi
        self.angle = angle * 57.2957795 # Radians to degrees

    def update(self):
        self.turn()
        self.frame = pygame.time.get_ticks()

        self.rect.center = (self.pos_x, self.pos_y)
        self.rect = self.rect.clamp(Constant.SCREEN_RECT)
        self.image = self.images[self.frame//self.animation_cycle % 2 + 2]
        self.image = pygame.transform.rotate(self.image, self.angle)
        # print self.angle


class Crosshairs(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = pygame.Surface([10, 10])
        pygame.draw.circle(self.image, Color("white"), (4, 4), 4, 0)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Enemy(pygame.sprite.Sprite):
    respawn = 600
    limit = 50
    animation_cycle = 120
    image_data = {}
    images = [0,0]
    rects = {}

    def __init__(self, player_pos, visual, close, mover, chaser, fastie):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.pos = [0, 0]
        if close:
            self.pos[0] = player_pos[0] * random_direction() + random.randint(70, 100)
            self.pos[1] = player_pos[1] * random_direction() + random.randint(70, 100)
        else:
            self.pos[0] = player_pos[0] * random_direction() + random.randint(300, 500)
            self.pos[1] = player_pos[1] * random_direction() + random.randint(300, 500)

        if visual == "blob":
            self.images = Enemy.image_data['blob']
        elif visual == "butterfly":
            self.images = Enemy.image_data['butterfly']
        else:
            self.images = Enemy.image_data['blob']

        self.image = self.images[0]

        # if visual == "blob":
        #     self.image = Enemy.images['blob']
        # elif visual == "butterfly":
        #     self.image = Enemy.images['butterfly']
        # elif visual == "octopus":
        #     self.image = Enemy.images['octopus']
        # else:
        #     self.image = Enemy.images['blob']

        self.rect = self.image.get_rect()
        self.rect.move_ip(Constant.SCREEN_RECT.width/2, Constant.SCREEN_RECT.bottom)
        self.mask = pygame.mask.from_surface(self.image)
        self.frame = 0

        # self.image = pygame.Surface([20, 20])
        # pygame.draw.circle(self.image, Color("red"), (10, 10), 10, 0)

        self.rect.center = (self.pos[0], self.pos[1])

        self.close = close
        self.mover = mover
        self.chaser = chaser
        self.fastie = fastie
        if fastie:
            self.speed = random.randint(2,4)
        else:
            self.speed = 1

        self.direction = None
        GameState.enemies_spawned += 1

    def move(self, player_pos):

        mouse_pos = pygame.mouse.get_pos()
        angle = math.atan2(player_pos[0] - self.pos[0],  player_pos[1] - self.pos[1]) + math.pi
        self.angle = angle * 57.2957795 # Radians to degrees

        if Bounds.outside(self.pos[0], self.pos[1]) or self.chaser:
            self.direction = PVector(player_pos[0], player_pos[1]) - PVector(self.pos[0], self.pos[1])
        else:
            self.direction = PVector(random.randint(0,640), random.randint(0,480)) - PVector(self.pos[0], self.pos[1])

        self.direction.normalize()
        self.direction.mag = self.speed

        self.pos[0] = self.pos[0] + self.direction.x * self.direction.mag
        self.pos[1] = self.pos[1] + self.direction.y * self.direction.mag

    def update(self):
        self.frame = pygame.time.get_ticks()
        self.rect.center = (self.pos[0], self.pos[1])
        self.image = self.images[self.frame//self.animation_cycle % 2]
        self.image = pygame.transform.rotate(self.image, self.angle)

    @property
    def value(self):
        value = 1
        if self.close:
            value += 1

        if self.mover:
            value += 2

        if self.fastie:
            value *= 2

        if self.chaser:
            value += 3

        return value

class Bullet(pygame.sprite.Sprite):

    strong = 240
    fast = 240
    spread = 6000

    def __init__(self, origin, direction, speed, type):
        pygame.sprite.Sprite.__init__(self, self.containers)

        if type == "fast":
            self.image = Bullet.fastimage
            self.rect = self.image.get_rect()
        elif type == "strong":
            self.image = Bullet.strongimage
            self.rect = Bullet.strongrect
        else:
            self.image = Bullet.fastimage
            self.rect = Bullet.fastrect

        self.rect = self.image.get_rect()

        self.origin = PVector(origin[0], origin[1])
        self.aim = PVector(direction[0], direction[1])

        self.direction = self.aim - self.origin
        self.direction.mag = speed

        self.pos = [0, 0]

        self.pos[0] = self.origin[0]
        self.pos[1] = self.origin[1]

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (self.pos[0], self.pos[1])

    def update(self):
        self.pos[0] = self.pos[0] + self.direction.x * self.direction.mag
        self.pos[1] = self.pos[1] + self.direction.y * self.direction.mag
        # print self.pos[0], self.pos[1]
        self.rect.center = (self.pos[0], self.pos[1])

        if Bounds.outside(self.pos[0], self.pos[1]):
            self.kill()

