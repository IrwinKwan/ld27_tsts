#!/usr/bin/python

"""A character"""

import pygame
from pygame.locals import *
from pygame.compat import geterror

import random

from constant import Constant
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
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = pygame.Surface([16, 16])
        self.image.fill(Color("blue"))

        self.rect = self.image.get_rect()

        self.pos_x = Constant.SCREEN_RECT.x/2
        self.pos_y = Constant.SCREEN_RECT.y/2

        self.speed = 5

    def pos(self, position_change):
        self.pos_x += position_change[0]
        self.pos_y += position_change[1]
        self.rect.center = (self.pos_x, self.pos_y)
        self.rect = self.rect.clamp(Constant.SCREEN_RECT)

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

        self.rect.center = (self.pos_x, self.pos_y)

        if Bounds.top_out(self.pos_x) or Bounds.bottom_out(self.pos_y):
            self.pos_x -= self.pos_x

        if Bounds.left_out(self.pos_y) or Bounds.right_out(self.pos_y):
            self.pos_y -=  self.pos_y

        self.rect = self.rect.clamp(Constant.SCREEN_RECT)

class Crosshairs(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.image = pygame.Surface([10, 10])
        pygame.draw.circle(self.image, Color("white"), (4, 4), 4, 0)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_pos, close, mover, chaser, fastie):
        pygame.sprite.Sprite.__init__(self, self.containers)

        self.pos = [0, 0]
        if close:
            self.pos[0] = random_direction() * random.randint(70, 100)
            self.pos[1] = random_direction() * random.randint(70, 100)
        else:
            self.pos[0] = random_direction() * random.randint(300, 500)
            self.pos[1] = random_direction() * random.randint(300, 500)


        if fastie:
            self.speed = random.randint(5,10)
        else:
            self.speed = 2

        self.image = pygame.Surface([20, 20])
        pygame.draw.circle(self.image, Color("red"), (10, 10), 10, 0)
        self.rect = self.image.get_rect()

        self.chaser = chaser
        self.direction = None

    def move(self, player_pos):
        self.direction = None
        if Bounds.outside(self.pos[0], self.pos[1]) or self.chaser:
            # if out of bounds, move toward the player
            self.direction = PVector(player_pos[0], player_pos[1]) - PVector(self.pos_x, self.pos_y)
            self.direction.mag = self.speed
        else:
            # random direction
            self.direction = PVector(player_pos[0], player_pos[1]) - PVector(random.randint(0,640), random.randint(0,480))
            self.direction.mag = self.speed

        self.pos[0] = self.pos[0] + self.direction.x * self.direction.mag
        self.pos[1] = self.pos[1] + self.direction.y * self.direction.mag

    def update(self):
        self.rect.center = (self.pos[0], self.pos[1])

class Bullet(pygame.sprite.Sprite):

    strong = 100
    fast = 10
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

